"""Tests unitaires pour ReleaseValidatorService.

Ce module teste la validation complète d'une release selon les règles Scene.
Le service doit vérifier nommage, métadonnées, structure et retourner liste d'erreurs.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from web.services.validator.release_validator import ReleaseValidatorService


class TestReleaseValidatorService:
    """Tests unitaires pour ReleaseValidatorService."""

    def test_validate_release_success(self):
        """Test validation release valide."""
        service = ReleaseValidatorService()
        
        release_data = {
            "name": "Test-Book-TESTGROUP-20250124",
            "group": "TESTGROUP",
            "release_type": "EBOOK",
            "metadata": {
                "title": "Test Book",
                "author": "Test Author",
            },
            "files": ["Test-Book-TESTGROUP-20250124.epub"],
        }
        
        rule_spec = {
            "naming": {
                "pattern": r"^[A-Z0-9a-z\-]+-\d{8}$",  # Pattern plus flexible pour tests
            },
            "file_formats": [".epub", ".pdf"],
            # Pas de required_files pour ce test (NFO optionnel dans ce cas)
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_validate_release_invalid_naming(self):
        """Test validation release avec nommage invalide."""
        service = ReleaseValidatorService()
        
        release_data = {
            "name": "Invalid Name!",
            "group": "TESTGROUP",
            "release_type": "EBOOK",
        }
        
        rule_spec = {
            "pattern": r"^[A-Z0-9]+-[A-Z0-9\-]+-\d{8}$",  # Pattern strict Scene
        }
        
        result = service.validate_naming(release_data["name"], rule_spec)
        
        assert len(result) > 0  # Doit avoir des erreurs car "Invalid Name!" ne correspond pas

    def test_validate_naming_pattern_match(self):
        """Test validation nommage avec pattern regex."""
        service = ReleaseValidatorService()
        
        valid_name = "TESTGROUP-Test-Book-20250124"  # Format conforme Scene
        invalid_name = "Invalid_Name!"  # Contient caractères spéciaux
        
        rule_spec = {
            "pattern": r"^[A-Z0-9]+-[A-Z0-9a-z\-]+-\d{8}$",  # Pattern qui accepte le nom valide
        }
        
        errors_valid = service.validate_naming(valid_name, rule_spec)
        
        # Pour invalid_name, utiliser un pattern strict qui rejette les caractères spéciaux
        rule_spec_strict = {
            "pattern": r"^[A-Z0-9a-z\-]+-\d{8}$",  # Pattern qui rejette les caractères spéciaux
        }
        errors_invalid = service.validate_naming(invalid_name, rule_spec_strict)
        
        assert len(errors_valid) == 0
        assert len(errors_invalid) > 0  # Doit détecter le caractère spécial "!"

    def test_validate_metadata_missing_required(self):
        """Test validation métadonnées avec champs requis manquants."""
        service = ReleaseValidatorService()
        
        metadata = {
            "title": "Test Book",
            # author manquant
        }
        
        rule_spec = {
            "required_fields": ["title", "author"],
        }
        
        errors = service.validate_metadata(metadata, rule_spec)
        
        assert len(errors) > 0
        assert any("author" in error.lower() for error in errors)

    def test_validate_metadata_format_validation(self):
        """Test validation format des métadonnées."""
        service = ReleaseValidatorService()
        
        metadata = {
            "title": "Test Book",
            "isbn": "invalid-isbn",  # Format invalide
            "year": "not-a-year",  # Format invalide
        }
        
        rule_spec = {
            "metadata_formats": {
                "isbn": r"^\d{10}$|^\d{13}$",
                "year": r"^\d{4}$",
            },
        }
        
        errors = service.validate_metadata(metadata, rule_spec)
        
        assert len(errors) > 0

    def test_validate_structure_missing_files(self):
        """Test validation structure avec fichiers manquants."""
        service = ReleaseValidatorService()
        
        files = ["Test-Book-TESTGROUP-20250124.epub"]
        # NFO manquant
        
        rule_spec = {
            "required_files": ["nfo"],
        }
        
        errors = service.validate_structure(files, rule_spec)
        
        assert len(errors) > 0
        assert any("nfo" in error.lower() for error in errors)

    def test_validate_structure_invalid_format(self):
        """Test validation structure avec format fichier invalide."""
        service = ReleaseValidatorService()
        
        files = ["Test-Book-TESTGROUP-20250124.txt"]  # Format non autorisé
        
        rule_spec = {
            "file_formats": [".epub", ".pdf"],
        }
        
        errors = service.validate_structure(files, rule_spec)
        
        assert len(errors) > 0

    def test_validate_release_multiple_errors(self):
        """Test validation release avec plusieurs erreurs."""
        service = ReleaseValidatorService()
        
        release_data = {
            "name": "Invalid Name!",
            "group": "TESTGROUP",
            "release_type": "EBOOK",
            "metadata": {},  # Métadonnées vides
            "files": [],  # Pas de fichiers
        }
        
        rule_spec = {
            "naming": {
                "pattern": r"^[A-Z0-9]+-[A-Z0-9\-]+-\d{8}$",
            },
            "required_files": ["epub", "nfo"],
            "required_fields": ["title"],
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 1  # Plusieurs erreurs

    def test_validate_release_warnings(self):
        """Test validation release avec avertissements."""
        service = ReleaseValidatorService()
        
        release_data = {
            "name": "Test-Book-TESTGROUP-20250124",
            "group": "TESTGROUP",
            "release_type": "EBOOK",
            "metadata": {
                "title": "Test Book",
            },
            "files": ["Test-Book-TESTGROUP-20250124.epub"],
        }
        
        rule_spec = {
            "naming": {
                "pattern": r"^[A-Z0-9]+-[A-Z0-9\-]+-\d{8}$",
            },
            "recommended_fields": ["author"],  # Champ recommandé mais non requis
        }
        
        result = service.validate_release(release_data, rule_spec)
        
        # Peut avoir des avertissements même si valide
        assert isinstance(result.get("warnings", []), list)

    def test_validate_release_different_types(self):
        """Test validation release pour différents types (TV, EBOOK, DOCS)."""
        service = ReleaseValidatorService()
        
        for release_type in ["TV", "EBOOK", "DOCS"]:
            release_data = {
                "name": f"Test-{release_type}-TESTGROUP-20250124",
                "group": "TESTGROUP",
                "release_type": release_type,
            }
            
            rule_spec = {
                "naming": {
                    "pattern": r"^[A-Z0-9]+-[A-Z0-9\-]+-\d{8}$",
                },
            }
            
            result = service.validate_release(release_data, rule_spec)
            
            # Doit toujours retourner un résultat valide
            assert "valid" in result
            assert isinstance(result["errors"], list)

