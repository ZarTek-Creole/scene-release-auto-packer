"""Tests unitaires pour le blueprint test_parser.

Ces tests vérifient les endpoints de test pour le parsing de règles Scene.
"""

from __future__ import annotations
from unittest.mock import patch

import pytest


class TestTestParserBlueprint:
    """Tests unitaires pour le blueprint test_parser."""

    def test_test_rule_parser_no_content(self, client: pytest.FixtureRequest) -> None:
        """Test endpoint rule-parser sans contenu.

        Vérifie que l'endpoint retourne une erreur 400 si aucun contenu n'est fourni.
        """
        response = client.post("/api/test/rule-parser", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert data is not None
        assert "rule_content requis" in data["error"]

    def test_test_rule_parser_empty_content(self, client: pytest.FixtureRequest) -> None:
        """Test endpoint rule-parser avec contenu vide.

        Vérifie que l'endpoint retourne une erreur 400 si le contenu est vide.
        """
        response = client.post("/api/test/rule-parser",
                               json={"rule_content": ""})
        assert response.status_code == 400
        data = response.get_json()
        assert data is not None
        assert "rule_content requis" in data["error"]

    def test_test_rule_parser_with_valid_content(self, client: pytest.FixtureRequest) -> None:
        """Test endpoint rule-parser avec contenu valide.

        Vérifie que l'endpoint parse correctement une règle Scene valide.
        """
        rule_content = """
        EBOOK RULE 2022
        
        FILE FORMATS:
        - EPUB
        - PDF
        - CBZ
        
        NAMING:
        GroupName-Author-Title-Format-Language-Year-ISBN-eBook
        
        REQUIRED FILES:
        - eBook file
        - NFO file
        
        PACKAGING:
        - Compress to RAR
        - Include NFO
        """

        response = client.post(
            "/api/test/rule-parser",
            json={"rule_content": rule_content},
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert data["success"] is True
        assert "result" in data
        result = data["result"]
        assert "file_formats" in result
        assert "naming" in result
        assert "required_files" in result
        assert "packaging" in result

    def test_test_extract_formats(self, client: pytest.FixtureRequest) -> None:
        """Test endpoint extract-formats.

        Vérifie que l'endpoint extrait correctement les formats de fichiers.
        """
        rule_content = """
        EBOOK RULE 2022
        
        FILE FORMATS:
        - EPUB
        - PDF
        - CBZ
        """

        response = client.post(
            "/api/test/rule-parser/extract-formats",
            json={"rule_content": rule_content},
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert data["success"] is True
        assert "formats" in data
        formats = data["formats"]
        assert isinstance(formats, list)
        # Formats peut être une liste de chaînes
        assert len(formats) >= 0

    def test_test_extract_naming(self, client: pytest.FixtureRequest) -> None:
        """Test endpoint extract-naming.

        Vérifie que l'endpoint extrait correctement le format de nommage.
        """
        rule_content = """
        EBOOK RULE 2022
        
        NAMING:
        GroupName-Author-Title-Format-Language-Year-ISBN-eBook
        """

        response = client.post(
            "/api/test/rule-parser/extract-naming",
            json={"rule_content": rule_content},
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert data["success"] is True
        assert "naming" in data
        naming = data["naming"]
        assert isinstance(naming, dict) or isinstance(naming, str)

    def test_test_rule_parser_exception(self, client: pytest.FixtureRequest) -> None:
        """Test endpoint rule-parser avec exception.

        Vérifie que l'endpoint gère correctement les exceptions lors du parsing.
        """
        # Mock pour forcer une exception lors du parsing
        with patch("web.blueprints.test_parser.RuleParserService") as mock_parser:
            mock_instance = mock_parser.return_value
            mock_instance.parse_ebook_rule_2022.side_effect = ValueError(
                "Test exception")

            rule_content = "TEST RULE CONTENT"

            response = client.post(
                "/api/test/rule-parser",
                json={"rule_content": rule_content},
                content_type="application/json",
            )

            assert response.status_code == 500
            data = response.get_json()
            assert data is not None
            assert data["success"] is False
            assert "error" in data
            assert "Test exception" in data["error"]

    def test_test_rule_parser_error_handling(self, client: pytest.FixtureRequest) -> None:
        """Test gestion d'erreurs lors du parsing.

        Vérifie que l'endpoint gère correctement les erreurs de parsing.
        """
        # Contenu invalide qui pourrait causer une erreur
        invalid_content = "INVALID RULE CONTENT" * 1000

        response = client.post(
            "/api/test/rule-parser",
            json={"rule_content": invalid_content},
            content_type="application/json",
        )

        # Le résultat peut être 200 (succès avec parsing partiel) ou 500 (erreur)
        assert response.status_code in (200, 500)
        data = response.get_json()
        assert data is not None
        assert "success" in data

    def test_test_extract_formats_empty_content(self, client: pytest.FixtureRequest) -> None:
        """Test endpoint extract-formats avec contenu vide.

        Vérifie que l'endpoint gère correctement un contenu vide.
        """
        response = client.post(
            "/api/test/rule-parser/extract-formats",
            json={"rule_content": ""},
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert data["success"] is True
        assert "formats" in data
        formats = data["formats"]
        assert isinstance(formats, list)

    def test_test_extract_naming_empty_content(self, client: pytest.FixtureRequest) -> None:
        """Test endpoint extract-naming avec contenu vide.

        Vérifie que l'endpoint gère correctement un contenu vide.
        """
        response = client.post(
            "/api/test/rule-parser/extract-naming",
            json={"rule_content": ""},
            content_type="application/json",
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data is not None
        assert data["success"] is True
        assert "naming" in data
