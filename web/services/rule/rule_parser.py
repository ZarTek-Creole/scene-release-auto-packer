"""Service de parsing et validation des règles Scene.

Ce service parse les règles Scene (notamment [2022] eBOOK) depuis scenerules.org
et extrait des spécifications structurées pour la validation du packaging.

Algorithme général :
1. Extraction des sections clés (OTHER, DIRNAMING, PACKAGING) via regex
2. Parsing des patterns de nommage et contraintes
3. Validation de conformité d'une release aux règles extraites

Complexité moyenne : O(n) où n est la taille du contenu de la règle.
Les regex utilisées sont optimisées pour éviter les backtracking excessifs.
"""

from __future__ import annotations

import re
from typing import Any


class RuleParserService:
    """Service de parsing et extraction des spécifications depuis les règles Scene.

    Ce service implémente la logique de parsing des règles Scene disponibles sur
    scenerules.org. Il extrait les patterns de nommage, les contraintes de packaging,
    et permet de valider la conformité d'une release aux règles.

    Les règles Scene sont généralement au format NFO (texte ASCII art) avec des
    sections structurées comme OTHER, DIRNAMING, PACKAGING, etc.

    Exemple d'utilisation :
        parser = RuleParserService()
        rule_spec = parser.parse_ebook_rule_2022(rule_content)
        formats = rule_spec["file_formats"]  # [".pdf", ".epub", ...]
    """

    def parse_ebook_rule_2022(self, rule_content: str) -> dict[str, Any]:
        """Parse complètement la règle [2022] eBOOK et extrait toutes les spécifications.

        Cette méthode orchestratrice appelle les méthodes d'extraction spécialisées
        pour chaque section de la règle. Elle construit un dictionnaire structuré
        contenant toutes les informations nécessaires pour valider une release.

        Complexité : O(n) où n est la taille du contenu de la règle.
        Chaque méthode d'extraction parcourt le contenu une fois.

        Args:
            rule_content: Contenu texte brut de la règle [2022] eBOOK (format NFO).

        Returns:
            Dictionnaire contenant les spécifications structurées :
            - file_formats: Liste des formats de fichiers acceptés (ex: [".pdf", ".epub"])
            - naming: Structure du format de nommage (composants, séparateurs, longueur max)
            - required_files: Liste des types de fichiers requis (ex: ["zip", "diz", "nfo"])
            - packaging: Règles de packaging (tailles ZIP autorisées, contraintes NFO/DIZ)

        Raises:
            Aucune exception levée explicitement, mais les méthodes appelées peuvent
            utiliser des valeurs par défaut si certaines sections ne sont pas trouvées.
        """
        return {
            "file_formats": self.extract_file_formats(rule_content),
            "naming": self.extract_naming_format(rule_content),
            "required_files": self.extract_required_files(rule_content),
            "packaging": self.extract_packaging_rules(rule_content),
        }

    def extract_file_formats(self, rule_content: str) -> list[str]:
        """Extrait les formats de fichiers acceptés depuis la section OTHER de la règle.

        Cette méthode utilise une regex pour trouver la section OTHER qui liste les formats
        acceptés dans la règle Scene. Elle détecte ensuite chaque format mentionné (PDF, EPUB,
        CBZ, Kindle, MOBIPOCKET) et les normalise en extensions de fichiers avec point.

        Algorithme :
        1. Recherche de la section OTHER avec regex (non-greedy pour éviter de capturer trop)
        2. Pour chaque format connu, recherche dans le texte extrait
        3. Normalisation en extensions avec point (ex: "PDF" → ".pdf")
        4. Si aucun format trouvé, utilisation des valeurs par défaut de [2022] eBOOK

        Complexité : O(n) où n est la taille du contenu, avec plusieurs recherches regex
        successives. La complexité est acceptable car le nombre de formats est limité.

        Patterns regex utilisés :
        - ``\\bPDF\\b`` : Mot complet "PDF" (word boundary pour éviter "PDFX")
        - ``\\.azw\\b|Kindle.*\\.azw`` : Extension .azw ou mention dans contexte Kindle

        Pièges potentiels :
        - Les règles peuvent varier dans la casse (d'où IGNORECASE)
        - Certains formats peuvent être mentionnés avec ou sans contexte (ex: "Kindle (.azw)")
        - Si la section OTHER n'existe pas, on utilise les valeurs par défaut

        Args:
            rule_content: Contenu texte brut de la règle Scene.

        Returns:
            Liste triée et dédupliquée des extensions de fichiers acceptées
            (lowercase, avec point, ex: [".epub", ".pdf", ".mobi"]).
        """
        formats: list[str] = []

        # Recherche de la section OTHER avec regex multi-ligne
        # Pattern expliqué :
        # - `(?:^|\n)` : Début de ligne ou nouvelle ligne
        # - `\s*OTHER\s*[:;]?` : Mot "OTHER" entouré d'espaces optionnels, suivi de : ou ;
        # - `(.*?)` : Capture non-greedy du contenu jusqu'au prochain séparateur
        # - `(?=\n\n|\n[A-Z]{2,}|$)` : Lookahead positif : arrête avant double saut de ligne,
        #   avant une section en majuscules (2+ lettres), ou fin de chaîne
        other_pattern = r"(?:^|\n)\s*OTHER\s*[:;]?\s*(.*?)(?=\n\n|\n[A-Z]{2,}|$)"
        match = re.search(other_pattern, rule_content, re.IGNORECASE | re.DOTALL | re.MULTILINE)

        if match:
            formats_text = match.group(1)

            # Extraction de chaque format avec recherche de mot complet (word boundary)
            # pour éviter les faux positifs (ex: "PDFX" ne doit pas matcher "PDF")
            if re.search(r"\bPDF\b", formats_text, re.IGNORECASE):
                formats.append(".pdf")
            if re.search(r"\bEPUB\b", formats_text, re.IGNORECASE):
                formats.append(".epub")
            if re.search(r"\bCBZ\b", formats_text, re.IGNORECASE):
                formats.append(".cbz")

            # Formats Kindle : recherche de l'extension ou du contexte "Kindle"
            # Pattern flexible pour gérer "Kindle (.azw, .kf8)" ou simplement ".azw"
            if re.search(r"\.azw\b|Kindle.*\.azw", formats_text, re.IGNORECASE):
                formats.append(".azw")
            if re.search(r"\.kf8\b|Kindle.*\.kf8", formats_text, re.IGNORECASE):
                formats.append(".kf8")

            # Formats MOBIPOCKET : même logique que Kindle
            if re.search(r"\.prc\b|MOBIPOCKET.*\.prc", formats_text, re.IGNORECASE):
                formats.append(".prc")
            if re.search(r"\.mobi\b|MOBIPOCKET.*\.mobi", formats_text, re.IGNORECASE):
                formats.append(".mobi")

        # Valeurs par défaut si aucun format trouvé (basées sur [2022] eBOOK)
        # Ces valeurs correspondent aux formats standard acceptés par la Scene
        if not formats:
            formats = [".pdf", ".epub", ".cbz", ".azw", ".kf8", ".prc", ".mobi"]

        # Tri et déduplication pour garantir un résultat cohérent
        return sorted(set(formats))

    def extract_naming_format(self, rule_content: str) -> dict[str, Any]:
        """Extrait le format de nommage depuis la section DIRNAMING de la règle.

        Cette méthode parse la section DIRNAMING qui définit la structure attendue
        pour les noms de répertoires des releases Scene. Le format standard est :
        GroupName-Author-Title-Format-Language-Year-ISBN-eBook

        Algorithme :
        1. Recherche de la section DIRNAMING avec regex
        2. Extraction du pattern de nommage (séquence de mots séparés par tirets)
        3. Découpage du pattern en composants individuels
        4. Construction d'un dictionnaire avec métadonnées de chaque composant

        Complexité : O(n) où n est la taille du contenu.
        Le split et la construction du dictionnaire sont O(k) où k est le nombre de composants.

        Structure de retour :
        - format : Chaîne complète du format (ex: "GroupName-Author-Title-...")
        - separators : Liste des séparateurs utilisés (généralement ["-"])
        - components : Dictionnaire avec métadonnées de chaque composant
        - max_length : Longueur maximale autorisée (243 caractères selon règles Scene)

        Note importante : La longueur maximale de 243 caractères est une contrainte
        stricte des règles Scene pour les noms de répertoires. Cette limite évite
        les problèmes avec les systèmes de fichiers FAT32 et NTFS.

        Args:
            rule_content: Contenu texte brut de la règle Scene.

        Returns:
            Dictionnaire contenant la structure du format de nommage :
            - format : Chaîne du format complet
            - separators : Liste des séparateurs
            - components : Dictionnaire des composants avec leurs contraintes
            - max_length : Longueur maximale autorisée
        """
        # Recherche de la section DIRNAMING
        # Pattern similaire à OTHER : recherche de "DIRNAMING" suivi du contenu
        dirnaming_pattern = r"DIRNAMING\s*[:;]?\s*(.*?)(?=\n\n|\n[A-Z]|$)"
        match = re.search(dirnaming_pattern, rule_content, re.IGNORECASE | re.DOTALL)

        if match:
            naming_text = match.group(1)
            # Extraction du pattern de nommage (séquence de mots séparés par tirets)
            # Pattern regex : ``([A-Za-z]+(?:-[A-Za-z]+)*)``
            # - ``[A-Za-z]+`` : Premier mot (lettres uniquement)
            # - ``(?:-[A-Za-z]+)*`` : Zéro ou plusieurs groupes de tiret + mot
            # Cela capture des patterns comme "GroupName-Author-Title-Format"
            # Note : Le pattern ne capture que les lettres et tirets, excluant chiffres et caractères spéciaux
            format_match = re.search(r"([A-Za-z]+(?:-[A-Za-z]+)+)", naming_text)
            if format_match:
                format_str = format_match.group(1)
                # Découpage en composants individuels
                components = format_str.split("-")

                # Construction du dictionnaire avec tous les composants marqués comme requis
                # Note : Dans une implémentation complète, on pourrait parser des annotations
                # dans la règle pour savoir quels composants sont optionnels
                return {
                    "format": format_str,
                    "separators": ["-"],
                    "components": {
                        comp: {"required": True, "format": "string"} for comp in components
                    },
                    "max_length": 243,  # Contrainte Scene : dirname max 243 caractères
                }

        # Format par défaut basé sur [2022] eBOOK si section DIRNAMING non trouvée
        # Ce format est le standard utilisé par la Scene pour les releases eBook
        return {
            "format": "GroupName-Author-Title-Format-Language-Year-ISBN-eBook",
            "separators": ["-"],
            "components": {
                "GroupName": {"required": True, "format": "SceneGroup"},
                "Author": {"required": True, "format": "AuthorName"},
                "Title": {"required": True, "format": "BookTitle"},
                "Format": {
                    "required": True,
                    "values": ["EPUB", "PDF", "CBZ", "MOBI", "AZW", "KF8", "PRC"],
                },
                "Language": {"required": False, "format": "ISO639"},
                "Year": {"required": True, "format": "YYYY"},
                "ISBN": {"required": False, "format": "ISBN13"},
                "eBook": {"required": True, "fixed": "eBook"},
            },
            "max_length": 243,
        }

    def extract_required_files(self, rule_content: str) -> list[str]:
        """Extrait la liste des fichiers obligatoires depuis la section PACKAGING.

        Cette méthode parse la section PACKAGING pour identifier les fichiers qui
        doivent être présents dans chaque release Scene. Les fichiers standards sont :
        - ZIP : Archive principale contenant les fichiers eBook
        - DIZ : Fichier de description (file_id.diz)
        - NFO : Fichier d'information Scene (généralement au format ASCII art)
        - RAR : Archive alternative (optionnelle généralement)

        Algorithme :
        1. Recherche de la section PACKAGING
        2. Recherche de chaque type de fichier avec indication "obligatoire"
        3. Ajout à la liste si trouvé comme obligatoire
        4. Valeurs par défaut si section non trouvée

        Complexité : O(n) où n est la taille du contenu.
        Plusieurs recherches regex sont effectuées mais le nombre de patterns est limité.

        Patterns de recherche :
        - ``ZIP.*DIZ.*obligatoire`` : ZIP et DIZ mentionnés ensemble comme obligatoires
        - ``\\.nfo.*obligatoire`` : Fichier .nfo marqué comme obligatoire
        - ``RAR.*obligatoire`` : RAR marqué comme obligatoire (cas rare)

        Note : Le pattern `ZIP.*DIZ.*obligatoire` utilise `.*` pour permettre du texte
        entre les mots. Cela gère des formulations comme "ZIP+DIZ obligatoire" ou
        "ZIP et DIZ sont obligatoires".

        Args:
            rule_content: Contenu texte brut de la règle Scene.

        Returns:
            Liste triée et dédupliquée des types de fichiers requis (lowercase,
            ex: ["diz", "nfo", "zip"]).
        """
        required: list[str] = []

        # Recherche de la section PACKAGING avec même pattern que les autres sections
        packaging_pattern = r"PACKAGING\s*[:;]?\s*(.*?)(?=\n\n|\n[A-Z]|$)"
        match = re.search(packaging_pattern, rule_content, re.IGNORECASE | re.DOTALL)

        if match:
            packaging_text = match.group(1)

            # Vérification ZIP+DIZ obligatoire
            # Pattern flexible : "ZIP.*DIZ.*obligatoire" permet du texte entre les mots
            # Cela gère "ZIP+DIZ obligatoire", "ZIP et DIZ obligatoire", etc.
            if re.search(r"ZIP.*DIZ.*obligatoire", packaging_text, re.IGNORECASE):
                required.extend(["zip", "diz"])

            # Vérification fichier .nfo obligatoire
            # Pattern : `\.nfo.*obligatoire` pour détecter la mention du fichier .nfo
            # comme obligatoire. Le `\.` échappe le point pour rechercher littéralement ".nfo"
            if re.search(r"\.nfo.*obligatoire", packaging_text, re.IGNORECASE):
                required.append("nfo")

            # Vérification RAR (généralement optionnel)
            # Le RAR est généralement optionnel dans les règles Scene, mais on vérifie
            # s'il est explicitement marqué comme obligatoire
            if re.search(r"RAR", packaging_text, re.IGNORECASE) and re.search(
                r"RAR.*obligatoire", packaging_text, re.IGNORECASE
            ):
                required.append("rar")

        # Valeurs par défaut basées sur [2022] eBOOK : ZIP+DIZ+NFO obligatoire
        # Ces fichiers sont universellement requis dans les releases Scene eBook
        if not required:
            required = ["zip", "diz", "nfo"]

        # Tri et déduplication pour garantir un résultat cohérent
        return sorted(set(required))

    def extract_packaging_rules(self, rule_content: str) -> dict[str, Any]:
        """Extrait les règles de packaging depuis la section PACKAGING de la règle.

        Cette méthode parse les contraintes de packaging spécifiques aux releases Scene,
        notamment les tailles ZIP autorisées, les contraintes sur les fichiers NFO et DIZ,
        et les limites sur le nombre de fichiers.

        Algorithme :
        1. Initialisation avec valeurs par défaut basées sur [2022] eBOOK
        2. Recherche de tailles ZIP explicites dans la règle
        3. Parsing et conversion des tailles en bytes
        4. Mise à jour des règles avec valeurs trouvées

        Complexité : O(n) où n est la taille du contenu.
        Le parsing des tailles ZIP utilise findall qui parcourt le contenu une fois.

        Structure de retour :
        - zip : Règles pour archives ZIP
          - required : Booléen indiquant si ZIP est obligatoire
          - allowed_sizes : Liste des tailles autorisées en bytes
          - max_files : Nombre maximum de fichiers dans le ZIP
        - rar : Règles pour archives RAR (généralement optionnel)
        - nfo : Règles pour fichiers NFO
          - required : Booléen
          - max_width : Largeur maximale en caractères (80 selon règles Scene)
        - diz : Règles pour fichiers DIZ
          - required : Booléen
          - max_width : Largeur maximale (44 caractères)
          - max_height : Hauteur maximale (30 lignes)

        Note importante : Les tailles ZIP autorisées sont généralement des valeurs
        fixes définies par la Scene (5MB, 10MB, 50MB, etc.). Ces valeurs permettent
        de garantir une compatibilité avec les systèmes de distribution Scene.

        Args:
            rule_content: Contenu texte brut de la règle Scene.

        Returns:
            Dictionnaire contenant les règles de packaging structurées.
        """
        # Initialisation avec valeurs par défaut basées sur [2022] eBOOK
        # Ces valeurs correspondent aux standards Scene pour les releases eBook
        packaging_rules: dict[str, Any] = {
            "zip": {
                "required": True,
                # Tailles ZIP autorisées en bytes (multiples de 5MB généralement)
                # Ces tailles correspondent aux limites standard des archives Scene
                "allowed_sizes": [
                    5000000,  # 5 MB
                    10000000,  # 10 MB
                    50000000,  # 50 MB
                    100000000,  # 100 MB
                    150000000,  # 150 MB
                    200000000,  # 200 MB
                    250000000,  # 250 MB
                ],
                "max_files": 99,  # Maximum 99 fichiers par ZIP (limite Scene)
            },
            "rar": {
                "required": False,  # RAR généralement optionnel
            },
            "nfo": {
                "required": True,
                # Largeur maximale 80 caractères pour conformité ASCII art Scene
                # Cette limite garantit la lisibilité sur tous les systèmes
                "max_width": 80,
            },
            "diz": {
                "required": True,
                # Contraintes DIZ : 44 caractères de largeur max, 30 lignes max
                # Ces limites permettent une description concise dans file_id.diz
                "max_width": 44,
                "max_height": 30,
            },
        }

        # Recherche de tailles ZIP explicites dans la règle
        # Pattern regex : `ZIP.*?(\d+[.,]?\d*)\s*(?:bytes|MB|mb)`
        # - `ZIP.*?` : Mot "ZIP" suivi de texte quelconque (non-greedy)
        # - `(\d+[.,]?\d*)` : Capture d'un nombre avec éventuellement virgule ou point
        # - `\s*(?:bytes|MB|mb)` : Unités possibles (bytes, MB, mb)
        zip_pattern = r"ZIP.*?(\d+[.,]?\d*)\s*(?:bytes|MB|mb)"
        zip_matches = re.findall(zip_pattern, rule_content, re.IGNORECASE)

        if zip_matches:
            sizes = []
            for match in zip_matches:
                # Normalisation : suppression des séparateurs de milliers (virgule, point)
                # Exemples : "5,000,000" → "5000000", "5.000.000" → "5000000"
                size_str = match.replace(",", "").replace(".", "")
                try:
                    size = int(size_str)
                    sizes.append(size)
                except ValueError:
                    # Ignorer les valeurs non convertibles (ne devrait pas arriver normalement)
                    pass
            if sizes:
                # Tri des tailles pour garantir un ordre cohérent
                packaging_rules["zip"]["allowed_sizes"] = sorted(sizes)

        return packaging_rules
