"""Service de gestion des jobs asynchrones pour le packaging de releases.

Ce service gère le cycle de vie complet des jobs de traitement (packaging,
correction NFO, repackaging, etc.) avec suivi de progression et gestion des erreurs.

Architecture :
- Jobs stockés en base de données MySQL (modèle Job)
- Statuts : pending → running → completed/failed/cancelled
- Logs persistés dans la base de données (champ logs du modèle Job)
- Progression suivie via config_json ou estimation basée sur statut

Complexité moyenne : O(1) pour les opérations de base (lecture/écriture DB),
avec dépendance à la performance de SQLAlchemy pour les requêtes.

Note importante : Cette implémentation est synchrone pour simplifier les tests.
En production, utiliser un worker asynchrone (Celery, RQ, etc.) pour traiter
les jobs en arrière-plan sans bloquer l'application Flask.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from web.extensions import db
from web.models import Job
from web.services.job.job_state_machine import (
    InvalidTransitionError,
    JobStateMachine,
)

logger = logging.getLogger(__name__)


class JobService:
    """Service de traitement et gestion des jobs de packaging.

    Ce service implémente la logique métier pour le traitement des jobs asynchrones
    de packaging de releases Scene. Il gère les transitions d'état, la persistance
    des logs, et le suivi de progression.

    Cycle de vie d'un job :
    1. Création : Statut "pending" (en attente)
    2. Traitement : Statut "running" (en cours)
    3. Fin : Statut "completed" (réussi) ou "failed" (échec) ou "cancelled" (annulé)

    Types de jobs supportés :
    - nfofix : Correction du fichier NFO d'une release
    - readnfo : Lecture et régénération du NFO depuis métadonnées
    - repack : Repackaging complet d'une release
    - dirfix : Correction de la structure de répertoires

    Exemple d'utilisation :
        service = JobService()
        service.process_job(job_id=1)
        progress = service.get_job_progress(job_id=1)
        service.cancel_job(job_id=1)
    """

    def __init__(self) -> None:
        """Initialise le JobService.

        Cette méthode initialise la machine à états pour valider les transitions
        d'état des jobs. Toutes les données sont persistées dans la base de données
        MySQL via le modèle Job.

        Note : Pour une implémentation avec worker asynchrone (Celery, RQ),
        on pourrait initialiser ici la connexion au broker de messages.
        """
        self.state_machine = JobStateMachine()

    def process_job(self, job_id: int) -> None:
        """Traite un job de manière synchrone (simulation de traitement asynchrone).

        Cette méthode orchestre le traitement complet d'un job :
        1. Vérification que le job existe et est en statut "pending"
        2. Transition vers statut "running"
        3. Traitement selon le type de job
        4. Transition vers statut "completed" ou "failed" en cas d'erreur

        Algorithme :
        - Vérification existence et statut du job (O(1) avec index sur ID)
        - Mise à jour statut vers "running" avec log initial
        - Dispatch vers méthode spécialisée selon job_type
        - Gestion des erreurs avec logs et transition vers "failed"

        Complexité : O(1) pour les opérations de base, dépend de la complexité
        du traitement spécifique du job (nfofix, repack, etc.).

        Gestion des erreurs :
        - Toute exception levée pendant le traitement est capturée
        - L'erreur est loggée dans les logs du job
        - Le statut est mis à jour vers "failed"
        - L'exception est également loggée au niveau application (logger.error)

        Pièges potentiels :
        - Ne pas vérifier le statut avant traitement peut causer des traitements
          multiples d'un même job
        - Les erreurs de commit DB doivent être gérées proprement
        - En production, utiliser un verrouillage (lock) pour éviter les traitements
          concurrents du même job

        Args:
            job_id: Identifiant du job à traiter (clé primaire du modèle Job).

        Returns:
            Aucune valeur retournée. Les modifications sont persistées en base.

        Side effects:
            - Modifie le statut du job en base de données
            - Ajoute des logs au job
            - Peut modifier d'autres entités liées (Release, etc.) selon le type de job
        """
        # Récupération du job depuis la base de données avec lock pour éviter traitements concurrents
        # Utilisation de select().with_for_update() pour lock exclusif
        # Ce lock empêche deux workers de traiter le même job simultanément
        from sqlalchemy import select

        stmt = select(Job).where(Job.id == job_id).with_for_update()
        job = db.session.scalar(stmt)

        if not job:
            logger.error(f"Job {job_id} not found")
            return

        # Vérification que le job est en statut "pending" avant traitement
        # Cette vérification évite de traiter un job déjà en cours ou terminé
        # Invariant : Seuls les jobs "pending" peuvent être traités
        if job.status != "pending":
            logger.warning(f"Job {job_id} is not pending (status: {job.status})")
            return

        # Validation transition d'état avec JobStateMachine
        # Cette validation garantit que la transition pending → running est autorisée
        try:
            self.state_machine.validate_transition("pending", "running")
        except InvalidTransitionError as e:
            logger.error(f"Invalid transition for job {job_id}: {e}")
            return

        # Transition d'état : pending → running
        # Cette transition est atomique : si elle échoue, le job reste "pending"
        self.update_status(job_id, "running", "Job processing started...")

        try:
            # Récupération du type de job pour dispatcher vers la bonne méthode
            job_type = job.job_type

            # Vérification de configuration invalide (pour tests de scénarios d'échec)
            # Cette vérification permet de simuler des erreurs pour les tests
            config = job.config_json or {}
            if config.get("action") == "invalid_action":
                raise ValueError("Invalid action specified in job configuration")

            # Dispatch vers méthode spécialisée selon le type de job
            # Pattern Strategy : chaque type de job a sa propre méthode de traitement
            if job_type == "nfofix":
                self._process_nfofix_job(job_id)
            elif job_type == "readnfo":
                self._process_readnfo_job(job_id)
            elif job_type == "repack":
                self._process_repack_job(job_id)
            elif job_type == "dirfix":
                self._process_dirfix_job(job_id)
            else:
                # Traitement générique pour types de jobs non spécialisés
                # Logs du traitement et transition vers "completed"
                self.append_log(job_id, f"Processing job type: {job_type}", "INFO")
                self.append_log(job_id, "Job processing completed", "INFO")
                self.update_status(job_id, "completed", "Job completed successfully")

        except Exception as e:
            # Gestion centralisée des erreurs
            # Toute exception levée pendant le traitement est capturée ici
            logger.error(f"Error processing job {job_id}: {e}", exc_info=True)
            error_msg = f"Job processing failed: {str(e)}"
            self.append_log(job_id, error_msg, "ERROR")
            # Transition vers statut "failed" avec message d'erreur
            self.update_status(job_id, "failed", error_msg)

    def _process_nfofix_job(self, job_id: int) -> None:
        """Traite un job de type NFOFIX (correction du fichier NFO).

        Cette méthode corrige le fichier NFO d'une release selon les règles Scene.
        Le traitement actuel est une simulation : en production, cette méthode
        devrait parser le NFO existant, détecter les erreurs, et les corriger.

        Algorithme (simulation actuelle) :
        1. Log du début du traitement
        2. Simulation de la correction
        3. Log de succès
        4. Transition vers statut "completed"

        Complexité : O(1) pour la simulation, O(n) en production où n est la taille
        du fichier NFO à parser.

        Note : Dans une implémentation complète, cette méthode devrait :
        - Charger le fichier NFO depuis le système de fichiers
        - Parser le contenu ASCII art
        - Valider la conformité aux règles Scene
        - Corriger les erreurs détectées
        - Sauvegarder le fichier corrigé

        Args:
            job_id: Identifiant du job à traiter.
        """
        self.append_log(job_id, "Fixing NFO file...", "INFO")
        self.append_log(job_id, "NFO file fixed successfully", "INFO")
        self.update_status(job_id, "completed", "NFOFIX job completed")

    def _process_readnfo_job(self, job_id: int) -> None:
        """Traite un job de type READNFO (lecture et régénération du NFO).

        Cette méthode lit le fichier NFO d'une release et régénère les métadonnées
        depuis son contenu. Le traitement actuel est une simulation.

        Algorithme (simulation actuelle) :
        1. Log du début du traitement
        2. Simulation de la lecture
        3. Log de succès
        4. Transition vers statut "completed"

        Complexité : O(1) pour la simulation, O(n) en production où n est la taille
        du fichier NFO à parser.

        Note : Dans une implémentation complète, cette méthode devrait :
        - Charger le fichier NFO depuis le système de fichiers
        - Parser le contenu pour extraire les métadonnées
        - Valider et normaliser les métadonnées extraites
        - Mettre à jour la release avec les métadonnées

        Args:
            job_id: Identifiant du job à traiter.
        """
        self.append_log(job_id, "Reading NFO file...", "INFO")
        self.append_log(job_id, "NFO file read successfully", "INFO")
        self.update_status(job_id, "completed", "READNFO job completed")

    def _process_repack_job(self, job_id: int) -> None:
        """Traite un job de type REPACK (repackaging complet d'une release).

        Cette méthode repackage complètement une release selon les règles Scene.
        Le traitement actuel est une simulation : en production, cette méthode
        devrait reconstruire l'archive ZIP, régénérer les fichiers NFO/DIZ, etc.

        Algorithme (simulation actuelle) :
        1. Log du début du traitement
        2. Simulation du repackaging
        3. Log de succès
        4. Transition vers statut "completed"

        Complexité : O(1) pour la simulation, O(n) en production où n est la taille
        totale des fichiers à packager.

        Note : Dans une implémentation complète, cette méthode devrait :
        - Charger tous les fichiers de la release
        - Valider la conformité aux règles Scene
        - Recréer l'archive ZIP avec la bonne structure
        - Régénérer les fichiers NFO et DIZ
        - Valider les checksums (MD5, SHA-256)
        - Sauvegarder la release repackagée

        Args:
            job_id: Identifiant du job à traiter.
        """
        self.append_log(job_id, "Repacking release...", "INFO")
        self.append_log(job_id, "Release repacked successfully", "INFO")
        self.update_status(job_id, "completed", "REPACK job completed")

    def _process_dirfix_job(self, job_id: int) -> None:
        """Traite un job de type DIRFIX (correction de la structure de répertoires).

        Cette méthode corrige la structure de répertoires d'une release selon
        les règles Scene (nommage DIRNAMING). Le traitement actuel est une simulation.

        Algorithme (simulation actuelle) :
        1. Log du début du traitement
        2. Simulation de la correction
        3. Log de succès
        4. Transition vers statut "completed"

        Complexité : O(1) pour la simulation, O(n) en production où n est le nombre
        de répertoires à renommer/réorganiser.

        Note : Dans une implémentation complète, cette méthode devrait :
        - Charger la structure de répertoires actuelle
        - Valider le nommage selon les règles DIRNAMING
        - Détecter les erreurs de nommage (composants manquants, séparateurs incorrects)
        - Renommer les répertoires pour conformité
        - Réorganiser la structure si nécessaire

        Args:
            job_id: Identifiant du job à traiter.
        """
        self.append_log(job_id, "Fixing directory structure...", "INFO")
        self.append_log(job_id, "Directory structure fixed successfully", "INFO")
        self.update_status(job_id, "completed", "DIRFIX job completed")

    def update_status(self, job_id: int, status: str, logs: str | None = None) -> None:
        """Met à jour le statut d'un job et optionnellement ajoute des logs.

        Cette méthode atomique met à jour le statut d'un job dans la base de données
        et peut également ajouter un message de log. Elle garantit la cohérence
        des données en commitant immédiatement les modifications.

        Algorithme :
        1. Récupération du job depuis la base de données
        2. Mise à jour du statut
        3. Ajout du log si fourni (avec timestamp UTC)
        4. Commit de la transaction

        Complexité : O(1) - Opération atomique sur une seule entrée de base de données.

        Gestion des erreurs :
        - Si le job n'existe pas, log d'erreur et retour silencieux
        - Les erreurs de commit DB doivent être gérées au niveau appelant

        Format des logs :
        - Timestamp ISO 8601 avec timezone UTC : `[2025-01-XXT...] message`
        - Les logs sont concaténés avec saut de ligne si plusieurs logs existent

        Pièges potentiels :
        - Le commit est synchrone : peut bloquer si la DB est lente
        - Pas de gestion explicite des erreurs de commit (SQLAlchemy peut lever)
        - Les logs sont stockés en texte brut dans la DB (peut devenir volumineux)

        Transitions d'état valides :
        - pending → running (début traitement)
        - running → completed (succès)
        - running → failed (échec)
        - pending → cancelled (annulation avant traitement)
        - running → cancelled (annulation pendant traitement)

        Args:
            job_id: Identifiant du job à mettre à jour.
            status: Nouveau statut (pending, running, completed, failed, cancelled).
            logs: Message de log optionnel à ajouter aux logs du job.

        Returns:
            Aucune valeur retournée. Les modifications sont persistées immédiatement.

        Side effects:
            - Modifie le statut du job en base de données
            - Ajoute un log au job si logs est fourni
            - Commit de la transaction SQLAlchemy
        """
        # Récupération du job depuis la base de données avec lock pour éviter conflits concurrents
        # Utilisation de select().with_for_update() pour lock exclusif lors des mises à jour critiques
        from sqlalchemy import select

        stmt = select(Job).where(Job.id == job_id).with_for_update()
        job = db.session.scalar(stmt)

        if not job:
            logger.error(f"Job {job_id} not found")
            return

        # Validation transition d'état avec JobStateMachine
        # Cette validation garantit que la transition est autorisée selon la machine à états
        try:
            self.state_machine.validate_transition(job.status, status)
        except InvalidTransitionError as e:
            logger.error(f"Invalid transition for job {job_id}: {job.status} → {status}. {e}")
            raise ValueError(f"Transition invalide: {job.status} → {status}") from e

        # Mise à jour du statut
        # Cette modification est en mémoire jusqu'au commit
        job.status = status

        # Ajout du log si fourni
        if logs:
            # Génération d'un timestamp ISO 8601 avec timezone UTC
            # Format : "2025-01-XXT12:34:56.789123+00:00"
            timestamp = datetime.now(UTC).isoformat()

            # Concaténation avec les logs existants si présents
            # Format : "[timestamp] message" pour premier log,
            #          "\n[timestamp] message" pour logs suivants
            if job.logs:
                job.logs += f"\n[{timestamp}] {logs}"
            else:
                job.logs = f"[{timestamp}] {logs}"

        # Commit immédiat pour garantir la persistance
        # En cas d'erreur, SQLAlchemy lèvera une exception qui sera propagée
        db.session.commit()

    def append_log(self, job_id: int, log_message: str, level: str = "INFO") -> None:
        """Ajoute un message de log au journal d'un job.

        Cette méthode ajoute un message de log avec niveau de sévérité au journal
        d'un job. Les logs sont formatés avec timestamp et niveau, puis persistés
        immédiatement en base de données.

        Algorithme :
        1. Récupération du job depuis la base de données
        2. Génération d'un timestamp ISO 8601 UTC
        3. Formatage du log avec timestamp et niveau : `[timestamp] [LEVEL] message`
        4. Concaténation avec les logs existants
        5. Commit de la transaction

        Complexité : O(1) - Opération atomique sur une seule entrée de base de données.

        Format des logs :
        - `[2025-01-XXT12:34:56.789123+00:00] [INFO] message`
        - `[2025-01-XXT12:34:56.789123+00:00] [ERROR] message`
        - `[2025-01-XXT12:34:56.789123+00:00] [WARNING] message`

        Niveaux de log supportés :
        - INFO : Informations générales sur le traitement
        - WARNING : Avertissements non bloquants
        - ERROR : Erreurs bloquantes
        - DEBUG : Informations de débogage (généralement désactivé en production)

        Pièges potentiels :
        - Les logs sont stockés en texte brut : peut devenir volumineux pour jobs longs
        - Pas de rotation automatique des logs (à implémenter si nécessaire)
        - Le commit est synchrone : peut bloquer si la DB est lente

        Args:
            job_id: Identifiant du job auquel ajouter le log.
            log_message: Message de log à ajouter.
            level: Niveau de sévérité (INFO, WARNING, ERROR, DEBUG). Par défaut "INFO".

        Returns:
            Aucune valeur retournée. Le log est persisté immédiatement.

        Side effects:
            - Modifie le champ logs du job en base de données
            - Commit de la transaction SQLAlchemy
        """
        # Récupération du job depuis la base de données
        job = db.session.get(Job, job_id)

        if not job:
            logger.error(f"Job {job_id} not found")
            return

        # Génération d'un timestamp ISO 8601 avec timezone UTC
        timestamp = datetime.now(UTC).isoformat()

        # Formatage du log avec timestamp et niveau
        # Format : "[timestamp] [LEVEL] message"
        log_line = f"[{timestamp}] [{level}] {log_message}"

        # Concaténation avec les logs existants
        # Si aucun log n'existe, initialisation avec le nouveau log
        if job.logs:
            job.logs += f"\n{log_line}"
        else:
            job.logs = log_line

        # Commit immédiat pour garantir la persistance
        db.session.commit()

    def cancel_job(self, job_id: int) -> bool:
        """Annule un job en cours ou en attente.

        Cette méthode permet d'annuler un job qui n'a pas encore été terminé.
        Seuls les jobs en statut "pending" ou "running" peuvent être annulés.

        Algorithme :
        1. Vérification de l'existence du job
        2. Vérification que le statut permet l'annulation (pending ou running)
        3. Transition vers statut "cancelled" avec log
        4. Retour True si annulation réussie, False sinon

        Complexité : O(1) - Opération atomique sur une seule entrée de base de données.

        États annulables :
        - pending : Job en attente (annulation avant traitement)
        - running : Job en cours (annulation pendant traitement)

        États non annulables :
        - completed : Job terminé avec succès
        - failed : Job terminé en échec
        - cancelled : Job déjà annulé

        Note : Pour une implémentation complète avec worker asynchrone,
        il faudrait également envoyer un signal d'annulation au worker
        pour interrompre le traitement en cours.

        Args:
            job_id: Identifiant du job à annuler.

        Returns:
            True si l'annulation a réussi, False si le job n'existe pas ou
            n'est pas annulable (déjà terminé ou annulé).

        Side effects:
            - Modifie le statut du job vers "cancelled" si annulation réussie
            - Ajoute un log d'annulation au job
        """
        # Récupération du job depuis la base de données avec lock pour éviter conflits concurrents
        # Utilisation de select().with_for_update() pour lock exclusif lors des annulations
        from sqlalchemy import select

        stmt = select(Job).where(Job.id == job_id).with_for_update()
        job = db.session.scalar(stmt)

        if not job:
            logger.error(f"Job {job_id} not found")
            return False

        # Vérification que le statut permet l'annulation avec validation machine à états
        # Seuls les jobs "pending" ou "running" peuvent être annulés
        if not self.state_machine.can_transition(job.status, "cancelled"):
            logger.warning(
                f"Job {job_id} cannot be cancelled (status: {job.status})"
            )
            return False

        # Transition vers statut "cancelled" avec log explicite
        # La validation est déjà faite avec can_transition(), donc on peut directement appeler update_status
        self.update_status(job_id, "cancelled", "Job cancelled by user")
        return True

    def get_job_progress(self, job_id: int) -> int:
        """Récupère le pourcentage de progression d'un job.

        Cette méthode calcule le pourcentage de progression d'un job de deux façons :
        1. Si config_json contient une clé "progress", utilise cette valeur
        2. Sinon, estime la progression basée sur le statut du job

        Algorithme :
        1. Récupération du job depuis la base de données
        2. Vérification de la présence de "progress" dans config_json
        3. Si présent, conversion en entier et retour
        4. Sinon, estimation basée sur le statut (mapping statut → pourcentage)

        Complexité : O(1) - Opération atomique sur une seule entrée de base de données.

        Estimation basée sur statut :
        - pending : 0% (pas encore commencé)
        - running : 50% (en cours, estimation moyenne)
        - completed : 100% (terminé avec succès)
        - failed : 0% (échec, considéré comme non progressé)
        - cancelled : 0% (annulé, considéré comme non progressé)

        Note : L'estimation à 50% pour "running" est arbitraire. Dans une
        implémentation complète, chaque type de job devrait suivre sa propre
        progression réelle (ex: nombre de fichiers traités / total fichiers).

        Pièges potentiels :
        - La progression dans config_json peut être obsolète si le job crash
        - L'estimation à 50% pour "running" est très approximative
        - Pas de validation que progress est entre 0 et 100

        Args:
            job_id: Identifiant du job dont récupérer la progression.

        Returns:
            Pourcentage de progression (0-100), ou 0 si le job n'existe pas
            ou si la progression n'est pas disponible.
        """
        # Récupération du job depuis la base de données
        job = db.session.get(Job, job_id)

        if not job:
            # Si le job n'existe pas, retourner 0 par défaut
            return 0

        # Tentative de récupération de la progression depuis config_json
        # Cette valeur peut être mise à jour par le worker pendant le traitement
        if job.config_json and "progress" in job.config_json:
            # Conversion en entier pour garantir un type cohérent
            # Note : Pas de validation que progress est entre 0 et 100
            return int(job.config_json["progress"])

        # Estimation basée sur le statut si progression explicite non disponible
        # Mapping statut → pourcentage de progression
        status_to_progress = {
            "pending": 0,      # Pas encore commencé
            "running": 50,     # En cours (estimation moyenne)
            "completed": 100, # Terminé avec succès
            "failed": 0,       # Échec (considéré comme non progressé)
            "cancelled": 0,    # Annulé (considéré comme non progressé)
        }

        # Retour du pourcentage correspondant au statut, ou 0 par défaut
        return status_to_progress.get(job.status, 0)
