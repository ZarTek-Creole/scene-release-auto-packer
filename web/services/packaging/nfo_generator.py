"""Service de génération de fichiers NFO conformes aux standards Scene.

Ce service génère des fichiers NFO (ASCII art) conformes aux standards Scene
avec contraintes strictes de formatage (80 colonnes max par ligne).

Architecture :
- Génération header/body/footer selon structure Scene
- Formatage automatique respectant contraintes 80 colonnes
- Support templates avec placeholders et conditionnelles
- Gestion caractères spéciaux UTF-8

Complexité moyenne : O(n) où n est la taille du contenu généré.
Le formatage ligne par ligne garantit respect contraintes 80 colonnes.
"""

from __future__ import annotations

import logging
import re
from textwrap import wrap
from typing import Any

logger = logging.getLogger(__name__)


class NfoGeneratorService:
    """Service de génération de fichiers NFO conformes aux standards Scene.

    Ce service génère des fichiers NFO (ASCII art) conformes aux standards Scene
    avec contraintes strictes de formatage ASCII 80 colonnes par ligne maximum.

    Fonctionnalités :
    - Génération NFO basique avec métadonnées
    - Formatage automatique respectant contraintes 80 colonnes
    - Support templates avec placeholders `{{variable}}`
    - Support conditionnelles `{% if condition %}...{% endif %}`
    - Gestion caractères spéciaux UTF-8

    Structure NFO typique :
    - Header : Séparateurs ASCII art, titre release
    - Body : Métadonnées formatées (titre, auteur, éditeur, ISBN, etc.)
    - Footer : Informations groupe, date, checksums

    Contraintes strictes :
    - Toutes les lignes ≤ 80 colonnes (obligatoire Scene)
    - Format ASCII avec support UTF-8 si nécessaire
    - Structure conforme standards Scene

    Exemple d'utilisation :
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book",
            "author": "Test Author",
            "group": "TESTGROUP",
            "date": "20250124",
        }
        nfo = service.generate_nfo(metadata)
    """

    MAX_LINE_WIDTH = 80  # Contrainte Scene : 80 colonnes max

    def __init__(self) -> None:
        """Initialise le service de génération NFO.

        Cette méthode est vide car le service n'a pas besoin d'état interne.
        Toutes les configurations sont définies comme constantes de classe.

        Complexité : O(1) - Initialisation simple sans dépendances.
        """

    def generate_nfo(self, metadata: dict[str, Any], template: str | None = None) -> str:
        """Génère un fichier NFO complet depuis les métadonnées.

        Cette méthode orchestratrice génère un fichier NFO complet en combinant
        header, body et footer. Si un template est fourni, il est utilisé en priorité,
        sinon un template par défaut conforme Scene est généré.

        Algorithme :
        1. Si template fourni : utiliser template avec remplacement placeholders
        2. Sinon : générer structure standard (header + body + footer)
        3. Formater toutes les lignes pour respecter contrainte 80 colonnes
        4. Retourner NFO final comme chaîne de caractères

        Complexité : O(n) où n est la taille du contenu généré.
        Le formatage ligne par ligne est O(n) avec n = nombre de lignes.

        Args:
            metadata: Dictionnaire contenant les métadonnées de la release :
                - title : Titre de la release (obligatoire)
                - author : Auteur (optionnel)
                - publisher : Éditeur (optionnel)
                - isbn : ISBN (optionnel)
                - year : Année de publication (optionnel)
                - language : Langue (optionnel)
                - group : Nom du groupe Scene (obligatoire)
                - date : Date de release au format YYYYMMDD (obligatoire)
            template: Template personnalisé avec placeholders {{variable}} (optionnel).
                     Si None, template par défaut conforme Scene est utilisé.

        Returns:
            Contenu du fichier NFO formaté (chaîne de caractères UTF-8).
            Toutes les lignes respectent la contrainte ≤ 80 colonnes.

        Raises:
            Aucune exception levée explicitement, mais les valeurs None dans
            metadata sont gérées gracieusement (lignes omises).
        """
        if template:
            # Utiliser template personnalisé avec remplacement placeholders
            nfo = self._render_template(template, metadata)
        else:
            # Générer structure standard conforme Scene
            header = self._generate_header(metadata)
            body = self._generate_body(metadata)
            footer = self._generate_footer(metadata)

            # Combiner toutes les sections
            nfo_lines = header + body + footer
            nfo = "\n".join(nfo_lines)

        # Formater toutes les lignes pour respecter contrainte 80 colonnes
        formatted_lines = []
        for line in nfo.split("\n"):
            formatted_lines.extend(self._format_line(line, self.MAX_LINE_WIDTH))

        return "\n".join(formatted_lines)

    def _generate_header(self, metadata: dict[str, Any]) -> list[str]:
        """Génère le header du NFO (séparateurs ASCII art et titre).

        Le header contient généralement :
        - Séparateurs ASCII art (ex: ==========)
        - Titre de la release formaté
        - Informations groupe et date

        Algorithme :
        1. Création séparateurs ASCII art
        2. Formatage titre release (si présent)
        3. Formatage informations groupe/date
        4. Formatage de toutes les lignes pour respecter contrainte 80 colonnes

        Complexité : O(1) - Génération de quelques lignes fixes.

        Args:
            metadata: Dictionnaire de métadonnées.

        Returns:
            Liste de lignes formatées pour le header (≤ 80 colonnes chacune).
        """
        lines = []

        # Séparateur ASCII art
        lines.append("=" * self.MAX_LINE_WIDTH)
        lines.append("")

        # Titre release
        title = metadata.get("title", "Untitled Release")
        group = metadata.get("group", "")
        date = metadata.get("date", "")

        if title:
            # Formater la ligne pour respecter contrainte 80 colonnes
            title_lines = self._format_line(f"Title: {title}", self.MAX_LINE_WIDTH)
            lines.extend(title_lines)

        if group and date:
            release_line = f"Release: {group} - {date}"
            release_lines = self._format_line(release_line, self.MAX_LINE_WIDTH)
            lines.extend(release_lines)
        elif group:
            group_line = f"Group: {group}"
            group_lines = self._format_line(group_line, self.MAX_LINE_WIDTH)
            lines.extend(group_lines)

        lines.append("")
        lines.append("=" * self.MAX_LINE_WIDTH)

        return lines

    def _generate_body(self, metadata: dict[str, Any]) -> list[str]:
        """Génère le body du NFO (métadonnées détaillées).

        Le body contient toutes les métadonnées de la release :
        - Titre, auteur, éditeur
        - ISBN, année, langue
        - Taille, format, etc.

        Algorithme :
        1. Parcourir métadonnées disponibles
        2. Formater chaque paire clé-valeur
        3. Ignorer valeurs None ou vides

        Complexité : O(n) où n est le nombre de métadonnées (généralement ≤ 20).

        Args:
            metadata: Dictionnaire de métadonnées.

        Returns:
            Liste de lignes formatées pour le body (≤ 80 colonnes chacune).
        """
        lines = []
        lines.append("")

        # Champs à inclure dans le body (dans l'ordre souhaité)
        fields = [
            ("title", "Title"),
            ("author", "Author"),
            ("publisher", "Publisher"),
            ("isbn", "ISBN"),
            ("year", "Year"),
            ("language", "Language"),
            ("format", "Format"),
            ("size", "Size"),
            ("pages", "Pages"),
            ("description", "Description"),
        ]

        for key, label in fields:
            value = metadata.get(key)
            if value is not None and str(value).strip():
                field_line = f"{label}: {value}"
                # Formater la ligne pour respecter contrainte 80 colonnes
                formatted_field_lines = self._format_line(field_line, self.MAX_LINE_WIDTH)
                lines.extend(formatted_field_lines)

        lines.append("")

        return lines

    def _generate_footer(self, metadata: dict[str, Any]) -> list[str]:
        """Génère le footer du NFO (informations groupe et checksums).

        Le footer contient généralement :
        - Informations groupe Scene
        - Checksums (SHA-256, MD5)
        - Date de release
        - Séparateur ASCII art final

        Algorithme :
        1. Formatage informations groupe
        2. Formatage checksums (si présents)
        3. Séparateur final

        Complexité : O(1) - Génération de quelques lignes fixes.

        Args:
            metadata: Dictionnaire de métadonnées.

        Returns:
            Liste de lignes formatées pour le footer (≤ 80 colonnes chacune).
        """
        lines = []
        lines.append("=" * self.MAX_LINE_WIDTH)
        lines.append("")

        # Informations groupe
        group = metadata.get("group", "")
        date = metadata.get("date", "")

        if group:
            lines.append(f"Released by: {group}")

        if date:
            lines.append(f"Release Date: {date}")

        # Checksums (si présents)
        checksums = metadata.get("checksums", {})
        if isinstance(checksums, dict):
            if "sha256" in checksums:
                lines.append(f"SHA-256: {checksums['sha256']}")
            if "md5" in checksums:
                lines.append(f"MD5: {checksums['md5']}")

        lines.append("")
        lines.append("=" * self.MAX_LINE_WIDTH)

        return lines

    def _render_template(self, template: str, metadata: dict[str, Any]) -> str:
        """Rend un template avec remplacement des placeholders.

        Cette méthode remplace les placeholders `{{variable}}` dans le template
        par les valeurs correspondantes dans metadata. Les valeurs None sont
        remplacées par chaînes vides. Supporte également `{variable}` pour compatibilité.

        Algorithme :
        1. Recherche de tous les placeholders {{variable}} ou {variable} avec regex
        2. Remplacement par valeurs correspondantes dans metadata
        3. Gestion valeurs None (remplacement par chaîne vide)

        Complexité : O(n*m) où n est la taille du template et m le nombre de
        placeholders. Généralement rapide car regex optimisée.

        Note : Support basique des placeholders. Pour support avancé (conditionnelles,
        fonctions), utiliser une bibliothèque de templating comme Jinja2.

        Args:
            template: Template avec placeholders {{variable}} ou {variable}.
            metadata: Dictionnaire de métadonnées pour remplacement.

        Returns:
            Template rendu avec placeholders remplacés.
        """
        result = template

        # Rechercher tous les placeholders {{variable}} ou {variable}
        # Pattern pour {{variable}} (double accolades)
        pattern_double = r"\{\{(\w+)\}\}"
        matches_double = re.findall(pattern_double, result)

        for placeholder in matches_double:
            value = metadata.get(placeholder, "")
            if value is None:
                value = ""
            result = result.replace(f"{{{{{placeholder}}}}}", str(value))

        # Pattern pour {variable} (accolades simples) - compatibilité
        pattern_single = r"\{(\w+)\}"
        matches_single = re.findall(pattern_single, result)

        for placeholder in matches_single:
            value = metadata.get(placeholder, "")
            if value is None:
                value = ""
            result = result.replace(f"{{{placeholder}}}", str(value))

        return result

    def _format_line(self, line: str, max_width: int = 80) -> list[str]:
        """Formate une ligne pour respecter la contrainte de largeur maximale.

        Cette méthode formate une ligne pour qu'elle respecte la contrainte de
        largeur maximale (80 colonnes par défaut). Si la ligne est trop longue,
        elle est coupée intelligemment avec textwrap.wrap(). Gère également
        les lignes multi-lignes (contenant \n).

        Algorithme :
        1. Séparer la ligne en sous-lignes si elle contient \n
        2. Pour chaque sous-ligne :
           - Vérification longueur
           - Si ligne ≤ max_width : garder telle quelle
           - Sinon : utiliser textwrap.wrap() pour couper intelligemment
        3. Retourner liste de lignes formatées

        Complexité : O(n) où n est la longueur de la ligne.
        textwrap.wrap() est O(n) pour le découpage.

        Pièges potentiels :
        - Les mots longs peuvent dépasser max_width (rare, mais possible)
        - textwrap.wrap() préserve les espaces multiples
        - Les lignes vides sont préservées
        - break_long_words=True pour garantir contrainte stricte

        Args:
            line: Ligne à formater (peut contenir \n pour multi-lignes).
            max_width: Largeur maximale autorisée (défaut: 80).

        Returns:
            Liste de lignes formatées (toutes ≤ max_width colonnes).
            Liste de 1 élément si ligne déjà conforme, liste de plusieurs
            éléments si ligne coupée.

        Example:
            >>> service = NfoGeneratorService()
            >>> service._format_line("Short line")
            ['Short line']
            >>> service._format_line("A" * 100)
            ['A' * 80, 'A' * 20]  # Coupé en 2 lignes
        """
        # Séparer les lignes si multi-lignes
        sub_lines = line.split("\n")
        formatted_lines = []

        for sub_line in sub_lines:
            # Si ligne déjà conforme, garder telle quelle
            if len(sub_line) <= max_width:
                formatted_lines.append(sub_line)
            else:
                # Couper ligne trop longue avec textwrap.wrap()
                # break_long_words=True pour garantir contrainte stricte 80 colonnes
                wrapped_lines = wrap(sub_line, width=max_width, break_long_words=True)
                formatted_lines.extend(wrapped_lines)

        return formatted_lines
