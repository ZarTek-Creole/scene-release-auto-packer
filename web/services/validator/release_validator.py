"""Service de validation complète d'une release selon les règles Scene.

Ce service valide une release complète selon les règles Scene extraites depuis
scenerules.org. Il vérifie le nommage, les métadonnées, la structure et retourne
une liste d'erreurs et d'avertissements.

Architecture :
- Validation nommage selon patterns regex des règles
- Validation métadonnées (champs requis, formats)
- Validation structure (fichiers requis, formats acceptés)
- Retour structuré avec erreurs et avertissements

Complexité moyenne : O(n) où n est le nombre de validations à effectuer.
Les regex sont optimisées pour éviter backtracking excessif.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ReleaseValidatorService:
    """Service de validation complète d'une release selon les règles Scene.

    Ce service implémente la logique de validation complète d'une release selon
    les règles Scene extraites depuis scenerules.org via RuleParserService.
    Il vérifie tous les aspects (nommage, métadonnées, structure) et retourne
    une liste structurée d'erreurs et d'avertissements.

    Fonctionnalités :
    - Validation nommage selon patterns regex des règles
    - Validation métadonnées (champs requis, formats)
    - Validation structure (fichiers requis, formats acceptés)
    - Retour structuré avec erreurs et avertissements clairs

    Types de validations :
    - Nommage : Pattern regex, longueur, caractères autorisés
    - Métadonnées : Champs requis, formats (ISBN, dates, etc.)
    - Structure : Fichiers requis présents, formats acceptés

    Exemple d'utilisation :
        service = ReleaseValidatorService()
        release_data = {
            "name": "Test-Book-TESTGROUP-20250124",
            "group": "TESTGROUP",
            "release_type": "EBOOK",
            "metadata": {...},
            "files": [...],
        }
        rule_spec = {...}  # Depuis RuleParserService
        result = service.validate_release(release_data, rule_spec)
        if not result["valid"]:
            print("Erreurs:", result["errors"])
    """

    def __init__(self) -> None:
        """Initialise le service de validation.

        Cette méthode est vide car le service n'a pas besoin d'état interne.
        Toutes les validations sont effectuées avec les données fournies.

        Complexité : O(1) - Initialisation simple sans dépendances.
        """

    def validate_release(
        self, release_data: dict[str, Any], rule_spec: dict[str, Any]
    ) -> dict[str, Any]:
        """Valide une release complète selon les règles Scene.

        Cette méthode orchestratrice effectue toutes les validations nécessaires
        sur une release : nommage, métadonnées, structure. Elle retourne un résultat
        structuré avec statut de validation, liste d'erreurs et avertissements.

        Algorithme :
        1. Validation nommage (si règle contient pattern)
        2. Validation métadonnées (si règle contient contraintes)
        3. Validation structure (si règle contient fichiers requis)
        4. Collecte de toutes les erreurs et avertissements
        5. Retour résultat structuré

        Complexité : O(n) où n est le nombre de validations à effectuer.
        Chaque validation est O(1) ou O(m) où m est la taille des données.

        Args:
            release_data: Dictionnaire contenant les données de la release :
                - name : Nom de la release (obligatoire)
                - group : Nom du groupe Scene (obligatoire)
                - release_type : Type de release ('TV', 'EBOOK', 'DOCS')
                - metadata : Dictionnaire de métadonnées (optionnel)
                - files : Liste des noms de fichiers (optionnel)
            rule_spec: Dictionnaire contenant les spécifications de la règle Scene :
                - naming : Dictionnaire avec pattern regex, contraintes
                - required_fields : Liste des champs métadonnées requis
                - required_files : Liste des types de fichiers requis
                - file_formats : Liste des formats de fichiers acceptés
                - metadata_formats : Dictionnaire de patterns regex pour métadonnées

        Returns:
            Dictionnaire contenant :
                - valid : True si la release est valide, False sinon
                - errors : Liste des erreurs (chaînes de caractères)
                - warnings : Liste des avertissements (chaînes de caractères)

        Raises:
            Aucune exception levée explicitement. Les erreurs sont collectées
            et retournées dans le dictionnaire de résultat.
        """
        errors: list[str] = []
        warnings: list[str] = []

        # Validation nommage
        if "naming" in rule_spec:
            naming_errors = self.validate_naming(release_data.get("name", ""), rule_spec["naming"])
            errors.extend(naming_errors)

        # Validation métadonnées
        if "required_fields" in rule_spec or "metadata_formats" in rule_spec:
            metadata = release_data.get("metadata", {})
            metadata_errors = self.validate_metadata(metadata, rule_spec)
            errors.extend(metadata_errors)

        # Validation structure
        if "required_files" in rule_spec or "file_formats" in rule_spec:
            files = release_data.get("files", [])
            structure_errors = self.validate_structure(files, rule_spec)
            errors.extend(structure_errors)

        # Vérifier champs recommandés (avertissements, pas erreurs)
        if "recommended_fields" in rule_spec:
            metadata = release_data.get("metadata", {})
            recommended_fields = rule_spec["recommended_fields"]
            for field in recommended_fields:
                if field not in metadata or not metadata.get(field):
                    warnings.append(f"Champ recommandé manquant: {field}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    def validate_naming(self, release_name: str, naming_spec: dict[str, Any]) -> list[str]:
        """Valide le nommage d'une release selon les règles Scene.

        Cette méthode valide le nom d'une release selon le pattern regex et
        les contraintes définies dans la règle Scene (longueur, caractères autorisés).

        Algorithme :
        1. Vérification pattern regex si fourni
        2. Vérification longueur max si fournie
        3. Vérification caractères autorisés si fourni

        Complexité : O(n) où n est la longueur du nom (regex matching).

        Args:
            release_name: Nom de la release à valider.
            naming_spec: Dictionnaire contenant les spécifications de nommage :
                - pattern : Pattern regex pour validation (obligatoire)
                - max_length : Longueur maximale autorisée (optionnel)
                - allowed_chars : Pattern regex pour caractères autorisés (optionnel)

        Returns:
            Liste des erreurs de validation (vide si nommage valide).
        """
        errors: list[str] = []

        if not release_name:
            errors.append("Le nom de la release ne peut pas être vide")
            return errors

        # Validation pattern regex
        if "pattern" in naming_spec:
            pattern = naming_spec["pattern"]
            try:
                if not re.match(pattern, release_name):
                    errors.append(
                        f"Le nom '{release_name}' ne correspond pas au pattern requis: {pattern}"
                    )
            except re.error as e:
                errors.append(f"Pattern regex invalide dans la règle: {e}")

        # Validation longueur max
        if "max_length" in naming_spec:
            max_length = naming_spec["max_length"]
            if len(release_name) > max_length:
                errors.append(
                    f"Le nom '{release_name}' dépasse la longueur maximale de {max_length} caractères"
                )

        # Validation caractères autorisés
        if "allowed_chars" in naming_spec:
            allowed_chars_pattern = naming_spec["allowed_chars"]
            if not re.match(allowed_chars_pattern, release_name):
                errors.append(f"Le nom '{release_name}' contient des caractères non autorisés")

        return errors

    def validate_metadata(self, metadata: dict[str, Any], rule_spec: dict[str, Any]) -> list[str]:
        """Valide les métadonnées d'une release selon les règles Scene.

        Cette méthode valide les métadonnées en vérifiant :
        - Présence des champs requis
        - Formats des champs (regex patterns)
        - Types de données attendus

        Algorithme :
        1. Vérification champs requis
        2. Vérification formats avec regex si fournis
        3. Collecte de toutes les erreurs

        Complexité : O(n) où n est le nombre de champs à valider.

        Args:
            metadata: Dictionnaire de métadonnées à valider.
            rule_spec: Dictionnaire contenant les spécifications de validation :
                - required_fields : Liste des champs requis (optionnel)
                - metadata_formats : Dictionnaire de patterns regex pour formats (optionnel)

        Returns:
            Liste des erreurs de validation (vide si métadonnées valides).
        """
        errors: list[str] = []

        # Validation champs requis
        if "required_fields" in rule_spec:
            required_fields = rule_spec["required_fields"]
            for field in required_fields:
                if field not in metadata or not metadata.get(field):
                    errors.append(f"Champ requis manquant: {field}")

        # Validation formats
        if "metadata_formats" in rule_spec:
            metadata_formats = rule_spec["metadata_formats"]
            for field, pattern in metadata_formats.items():
                if field in metadata and metadata[field]:
                    value = str(metadata[field])
                    if not re.match(pattern, value):
                        errors.append(
                            f"Format invalide pour '{field}': '{value}' ne correspond pas au pattern '{pattern}'"
                        )

        return errors

    def validate_structure(self, files: list[str | Path], rule_spec: dict[str, Any]) -> list[str]:
        """Valide la structure d'une release (fichiers présents et formats).

        Cette méthode valide la structure en vérifiant :
        - Présence des fichiers requis selon la règle
        - Formats des fichiers présents (extensions autorisées)

        Algorithme :
        1. Extraction extensions des fichiers fournis
        2. Vérification présence fichiers requis
        3. Vérification formats acceptés

        Complexité : O(n*m) où n est le nombre de fichiers et m le nombre
        de formats requis (généralement petit).

        Args:
            files: Liste des noms de fichiers ou chemins Path.
            rule_spec: Dictionnaire contenant les spécifications de structure :
                - required_files : Liste des types de fichiers requis (ex: ["nfo", "epub"])
                - file_formats : Liste des extensions acceptées (ex: [".epub", ".pdf"])

        Returns:
            Liste des erreurs de validation (vide si structure valide).
        """
        errors: list[str] = []

        # Convertir fichiers en chemins Path et extraire extensions
        file_paths = [Path(f) if isinstance(f, str) else f for f in files]
        file_extensions = [path.suffix.lower() for path in file_paths]
        file_types = [
            path.stem.split(".")[-1].lower() for path in file_paths
        ]  # Pour fichiers comme "file.nfo"

        # Validation fichiers requis
        if "required_files" in rule_spec:
            required_files = rule_spec["required_files"]
            for required_file in required_files:
                # Normaliser extension (avec ou sans point)
                normalized_required = required_file.lower()
                if not normalized_required.startswith("."):
                    normalized_required = f".{normalized_required}"

                # Vérifier présence fichier requis
                found = False
                for ext in file_extensions:
                    if ext == normalized_required:
                        found = True
                        break

                # Vérifier aussi par type (ex: "nfo" dans required_files)
                if not found and required_file.lower() in file_types:
                    found = True

                if not found:
                    errors.append(f"Fichier requis manquant: {required_file}")

        # Validation formats acceptés
        if "file_formats" in rule_spec:
            accepted_formats = rule_spec["file_formats"]
            # Normaliser formats (avec point)
            normalized_formats = [
                f.lower() if f.startswith(".") else f".{f.lower()}" for f in accepted_formats
            ]

            for file_path in file_paths:
                ext = file_path.suffix.lower()
                if ext and ext not in normalized_formats:
                    errors.append(
                        f"Format de fichier non accepté: {ext} (formats acceptés: {', '.join(accepted_formats)})"
                    )

        return errors
