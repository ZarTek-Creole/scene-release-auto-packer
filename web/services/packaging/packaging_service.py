"""Service de packaging complet de releases selon format Scene.

Ce service génère le package final d'une release selon les standards Scene :
structure de dossiers, fichiers ZIP, NFO conforme, checksums et validation finale.

Architecture :
- Création structure dossiers conforme Scene (GROUPE-ReleaseName-YYYYMMDD)
- Copie fichiers source dans structure
- Génération fichier NFO avec NfoGeneratorService
- Création fichier ZIP final
- Génération checksums (SHA-256, MD5)
- Validation finale avant retour

Complexité moyenne : O(n) où n est la taille totale des fichiers à packager.
Les opérations de copie et création ZIP sont dépendantes de la taille des fichiers.
"""

from __future__ import annotations

import hashlib
import logging
import shutil
import zipfile
from pathlib import Path
from typing import Any

from web.services.packaging.nfo_generator import NfoGeneratorService

logger = logging.getLogger(__name__)


class PackagingService:
    """Service de packaging complet de releases selon format Scene.

    Ce service implémente la logique complète de packaging d'une release selon
    les standards Scene. Il génère la structure de dossiers conforme, copie les
    fichiers source, génère le fichier NFO, crée le fichier ZIP final et calcule
    les checksums pour garantir l'intégrité.

    Fonctionnalités :
    - Création structure dossiers conforme Scene
    - Copie fichiers source dans structure
    - Génération fichier NFO avec NfoGeneratorService
    - Création fichier ZIP final
    - Génération checksums SHA-256 et MD5
    - Validation finale du package

    Structure Scene typique :
    ```
    ReleaseName-GROUP/
    ├── ReleaseName-GROUP.epub
    ├── ReleaseName-GROUP.nfo
    ├── ReleaseName-GROUP.sfv (optionnel)
    └── ReleaseName-GROUP.diz (optionnel)
    ```

    Exemple d'utilisation :
        service = PackagingService()
        release_data = {
            "name": "Test-Book-TESTGROUP-20250124",
            "group": "TESTGROUP",
            "release_type": "EBOOK",
            "files": [...],
            "metadata": {...},
        }
        result = service.package_release(release_data, output_path)
        # Retourne : {"success": True, "zip_path": "...", "checksums": {...}}
    """

    def __init__(self) -> None:
        """Initialise le service de packaging.

        Cette méthode initialise le NfoGeneratorService pour la génération
        des fichiers NFO conformes Scene.

        Complexité : O(1) - Initialisation simple.
        """
        self.nfo_generator = NfoGeneratorService()

    def package_release(
        self, release_data: dict[str, Any], output_path: Path
    ) -> dict[str, Any]:
        """Package une release complète selon format Scene.

        Cette méthode orchestratrice effectue tout le processus de packaging :
        1. Création structure dossiers conforme Scene
        2. Copie fichiers source dans structure
        3. Génération fichier NFO
        4. Création fichier ZIP final
        5. Génération checksums
        6. Validation finale

        Algorithme :
        1. Validation données release (nom, groupe, fichiers)
        2. Création structure dossiers avec _create_directory_structure()
        3. Copie fichiers source vers structure
        4. Génération NFO avec NfoGeneratorService
        5. Création ZIP avec _create_zip_file()
        6. Génération checksums avec _generate_checksums()
        7. Validation finale avec _validate_final_package()
        8. Nettoyage structure temporaire

        Complexité : O(n) où n est la taille totale des fichiers à packager.
        Les opérations de copie et création ZIP sont O(n).

        Gestion des erreurs :
        - Toute erreur pendant le packaging est loggée et levée
        - La structure temporaire est nettoyée en cas d'erreur
        - Les fichiers source ne sont jamais modifiés

        Pièges potentiels :
        - Les fichiers source doivent exister avant copie
        - L'espace disque doit être suffisant pour le ZIP
        - Les permissions doivent permettre création fichiers/dossiers
        - La structure temporaire doit être nettoyée même en cas d'erreur

        Args:
            release_data: Dictionnaire contenant les données de la release :
                - name : Nom de la release (obligatoire)
                - group : Nom du groupe Scene (obligatoire)
                - release_type : Type de release ('TV', 'EBOOK', 'DOCS')
                - files : Liste de dictionnaires avec 'path' et 'name' (obligatoire)
                - metadata : Dictionnaire de métadonnées pour NFO (obligatoire)
                - nfo_content : Contenu NFO pré-généré (optionnel)
            output_path: Chemin du répertoire de sortie pour le package final.

        Returns:
            Dictionnaire contenant :
                - success : True si packaging réussi
                - zip_path : Chemin du fichier ZIP créé
                - checksums : Dictionnaire avec sha256 et md5
                - structure_path : Chemin de la structure créée (optionnel)

        Raises:
            ValueError: Si release_data est invalide (nom vide, fichiers manquants).
            FileNotFoundError: Si un fichier source n'existe pas.
            PermissionError: Si permissions insuffisantes pour créer fichiers/dossiers.
        """
        # Validation données release
        release_name = release_data.get("name", "").strip()
        if not release_name:
            raise ValueError("Le nom de la release ne peut pas être vide")

        files = release_data.get("files", [])
        if not files:
            raise ValueError("Au moins un fichier est requis pour le packaging")

        # Créer structure dossiers conforme Scene
        structure_path = self._create_directory_structure(release_name, output_path)

        try:
            # Copier fichiers source dans structure
            copied_files = []
            for file_info in files:
                source_path = Path(file_info["path"])
                dest_name = file_info.get("name", source_path.name)
                dest_path = structure_path / dest_name

                if not source_path.exists():
                    raise FileNotFoundError(f"Fichier source introuvable: {source_path}")

                shutil.copy2(source_path, dest_path)
                copied_files.append(dest_path)
                logger.info(f"Fichier copié: {source_path} -> {dest_path}")

            # Générer fichier NFO
            metadata = release_data.get("metadata", {})
            metadata["group"] = release_data.get("group", "")
            metadata["date"] = release_data.get("date", "")

            nfo_content = release_data.get("nfo_content")
            if not nfo_content:
                nfo_content = self.nfo_generator.generate_nfo(metadata)

            nfo_path = structure_path / f"{release_name}.nfo"
            nfo_path.write_text(nfo_content, encoding="utf-8")
            logger.info(f"Fichier NFO généré: {nfo_path}")

            # Créer fichier ZIP final
            zip_path = self._create_zip_file(structure_path, output_path)

            # Générer checksums du ZIP final
            checksums = self._generate_checksums(zip_path)

            # Validation finale
            self._validate_final_package(zip_path)

            return {
                "success": True,
                "zip_path": str(zip_path),
                "checksums": checksums,
                "structure_path": str(structure_path),
            }

        except Exception as e:
            # En cas d'erreur, nettoyer structure temporaire si possible
            logger.error(f"Erreur lors du packaging: {e}")
            if structure_path.exists():
                try:
                    shutil.rmtree(structure_path)
                except Exception:
                    pass  # Ignorer erreurs de nettoyage
            raise

    def _create_directory_structure(
        self, release_name: str, output_path: Path
    ) -> Path:
        """Crée la structure de dossiers conforme Scene.

        Cette méthode crée le dossier principal de la release avec le nom formaté
        selon les standards Scene. La structure est créée dans le répertoire de sortie.

        Algorithme :
        1. Validation nom release (non vide)
        2. Création chemin complet dans output_path
        3. Création dossier avec mkdir(parents=True)
        4. Retour chemin créé

        Complexité : O(1) - Création d'un seul dossier.

        Pièges potentiels :
        - Le nom release ne doit pas contenir de caractères interdits pour chemins
        - Les permissions doivent permettre création de dossiers
        - Si le dossier existe déjà, création échoue (à gérer selon besoin)

        Args:
            release_name: Nom de la release formaté (ex: "Test-Book-TESTGROUP-20250124").
            output_path: Répertoire de sortie pour créer la structure.

        Returns:
            Chemin Path du dossier créé.

        Raises:
            ValueError: Si release_name est vide.
            PermissionError: Si permissions insuffisantes pour créer le dossier.
        """
        if not release_name:
            raise ValueError("Le nom de la release ne peut pas être vide")

        structure_path = output_path / release_name

        # Créer le dossier (créer parents si nécessaire)
        structure_path.mkdir(parents=True, exist_ok=False)

        logger.info(f"Structure créée: {structure_path}")

        return structure_path

    def _create_zip_file(self, source_dir: Path, output_path: Path) -> Path:
        """Crée un fichier ZIP à partir d'un répertoire source.

        Cette méthode crée un fichier ZIP contenant tous les fichiers et dossiers
        du répertoire source, en préservant la structure arborescente.

        Algorithme :
        1. Déterminer nom fichier ZIP (basé sur nom répertoire source)
        2. Créer fichier ZIP avec zipfile.ZipFile
        3. Parcourir récursivement tous les fichiers du répertoire source
        4. Ajouter chaque fichier au ZIP avec chemin relatif préservé
        5. Fermer le ZIP et retourner chemin

        Complexité : O(n) où n est le nombre de fichiers à compresser.
        La compression dépend de la taille des fichiers (O(m) où m est la taille).

        Pièges potentiels :
        - Les fichiers symlinks doivent être traités correctement
        - Les permissions doivent être préservées si nécessaire
        - L'espace disque doit être suffisant pour le ZIP
        - Les noms de fichiers avec caractères spéciaux doivent être gérés

        Args:
            source_dir: Répertoire source à compresser.
            output_path: Répertoire de sortie pour le fichier ZIP.

        Returns:
            Chemin Path du fichier ZIP créé.

        Raises:
            FileNotFoundError: Si source_dir n'existe pas.
            PermissionError: Si permissions insuffisantes pour créer le ZIP.
        """
        if not source_dir.exists():
            raise FileNotFoundError(f"Répertoire source introuvable: {source_dir}")

        # Nom du fichier ZIP basé sur le nom du répertoire source
        zip_filename = f"{source_dir.name}.zip"
        zip_path = output_path / zip_filename

        # Créer le fichier ZIP
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Parcourir récursivement tous les fichiers du répertoire source
            for file_path in source_dir.rglob("*"):
                if file_path.is_file():
                    # Chemin relatif dans le ZIP (préserver structure)
                    arcname = file_path.relative_to(source_dir)
                    zipf.write(file_path, arcname)
                    logger.debug(f"Ajouté au ZIP: {arcname}")

        logger.info(f"Fichier ZIP créé: {zip_path}")

        return zip_path

    def _generate_checksums(self, file_path: Path) -> dict[str, str]:
        """Génère les checksums SHA-256 et MD5 d'un fichier.

        Cette méthode calcule les checksums SHA-256 et MD5 d'un fichier pour
        garantir l'intégrité. Les checksums sont retournés en format hexadécimal.

        Algorithme :
        1. Ouverture fichier en mode binaire
        2. Lecture par chunks pour fichiers volumineux (mémoire efficace)
        3. Mise à jour hashers SHA-256 et MD5 avec chaque chunk
        4. Calcul des digests finaux en hexadécimal

        Complexité : O(n) où n est la taille du fichier.
        Lecture séquentielle avec chunks pour optimiser mémoire.

        Pièges potentiels :
        - Les fichiers très volumineux peuvent prendre du temps
        - La mémoire doit être suffisante pour les chunks
        - Les fichiers en lecture doivent être fermés proprement

        Args:
            file_path: Chemin du fichier pour lequel calculer les checksums.

        Returns:
            Dictionnaire contenant :
                - sha256 : Checksum SHA-256 (64 caractères hexadécimaux)
                - md5 : Checksum MD5 (32 caractères hexadécimaux)

        Raises:
            FileNotFoundError: Si file_path n'existe pas.
            PermissionError: Si permissions insuffisantes pour lire le fichier.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Fichier introuvable: {file_path}")

        sha256_hash = hashlib.sha256()
        md5_hash = hashlib.md5()

        # Lecture par chunks pour optimiser mémoire (taille chunk : 64KB)
        chunk_size = 65536

        with file_path.open("rb") as f:
            while chunk := f.read(chunk_size):
                sha256_hash.update(chunk)
                md5_hash.update(chunk)

        return {
            "sha256": sha256_hash.hexdigest(),
            "md5": md5_hash.hexdigest(),
        }

    def _validate_final_package(self, zip_path: Path) -> bool:
        """Valide le package final créé.

        Cette méthode effectue une validation basique du package ZIP final :
        vérification existence, taille non nulle, et validité du format ZIP.

        Algorithme :
        1. Vérification existence fichier
        2. Vérification taille > 0
        3. Vérification format ZIP valide (tentative ouverture)

        Complexité : O(1) - Vérifications simples.

        Args:
            zip_path: Chemin du fichier ZIP à valider.

        Returns:
            True si le package est valide, False sinon.

        Raises:
            FileNotFoundError: Si zip_path n'existe pas.
        """
        if not zip_path.exists():
            raise FileNotFoundError(f"Fichier ZIP introuvable: {zip_path}")

        # Vérifier taille > 0
        if zip_path.stat().st_size == 0:
            logger.error(f"Fichier ZIP vide: {zip_path}")
            return False

        # Vérifier format ZIP valide (tentative ouverture)
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # Vérifier que le ZIP n'est pas corrompu
                zip_ref.testzip()
        except zipfile.BadZipFile:
            logger.error(f"Fichier ZIP corrompu: {zip_path}")
            return False

        logger.info(f"Package validé: {zip_path}")

        return True

