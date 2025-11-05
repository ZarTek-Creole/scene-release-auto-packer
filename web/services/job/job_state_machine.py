"""Machine à états finis pour les transitions d'état des jobs.

Ce module implémente une machine à états finis stricte pour garantir que seules
les transitions d'état valides sont autorisées lors du traitement des jobs.

Architecture :
- États finaux définis : pending, running, completed, failed, cancelled
- Transitions autorisées :
  * pending → running (démarrage traitement)
  * pending → cancelled (annulation avant traitement)
  * running → completed (succès)
  * running → failed (échec)
  * running → cancelled (annulation pendant traitement)
- États finaux : completed, failed, cancelled (aucune transition sortante)

Complexité : O(1) pour toutes les opérations (validation, récupération transitions).
Les transitions sont stockées dans un dictionnaire pour accès constant.

Invariants :
- Un job ne peut jamais passer directement de pending à completed/failed
- Un job dans un état final ne peut plus changer d'état
- Toutes les transitions doivent être validées avant mise à jour en base
"""

from __future__ import annotations

import logging
from typing import Final

logger = logging.getLogger(__name__)


class InvalidTransitionError(Exception):
    """Exception levée lors d'une tentative de transition d'état invalide.

    Cette exception est utilisée pour signaler qu'une transition d'état n'est
    pas autorisée selon la machine à états finis définie.

    Exemple :
        raise InvalidTransitionError("pending", "completed")
    """

    def __init__(self, from_status: str, to_status: str) -> None:
        """Initialise l'exception avec les statuts concernés.

        Args:
            from_status: Statut source de la transition.
            to_status: Statut cible de la transition.
        """
        self.from_status = from_status.lower()
        self.to_status = to_status.lower()
        message = (
            f"Transition invalide de '{from_status}' vers '{to_status}'. "
            f"Transitions autorisées depuis '{from_status}': "
            f"{', '.join(self._get_allowed_transitions_for_status(from_status))}"
        )
        super().__init__(message)

    def _get_allowed_transitions_for_status(self, status: str) -> list[str]:
        """Récupère les transitions autorisées pour un statut (méthode interne).

        Cette méthode est utilisée uniquement pour générer le message d'erreur.
        Elle ne doit pas être utilisée ailleurs, utiliser JobStateMachine à la place.
        """
        transitions_map: dict[str, list[str]] = {
            "pending": ["running", "cancelled"],
            "running": ["completed", "failed", "cancelled"],
            "completed": [],
            "failed": [],
            "cancelled": [],
        }
        return transitions_map.get(status.lower(), [])


class JobStateMachine:
    """Machine à états finis pour validation des transitions d'état des jobs.

    Cette classe implémente une machine à états finis stricte pour garantir
    la cohérence des transitions d'état lors du traitement des jobs de packaging.

    La machine à états empêche les transitions invalides comme :
    - PENDING → COMPLETED (doit passer par RUNNING)
    - PENDING → FAILED (doit passer par RUNNING)
    - COMPLETED → RUNNING (état final)
    - FAILED → RUNNING (état final)
    - CANCELLED → RUNNING (état final)

    États supportés :
    - pending : Job créé, en attente de traitement
    - running : Job en cours de traitement
    - completed : Job terminé avec succès (état final)
    - failed : Job terminé en échec (état final)
    - cancelled : Job annulé (état final)

    Transitions autorisées :
    - pending → running : Démarrage du traitement
    - pending → cancelled : Annulation avant traitement
    - running → completed : Succès du traitement
    - running → failed : Échec du traitement
    - running → cancelled : Annulation pendant traitement

    Exemple d'utilisation :
        machine = JobStateMachine()

        # Vérifier si transition valide
        if machine.can_transition("pending", "running"):
            job.status = "running"

        # Valider transition (lève exception si invalide)
        machine.validate_transition("pending", "running")

        # Récupérer toutes les transitions autorisées
        transitions = machine.get_allowed_transitions("pending")
        # Retourne : ["running", "cancelled"]
    """

    # États finaux supportés (normalisés en lowercase)
    VALID_STATES: Final[list[str]] = [
        "pending",
        "running",
        "completed",
        "failed",
        "cancelled",
    ]

    # États finaux (aucune transition sortante autorisée)
    FINAL_STATES: Final[list[str]] = ["completed", "failed", "cancelled"]

    # Carte des transitions autorisées
    # Clé : état source, Valeur : liste des états cibles autorisés
    TRANSITIONS: Final[dict[str, list[str]]] = {
        "pending": ["running", "cancelled"],
        "running": ["completed", "failed", "cancelled"],
        "completed": [],  # État final
        "failed": [],  # État final
        "cancelled": [],  # État final
    }

    def __init__(self) -> None:
        """Initialise la machine à états finis.

        Cette méthode est vide car la machine à états n'a pas besoin d'état interne.
        Toutes les transitions sont définies statiquement dans TRANSITIONS.

        Complexité : O(1) - Initialisation simple sans dépendances.
        """

    def _normalize_status(self, status: str) -> str:
        """Normalise un statut en lowercase pour comparaison case-insensitive.

        Cette méthode interne permet de gérer les statuts de manière case-insensitive,
        évitant les erreurs dues à des différences de casse (ex: "Pending" vs "pending").

        Args:
            status: Statut à normaliser.

        Returns:
            Statut normalisé en lowercase.

        Raises:
            ValueError: Si le statut n'est pas dans VALID_STATES.
        """
        normalized = status.lower()
        if normalized not in self.VALID_STATES:
            raise ValueError(
                f"Statut invalide: '{status}'. Statuts valides: {', '.join(self.VALID_STATES)}"
            )
        return normalized

    def can_transition(self, from_status: str, to_status: str) -> bool:
        """Vérifie si une transition d'état est autorisée.

        Cette méthode vérifie si une transition depuis un état source vers un état
        cible est autorisée selon la machine à états finis définie.

        Algorithme :
        1. Normalisation des statuts (case-insensitive)
        2. Vérification que les statuts sont valides
        3. Recherche de la transition dans TRANSITIONS
        4. Retour True si transition autorisée, False sinon

        Complexité : O(1) - Recherche dans dictionnaire avec clé hashée.

        Args:
            from_status: Statut source de la transition.
            to_status: Statut cible de la transition.

        Returns:
            True si la transition est autorisée, False sinon.

        Raises:
            ValueError: Si from_status ou to_status n'est pas dans VALID_STATES.

        Example:
            >>> machine = JobStateMachine()
            >>> machine.can_transition("pending", "running")
            True
            >>> machine.can_transition("pending", "completed")
            False
        """
        normalized_from = self._normalize_status(from_status)
        normalized_to = self._normalize_status(to_status)

        # Récupérer les transitions autorisées depuis l'état source
        allowed_transitions = self.TRANSITIONS.get(normalized_from, [])

        # Vérifier si la transition cible est autorisée
        return normalized_to in allowed_transitions

    def validate_transition(self, from_status: str, to_status: str) -> None:
        """Valide une transition d'état et lève une exception si invalide.

        Cette méthode est une version stricte de can_transition() qui lève une
        exception si la transition n'est pas autorisée. Elle est recommandée
        pour valider les transitions avant de mettre à jour le statut en base
        de données.

        Algorithme :
        1. Vérification avec can_transition()
        2. Si transition invalide, lever InvalidTransitionError avec message détaillé
        3. Si transition valide, ne rien faire (pas d'exception)

        Complexité : O(1) - Appel à can_transition() qui est O(1).

        Args:
            from_status: Statut source de la transition.
            to_status: Statut cible de la transition.

        Raises:
            ValueError: Si from_status ou to_status n'est pas dans VALID_STATES.
            InvalidTransitionError: Si la transition n'est pas autorisée.

        Example:
            >>> machine = JobStateMachine()
            >>> machine.validate_transition("pending", "running")  # OK
            >>> machine.validate_transition("pending", "completed")  # Lève InvalidTransitionError
        """
        if not self.can_transition(from_status, to_status):
            raise InvalidTransitionError(from_status, to_status)

    def get_allowed_transitions(self, status: str) -> list[str]:
        """Récupère toutes les transitions autorisées depuis un statut donné.

        Cette méthode retourne la liste complète des états vers lesquels il est
        possible de transitionner depuis le statut donné. Utile pour générer
        des interfaces utilisateur ou des logs détaillés.

        Algorithme :
        1. Normalisation du statut
        2. Recherche dans TRANSITIONS
        3. Retour de la liste des transitions autorisées (copie pour éviter mutations)

        Complexité : O(1) - Recherche dans dictionnaire, copie de liste O(k) où k
        est le nombre de transitions (généralement ≤ 3).

        Args:
            status: Statut source pour lequel récupérer les transitions autorisées.

        Returns:
            Liste des statuts vers lesquels il est possible de transitionner.
            Liste vide pour les états finaux (completed, failed, cancelled).

        Raises:
            ValueError: Si status n'est pas dans VALID_STATES.

        Example:
            >>> machine = JobStateMachine()
            >>> machine.get_allowed_transitions("pending")
            ['running', 'cancelled']
            >>> machine.get_allowed_transitions("running")
            ['completed', 'failed', 'cancelled']
            >>> machine.get_allowed_transitions("completed")
            []
        """
        normalized_status = self._normalize_status(status)
        transitions = self.TRANSITIONS.get(normalized_status, [])
        # Retourner une copie pour éviter mutations externes
        return transitions.copy()

    def is_final_state(self, status: str) -> bool:
        """Vérifie si un statut est un état final (aucune transition sortante).

        Les états finaux sont : completed, failed, cancelled.
        Un job dans un état final ne peut plus changer d'état.

        Complexité : O(1) - Recherche dans liste FINAL_STATES (petite liste).

        Args:
            status: Statut à vérifier.

        Returns:
            True si le statut est un état final, False sinon.

        Raises:
            ValueError: Si status n'est pas dans VALID_STATES.

        Example:
            >>> machine = JobStateMachine()
            >>> machine.is_final_state("completed")
            True
            >>> machine.is_final_state("pending")
            False
        """
        normalized_status = self._normalize_status(status)
        return normalized_status in self.FINAL_STATES
