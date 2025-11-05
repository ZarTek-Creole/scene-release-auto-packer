"""Tests unitaires pour ReleaseFormatterService.

Ce module teste le formatage des données de release pour affichage et export.
Le service doit générer des noms de fichiers et dossiers conformes aux règles Scene.
"""

from __future__ import annotations

import pytest

from web.services.formatter.release_formatter import ReleaseFormatterService


class TestReleaseFormatterService:
    """Tests unitaires pour ReleaseFormatterService."""

    def test_format_release_name_basic(self):
        """Test formatage nom release basique."""
        service = ReleaseFormatterService()
        
        name = service.format_release_name(
            title="Test Book",
            group="TESTGROUP",
            date="20250124"
        )
        
        assert name == "Test-Book-TESTGROUP-20250124"

    def test_format_release_name_with_special_chars(self):
        """Test formatage nom release avec caractères spéciaux."""
        service = ReleaseFormatterService()
        
        name = service.format_release_name(
            title="Test Book & More!",
            group="TESTGROUP",
            date="20250124"
        )
        
        # Caractères spéciaux doivent être remplacés ou supprimés
        assert "TESTGROUP" in name
        assert "20250124" in name

    def test_format_release_name_empty_title(self):
        """Test formatage nom release avec titre vide."""
        service = ReleaseFormatterService()
        
        name = service.format_release_name(
            title="",
            group="TESTGROUP",
            date="20250124"
        )
        
        assert "TESTGROUP" in name
        assert "20250124" in name

    def test_format_directory_name(self):
        """Test formatage nom dossier."""
        service = ReleaseFormatterService()
        
        dir_name = service.format_directory_name(
            release_name="Test-Book-TESTGROUP-20250124"
        )
        
        assert dir_name == "Test-Book-TESTGROUP-20250124"

    def test_normalize_metadata(self):
        """Test normalisation métadonnées."""
        service = ReleaseFormatterService()
        
        metadata = {
            "title": "  Test Book  ",
            "author": "Author Name",
            "year": "2025",
            "isbn": "1234567890",
        }
        
        normalized = service.normalize_metadata(metadata)
        
        assert normalized["title"] == "Test Book"
        assert normalized["year"] == 2025  # Converti en int si possible
        assert "isbn" in normalized

    def test_format_release_name_long_title(self):
        """Test formatage nom release avec titre très long."""
        service = ReleaseFormatterService()
        
        long_title = "A" * 200
        name = service.format_release_name(
            title=long_title,
            group="TESTGROUP",
            date="20250124"
        )
        
        # Le nom doit être tronqué si nécessaire
        assert len(name) <= 255  # Limite Scene standard
        assert "TESTGROUP" in name

    def test_format_release_name_different_formats(self):
        """Test formatage nom release selon différents formats."""
        service = ReleaseFormatterService()
        
        # Format EBOOK
        name_ebook = service.format_release_name(
            title="Test Book",
            group="TESTGROUP",
            date="20250124",
            release_type="EBOOK"
        )
        
        assert "TESTGROUP" in name_ebook
        assert "20250124" in name_ebook

    def test_normalize_metadata_with_none_values(self):
        """Test normalisation métadonnées avec valeurs None."""
        service = ReleaseFormatterService()
        
        metadata = {
            "title": "Test Book",
            "author": None,
            "publisher": None,
            "year": "2025",
        }
        
        normalized = service.normalize_metadata(metadata)
        
        assert normalized["title"] == "Test Book"
        assert normalized.get("author") is None or normalized.get("author") == ""
        assert normalized["year"] == 2025

    def test_format_filename(self):
        """Test formatage nom fichier."""
        service = ReleaseFormatterService()
        
        filename = service.format_filename(
            base_name="Test-Book-TESTGROUP-20250124",
            extension=".epub"
        )
        
        assert filename == "Test-Book-TESTGROUP-20250124.epub"

    def test_format_filename_without_extension(self):
        """Test formatage nom fichier sans extension."""
        service = ReleaseFormatterService()
        
        filename = service.format_filename(
            base_name="Test-Book-TESTGROUP-20250124",
            extension=""
        )
        
        assert filename == "Test-Book-TESTGROUP-20250124"

    def test_format_release_name_preserves_group_format(self):
        """Test que le format du groupe est préservé."""
        service = ReleaseFormatterService()
        
        name = service.format_release_name(
            title="Test Book",
            group="TESTGROUP123",
            date="20250124"
        )
        
        assert "TESTGROUP123" in name

