"""Tests unitaires pour RuleParserService.

Ces tests vérifient le parsing et la validation des règles Scene,
notamment la règle [2022] eBOOK.

Approche TDD : Tests écrits avant toute modification du service.
"""

from __future__ import annotations

import pytest
from web.services.rule import RuleParserService


class TestRuleParserService:
    """Tests unitaires pour RuleParserService."""

    def test_parse_ebook_rule_2022_extract_file_formats(self) -> None:
        """Test extraction des formats de fichiers depuis section OTHER.
        
        Vérifie que la méthode extract_file_formats extrait correctement
        tous les formats acceptés depuis une règle Scene valide.
        """
        parser = RuleParserService()

        # Contenu de règle mocké (version simplifiée de [2022] eBOOK)
        rule_content = """
        OTHER
        PDF, EPUB, CBZ, Kindle (.azw, .kf8), MOBIPOCKET (.prc, .mobi)
        """

        formats = parser.extract_file_formats(rule_content)

        # Vérification que tous les formats attendus sont présents
        assert ".pdf" in formats
        assert ".epub" in formats
        assert ".cbz" in formats
        assert ".azw" in formats
        assert ".kf8" in formats
        assert ".mobi" in formats
        assert ".prc" in formats
        
        # Vérification que la liste est triée et dédupliquée
        assert formats == sorted(set(formats))

    def test_parse_ebook_rule_2022_extract_file_formats_default(self) -> None:
        """Test extraction formats avec valeurs par défaut si section OTHER absente.
        
        Vérifie que si la section OTHER n'est pas trouvée, les valeurs par défaut
        de [2022] eBOOK sont utilisées.
        """
        parser = RuleParserService()

        # Contenu sans section OTHER
        rule_content = """
        DIRNAMING
        GroupName-Author-Title-Format-Language-Year-ISBN-eBook
        """

        formats = parser.extract_file_formats(rule_content)

        # Vérification que les formats par défaut sont présents
        assert ".pdf" in formats
        assert ".epub" in formats
        assert ".cbz" in formats
        assert ".azw" in formats
        assert ".kf8" in formats
        assert ".mobi" in formats
        assert ".prc" in formats

    def test_extract_naming_format(self) -> None:
        """Test extraction du format de nommage depuis section DIRNAMING.
        
        Vérifie que la méthode extract_naming_format extrait correctement
        le format de nommage et ses composants.
        """
        parser = RuleParserService()

        # Contenu de règle avec section DIRNAMING
        rule_content = """
        DIRNAMING
        GroupName-Author-Title-Format-Language-Year-ISBN-eBook
        """

        naming_format = parser.extract_naming_format(rule_content)

        # Vérification de la structure de retour
        assert naming_format is not None
        assert "format" in naming_format
        assert "components" in naming_format
        assert "separators" in naming_format
        assert "max_length" in naming_format
        
        # Vérification du format
        assert "GroupName" in naming_format["format"]
        assert "Author" in naming_format["format"]
        
        # Vérification de la longueur maximale (contrainte Scene)
        assert naming_format["max_length"] == 243

    def test_extract_naming_format_default(self) -> None:
        """Test extraction format nommage avec valeurs par défaut.
        
        Vérifie que si la section DIRNAMING n'est pas trouvée, le format par défaut
        de [2022] eBOOK est utilisé.
        """
        parser = RuleParserService()

        # Contenu sans section DIRNAMING
        rule_content = """
        OTHER
        PDF, EPUB
        """

        naming_format = parser.extract_naming_format(rule_content)

        # Vérification que le format par défaut est retourné
        assert naming_format["format"] == "GroupName-Author-Title-Format-Language-Year-ISBN-eBook"
        assert "GroupName" in naming_format["components"]
        assert "Author" in naming_format["components"]
        assert "Title" in naming_format["components"]
        assert naming_format["max_length"] == 243

    def test_extract_required_files(self) -> None:
        """Test extraction des fichiers requis depuis section PACKAGING.
        
        Vérifie que la méthode extract_required_files détecte correctement
        les fichiers obligatoires mentionnés dans la règle.
        """
        parser = RuleParserService()

        # Contenu avec section PACKAGING
        rule_content = """
        PACKAGING
        ZIP+DIZ obligatoire
        .nfo file obligatoire
        """

        required_files = parser.extract_required_files(rule_content)

        # Vérification que tous les fichiers requis sont présents
        assert "zip" in required_files
        assert "diz" in required_files
        assert "nfo" in required_files
        
        # Vérification que la liste est triée et dédupliquée
        assert required_files == sorted(set(required_files))

    def test_extract_required_files_with_rar(self) -> None:
        """Test extraction fichiers requis avec RAR obligatoire.
        
        Vérifie que si RAR est explicitement marqué comme obligatoire,
        il est ajouté à la liste.
        """
        parser = RuleParserService()

        # Contenu avec RAR obligatoire
        rule_content = """
        PACKAGING
        ZIP+DIZ obligatoire
        .nfo file obligatoire
        RAR obligatoire
        """

        required_files = parser.extract_required_files(rule_content)

        assert "zip" in required_files
        assert "diz" in required_files
        assert "nfo" in required_files
        assert "rar" in required_files

    def test_extract_required_files_default(self) -> None:
        """Test extraction fichiers requis avec valeurs par défaut.
        
        Vérifie que si la section PACKAGING n'est pas trouvée, les valeurs par défaut
        de [2022] eBOOK sont utilisées (ZIP+DIZ+NFO).
        """
        parser = RuleParserService()

        # Contenu sans section PACKAGING
        rule_content = """
        OTHER
        PDF, EPUB
        """

        required_files = parser.extract_required_files(rule_content)

        # Vérification des valeurs par défaut
        assert "zip" in required_files
        assert "diz" in required_files
        assert "nfo" in required_files

    def test_extract_packaging_rules(self) -> None:
        """Test extraction des règles de packaging.
        
        Vérifie que la méthode extract_packaging_rules extrait correctement
        les contraintes de packaging (tailles ZIP, contraintes NFO/DIZ).
        """
        parser = RuleParserService()

        # Contenu avec section PACKAGING
        rule_content = """
        PACKAGING
        ZIP max 100MB
        """

        packaging_rules = parser.extract_packaging_rules(rule_content)

        # Vérification de la structure
        assert "zip" in packaging_rules
        assert "rar" in packaging_rules
        assert "nfo" in packaging_rules
        assert "diz" in packaging_rules
        
        # Vérification des contraintes ZIP
        assert packaging_rules["zip"]["required"] is True
        assert "allowed_sizes" in packaging_rules["zip"]
        assert packaging_rules["zip"]["max_files"] == 99
        
        # Vérification des contraintes NFO
        assert packaging_rules["nfo"]["required"] is True
        assert packaging_rules["nfo"]["max_width"] == 80
        
        # Vérification des contraintes DIZ
        assert packaging_rules["diz"]["required"] is True
        assert packaging_rules["diz"]["max_width"] == 44
        assert packaging_rules["diz"]["max_height"] == 30

    def test_parse_ebook_rule_2022_complete(self) -> None:
        """Test parsing complet d'une règle [2022] eBOOK.
        
        Vérifie que la méthode parse_ebook_rule_2022 extrait correctement
        toutes les sections d'une règle complète.
        """
        parser = RuleParserService()

        # Contenu complet mocké (simplifié)
        rule_content = """
        [2022] eBOOK

        OTHER
        PDF, EPUB, CBZ, Kindle (.azw, .kf8), MOBIPOCKET (.prc, .mobi)

        PACKAGING
        ZIP+DIZ obligatoire
        .nfo file obligatoire

        DIRNAMING
        GroupName-Author-Title-Format-Language-Year-ISBN-eBook
        """

        rule_spec = parser.parse_ebook_rule_2022(rule_content)

        # Vérification que toutes les sections sont présentes
        assert rule_spec is not None
        assert "file_formats" in rule_spec
        assert "naming" in rule_spec
        assert "required_files" in rule_spec
        assert "packaging" in rule_spec
        
        # Vérification des formats
        assert len(rule_spec["file_formats"]) > 0
        assert ".pdf" in rule_spec["file_formats"]
        
        # Vérification du format de nommage
        assert rule_spec["naming"]["format"] is not None
        assert rule_spec["naming"]["max_length"] == 243
        
        # Vérification des fichiers requis
        assert len(rule_spec["required_files"]) > 0
        assert "zip" in rule_spec["required_files"]
        
        # Vérification des règles de packaging
        assert "zip" in rule_spec["packaging"]
        assert "nfo" in rule_spec["packaging"]

    def test_extract_file_formats_case_insensitive(self) -> None:
        """Test extraction formats insensible à la casse.
        
        Vérifie que l'extraction fonctionne même si la casse varie dans la règle.
        """
        parser = RuleParserService()

        # Contenu avec casse variée
        rule_content = """
        other
        pdf, epub, cbz
        """

        formats = parser.extract_file_formats(rule_content)

        assert ".pdf" in formats
        assert ".epub" in formats
        assert ".cbz" in formats

    def test_extract_naming_format_invalid_pattern(self) -> None:
        """Test extraction format nommage avec pattern invalide.
        
        Vérifie que si le pattern de nommage ne contient pas de tirets
        (requis pour les patterns Scene), les valeurs par défaut sont utilisées.
        """
        parser = RuleParserService()

        # Contenu avec section DIRNAMING mais pattern sans tirets (invalide pour Scene)
        # Le pattern regex requiert au moins un tiret entre deux mots
        rule_content = """
        DIRNAMING
        InvalidPatternWithoutDashes
        """

        naming_format = parser.extract_naming_format(rule_content)

        # Vérification que le format par défaut est retourné car le pattern est invalide
        assert naming_format["format"] == "GroupName-Author-Title-Format-Language-Year-ISBN-eBook"
        assert naming_format["max_length"] == 243

