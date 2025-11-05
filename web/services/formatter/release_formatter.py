"""Service de formatage des données de release pour affichage et export.

Ce service formate les données de release pour générer des noms de fichiers
et dossiers conformes aux règles Scene, et normalise les métadonnées pour export.

Architecture :
- Formatage noms conformes Scene (GROUPE-ReleaseName-YYYYMMDD)
- Normalisation métadonnées (trim, conversion types, validation)
- Génération noms fichiers/dossiers selon patterns règles

Complexité moyenne : O(n) où n est la taille des données à formater.
Les opérations de formatage sont généralement rapides.
"""

from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


class ReleaseFormatterService:
    """Service de formatage des données de release pour affichage et export.

    Ce service implémente la logique de formatage pour générer des noms de fichiers
    et dossiers conformes aux règles Scene, et normalise les métadonnées pour différents
    formats d'export.

    Fonctionnalités :
    - Formatage noms releases selon patterns Scene
    - Normalisation métadonnées (trim, conversion types)
    - Génération noms fichiers/dossiers conformes
    - Support différents types de releases (TV, EBOOK, DOCS)

    Format nom release Scene :
    - Pattern : `{Title}-{Group}-{YYYYMMDD}`
    - Caractères autorisés : lettres, chiffres, tirets
    - Caractères spéciaux supprimés ou remplacés
    - Longueur max : 255 caractères (limite Scene standard)

    Exemple d'utilisation :
        service = ReleaseFormatterService()
        name = service.format_release_name(
            title="Test Book",
            group="TESTGROUP",
            date="20250124"
        )
        # Retourne : "Test-Book-TESTGROUP-20250124"
    """

    MAX_RELEASE_NAME_LENGTH = 255  # Limite Scene standard
    ALLOWED_CHARS_PATTERN = re.compile(r"[^A-Za-z0-9\-]")

    def __init__(self) -> None:
        """Initialise le service de formatage.

        Cette méthode est vide car le service n'a pas besoin d'état interne.
        Toutes les configurations sont définies comme constantes de classe.

        Complexité : O(1) - Initialisation simple sans dépendances.
        """

    def format_release_name(
        self,
        title: str,
        group: str,
        date: str,
        release_type: str = "EBOOK",
    ) -> str:
        """Formate le nom d'une release selon les règles Scene.

        Cette méthode génère un nom de release conforme aux standards Scene
        avec le pattern : `{Title}-{Group}-{YYYYMMDD}`.

        Algorithme :
        1. Normalisation du titre (trim, suppression caractères spéciaux)
        2. Normalisation du groupe (uppercase, validation format)
        3. Vérification format date (YYYYMMDD)
        4. Construction nom final : Title-Group-Date
        5. Troncature si nécessaire pour respecter limite 255 caractères

        Complexité : O(n) où n est la longueur du titre + groupe.
        Les opérations regex et remplacements sont O(n).

        Pièges potentiels :
        - Les caractères spéciaux doivent être supprimés ou remplacés
        - Le nom final ne doit pas dépasser 255 caractères
        - Le groupe doit être en uppercase
        - La date doit être au format YYYYMMDD

        Args:
            title: Titre de la release (sera normalisé).
            group: Nom du groupe Scene (sera converti en uppercase).
            date: Date de release au format YYYYMMDD.
            release_type: Type de release ('TV', 'EBOOK', 'DOCS').

        Returns:
            Nom de release formaté conforme Scene (ex: "Test-Book-TESTGROUP-20250124").

        Raises:
            ValueError: Si date n'est pas au format YYYYMMDD.
            ValueError: Si groupe est vide.
        """
        if not group:
            raise ValueError("Le nom du groupe ne peut pas être vide")

        if not date or len(date) != 8 or not date.isdigit():
            raise ValueError(f"Date invalide: '{date}'. Format attendu: YYYYMMDD")

        # Normaliser titre : trim, remplacer espaces par tirets, supprimer caractères spéciaux
        normalized_title = title.strip()
        normalized_title = normalized_title.replace(" ", "-")
        normalized_title = self.ALLOWED_CHARS_PATTERN.sub("", normalized_title)
        normalized_title = re.sub(r"-+", "-", normalized_title)  # Remplacer tirets multiples par un seul
        normalized_title = normalized_title.strip("-")  # Supprimer tirets début/fin

        # Normaliser groupe : uppercase, supprimer caractères spéciaux
        normalized_group = group.strip().upper()
        normalized_group = self.ALLOWED_CHARS_PATTERN.sub("", normalized_group)

        # Construire nom final
        release_name = f"{normalized_title}-{normalized_group}-{date}"

        # Tronquer si nécessaire pour respecter limite 255 caractères
        if len(release_name) > self.MAX_RELEASE_NAME_LENGTH:
            # Tronquer le titre pour laisser place au groupe et à la date
            title_max_length = (
                self.MAX_RELEASE_NAME_LENGTH
                - len(normalized_group)
                - len(date)
                - 2  # 2 tirets séparateurs
            )
            normalized_title = normalized_title[:title_max_length]
            release_name = f"{normalized_title}-{normalized_group}-{date}"

        return release_name

    def format_directory_name(self, release_name: str) -> str:
        """Formate le nom d'un dossier pour une release.

        Le nom du dossier est généralement identique au nom de la release,
        mais peut être ajusté selon les règles Scene spécifiques.

        Complexité : O(1) - Retour direct sans traitement complexe.

        Args:
            release_name: Nom de la release formaté.

        Returns:
            Nom du dossier formaté (identique au nom de release par défaut).
        """
        return release_name.strip()

    def format_filename(
        self, base_name: str, extension: str = ""
    ) -> str:
        """Formate le nom d'un fichier pour une release.

        Génère un nom de fichier en combinant le nom de base avec l'extension.
        L'extension doit commencer par un point si fournie.

        Complexité : O(1) - Concaténation simple.

        Args:
            base_name: Nom de base du fichier (sans extension).
            extension: Extension du fichier (ex: ".epub", ".pdf").
                     Peut être vide pour fichiers sans extension.

        Returns:
            Nom de fichier complet avec extension.

        Example:
            >>> service = ReleaseFormatterService()
            >>> service.format_filename("Test-Book-TESTGROUP-20250124", ".epub")
            "Test-Book-TESTGROUP-20250124.epub"
        """
        if extension and not extension.startswith("."):
            extension = f".{extension}"

        return f"{base_name}{extension}"

    def normalize_metadata(self, metadata: dict[str, Any]) -> dict[str, Any]:
        """Normalise les métadonnées pour export.

        Cette méthode nettoie et normalise les métadonnées :
        - Trim des chaînes de caractères
        - Conversion types (str → int pour années, etc.)
        - Suppression valeurs None vides
        - Normalisation encodage UTF-8

        Algorithme :
        1. Parcourir toutes les clés de metadata
        2. Pour chaque valeur :
           - Trim si chaîne de caractères
           - Conversion type si possible (ex: "2025" → 2025)
           - Suppression si None ou chaîne vide
        3. Retourner dictionnaire normalisé

        Complexité : O(n) où n est le nombre de métadonnées (généralement ≤ 20).

        Args:
            metadata: Dictionnaire de métadonnées brutes.

        Returns:
            Dictionnaire de métadonnées normalisées.
        """
        normalized: dict[str, Any] = {}

        for key, value in metadata.items():
            if value is None:
                continue

            # Normaliser chaînes de caractères
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    continue

                # Tentative conversion en int pour certaines clés
                if key in ["year", "pages", "size"]:
                    try:
                        value = int(value)
                    except ValueError:
                        pass  # Garder comme chaîne si conversion échoue

            # Normaliser autres types
            elif isinstance(value, int | float):
                # Garder tel quel
                pass
            elif isinstance(value, list):
                # Normaliser chaque élément de la liste
                normalized_list = [
                    item.strip() if isinstance(item, str) else item
                    for item in value
                    if item is not None
                ]
                if normalized_list:
                    value = normalized_list
                else:
                    continue

            normalized[key] = value

        return normalized

