"""Tests for ReleaseValidatorService.

Tests unitaires pour le service de validation complète d'une release selon les règles Scene.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from web.services.validator.release_validator import ReleaseValidatorService


class TestReleaseValidatorService:
    """Tests pour ReleaseValidatorService."""

    def test_init(self) -> None:
        """Test initialisation du service."""
        service = ReleaseValidatorService()
        assert service is not None

    def test_validate_release_success(self) -> None:
        """Test validation release réussie."""
        service = ReleaseValidatorService()
        release_data = {
            "name": "Test-Book-TESTGROUP-20250124",
            "group": "TESTGROUP",
            "release_type": "EBOOK",
            "metadata": {
                "title": "Test Book",
                "author": "Test Author",
            },
            "files": ["test.epub"],
        }
        rule_spec = {
            "naming": {
                "pattern": r"^[A-Za-z0-9\-]+$",
            },
            "required_fields": ["title"],
            "required_files": [".epub"],
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_validate_release_naming_failure(self) -> None:
        """Test validation nommage échoue."""
        service = ReleaseValidatorService()
        release_data = {
            "name": "Invalid@Name#123",
            "group": "TESTGROUP",
            "release_type": "EBOOK",
        }
        rule_spec = {
            "naming": {
                "pattern": r"^[A-Za-z0-9\-]+$",
            },
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert any("pattern" in error.lower() for error in result["errors"])

    def test_validate_release_empty_name(self) -> None:
        """Test validation nom vide."""
        service = ReleaseValidatorService()
        release_data = {
            "name": "",
            "group": "TESTGROUP",
        }
        rule_spec = {
            "naming": {
                "pattern": r"^[A-Za-z0-9\-]+$",
            },
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        assert result["valid"] is False
        assert any("vide" in error.lower() or "empty" in error.lower() for error in result["errors"])

    def test_validate_release_max_length(self) -> None:
        """Test validation longueur maximale."""
        service = ReleaseValidatorService()
        long_name = "A" * 300
        release_data = {
            "name": long_name,
            "group": "TESTGROUP",
        }
        rule_spec = {
            "naming": {
                "max_length": 255,
            },
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        assert result["valid"] is False
        assert any("longueur" in error.lower() or "length" in error.lower() for error in result["errors"])

    def test_validate_release_allowed_chars(self) -> None:
        """Test validation caractères autorisés."""
        service = ReleaseValidatorService()
        release_data = {
            "name": "Test@Book#123",
            "group": "TESTGROUP",
        }
        rule_spec = {
            "naming": {
                "allowed_chars": r"^[A-Za-z0-9\-]+$",
            },
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        assert result["valid"] is False
        assert any("caractères" in error.lower() or "characters" in error.lower() for error in result["errors"])

    def test_validate_release_invalid_regex_pattern(self) -> None:
        """Test erreur pattern regex invalide."""
        service = ReleaseValidatorService()
        release_data = {
            "name": "Test-Book",
            "group": "TESTGROUP",
        }
        rule_spec = {
            "naming": {
                "pattern": r"[[invalid regex",
            },
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        assert result["valid"] is False
        assert any("pattern" in error.lower() or "regex" in error.lower() for error in result["errors"])

    def test_validate_release_missing_required_field(self) -> None:
        """Test validation champ requis manquant."""
        service = ReleaseValidatorService()
        release_data = {
            "name": "Test-Book-TESTGROUP-20250124",
            "group": "TESTGROUP",
            "metadata": {},
        }
        rule_spec = {
            "required_fields": ["title", "author"],
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        assert result["valid"] is False
        assert any("title" in error.lower() for error in result["errors"])
        assert any("author" in error.lower() for error in result["errors"])

    def test_validate_release_metadata_format(self) -> None:
        """Test validation format métadonnées."""
        service = ReleaseValidatorService()
        release_data = {
            "name": "Test-Book-TESTGROUP-20250124",
            "group": "TESTGROUP",
            "metadata": {
                "isbn": "invalid-isbn",
            },
        }
        rule_spec = {
            "metadata_formats": {
                "isbn": r"^\d{10}$|^\d{13}$",
            },
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        assert result["valid"] is False
        assert any("isbn" in error.lower() for error in result["errors"])

    def test_validate_release_missing_required_file(self) -> None:
        """Test validation fichier requis manquant."""
        service = ReleaseValidatorService()
        release_data = {
            "name": "Test-Book-TESTGROUP-20250124",
            "group": "TESTGROUP",
            "files": ["test.pdf"],
        }
        rule_spec = {
            "required_files": [".epub", ".nfo"],
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        assert result["valid"] is False
        assert any(".epub" in error.lower() or ".nfo" in error.lower() for error in result["errors"])

    def test_validate_release_invalid_file_format(self) -> None:
        """Test validation format fichier invalide."""
        service = ReleaseValidatorService()
        release_data = {
            "name": "Test-Book-TESTGROUP-20250124",
            "group": "TESTGROUP",
            "files": ["test.doc"],
        }
        rule_spec = {
            "file_formats": [".epub", ".pdf", ".nfo"],
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        assert result["valid"] is False
        assert any(".doc" in error.lower() for error in result["errors"])

    def test_validate_release_recommended_fields(self) -> None:
        """Test avertissements champs recommandés."""
        service = ReleaseValidatorService()
        release_data = {
            "name": "Test-Book-TESTGROUP-20250124",
            "group": "TESTGROUP",
            "metadata": {},
        }
        rule_spec = {
            "recommended_fields": ["description", "tags"],
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        # Les champs recommandés génèrent des avertissements, pas des erreurs
        assert result["valid"] is True  # Pas d'erreurs bloquantes
        assert len(result["warnings"]) > 0
        assert any("description" in warning.lower() for warning in result["warnings"])

    def test_validate_naming(self) -> None:
        """Test validation nommage directe."""
        service = ReleaseValidatorService()
        result = service.validate_naming("Test-Book-TESTGROUP-20250124", {
            "pattern": r"^[A-Za-z0-9\-]+$",
        })
        
        assert len(result) == 0  # Pas d'erreurs

    def test_validate_naming_empty(self) -> None:
        """Test validation nommage vide."""
        service = ReleaseValidatorService()
        result = service.validate_naming("", {
            "pattern": r"^[A-Za-z0-9\-]+$",
        })
        
        assert len(result) > 0
        assert any("vide" in error.lower() or "empty" in error.lower() for error in result)

    def test_validate_metadata(self) -> None:
        """Test validation métadonnées directe."""
        service = ReleaseValidatorService()
        metadata = {
            "title": "Test Book",
            "author": "Test Author",
        }
        rule_spec = {
            "required_fields": ["title"],
        }
        
        result = service.validate_metadata(metadata, rule_spec)
        
        assert len(result) == 0  # Pas d'erreurs

    def test_validate_metadata_missing_required(self) -> None:
        """Test validation métadonnées champ requis manquant."""
        service = ReleaseValidatorService()
        metadata = {}
        rule_spec = {
            "required_fields": ["title"],
        }
        
        result = service.validate_metadata(metadata, rule_spec)
        
        assert len(result) > 0
        assert any("title" in error.lower() for error in result)

    def test_validate_structure(self) -> None:
        """Test validation structure directe."""
        service = ReleaseValidatorService()
        files = ["test.epub", "test.nfo"]
        rule_spec = {
            "required_files": [".epub"],
            "file_formats": [".epub", ".nfo"],
        }
        
        result = service.validate_structure(files, rule_spec)
        
        assert len(result) == 0  # Pas d'erreurs

    def test_validate_structure_with_path_objects(self) -> None:
        """Test validation structure avec objets Path."""
        service = ReleaseValidatorService()
        files = [Path("test.epub"), Path("test.nfo")]
        rule_spec = {
            "required_files": [".epub"],
        }
        
        result = service.validate_structure(files, rule_spec)
        
        assert len(result) == 0  # Pas d'erreurs

    def test_validate_structure_missing_required(self) -> None:
        """Test validation structure fichier requis manquant."""
        service = ReleaseValidatorService()
        files = ["test.pdf"]
        rule_spec = {
            "required_files": [".epub"],
        }
        
        result = service.validate_structure(files, rule_spec)
        
        assert len(result) > 0
        assert any(".epub" in error.lower() for error in result)

    def test_validate_structure_file_format_without_dot(self) -> None:
        """Test validation structure format sans point."""
        service = ReleaseValidatorService()
        files = ["test.epub"]
        rule_spec = {
            "required_files": ["epub"],  # Sans point
        }
        
        result = service.validate_structure(files, rule_spec)
        
        assert len(result) == 0  # Devrait matcher quand même

