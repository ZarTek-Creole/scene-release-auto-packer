"""Tests for ReleaseFormatterService.

Tests unitaires pour le service de formatage des releases selon les règles Scene.
"""

from __future__ import annotations

import pytest

from web.services.formatter.release_formatter import ReleaseFormatterService


class TestReleaseFormatterService:
    """Tests pour ReleaseFormatterService."""

    def test_init(self) -> None:
        """Test initialisation du service."""
        service = ReleaseFormatterService()
        assert service is not None
        assert service.MAX_RELEASE_NAME_LENGTH == 255

    def test_format_release_name_success(self) -> None:
        """Test formatage nom release réussi."""
        service = ReleaseFormatterService()
        result = service.format_release_name(
            title="Test Book",
            group="TESTGROUP",
            date="20250124",
        )
        assert result == "Test-Book-TESTGROUP-20250124"

    def test_format_release_name_normalizes_title(self) -> None:
        """Test normalisation titre (espaces, caractères spéciaux)."""
        service = ReleaseFormatterService()
        result = service.format_release_name(
            title="Test  Book @#$%",
            group="TESTGROUP",
            date="20250124",
        )
        assert result == "Test-Book-TESTGROUP-20250124"

    def test_format_release_name_normalizes_group(self) -> None:
        """Test normalisation groupe (uppercase, caractères spéciaux)."""
        service = ReleaseFormatterService()
        result = service.format_release_name(
            title="Test Book",
            group="testgroup123",
            date="20250124",
        )
        assert result == "Test-Book-TESTGROUP123-20250124"

    def test_format_release_name_empty_group(self) -> None:
        """Test erreur groupe vide."""
        service = ReleaseFormatterService()
        with pytest.raises(ValueError, match="Le nom du groupe ne peut pas être vide"):
            service.format_release_name(
                title="Test Book",
                group="",
                date="20250124",
            )

    def test_format_release_name_invalid_date_format(self) -> None:
        """Test erreur date format invalide."""
        service = ReleaseFormatterService()
        with pytest.raises(ValueError, match="Date invalide"):
            service.format_release_name(
                title="Test Book",
                group="TESTGROUP",
                date="2025-01-24",
            )

    def test_format_release_name_invalid_date_length(self) -> None:
        """Test erreur date longueur invalide."""
        service = ReleaseFormatterService()
        with pytest.raises(ValueError, match="Date invalide"):
            service.format_release_name(
                title="Test Book",
                group="TESTGROUP",
                date="2025012",
            )

    def test_format_release_name_truncates_long_title(self) -> None:
        """Test troncature titre trop long."""
        service = ReleaseFormatterService()
        # Créer un titre très long
        long_title = "A" * 300
        result = service.format_release_name(
            title=long_title,
            group="TESTGROUP",
            date="20250124",
        )
        # Vérifier que le résultat respecte la limite de 255 caractères
        assert len(result) <= 255
        assert result.endswith("-TESTGROUP-20250124")

    def test_format_directory_name(self) -> None:
        """Test formatage nom dossier."""
        service = ReleaseFormatterService()
        result = service.format_directory_name("Test-Book-TESTGROUP-20250124")
        assert result == "Test-Book-TESTGROUP-20250124"

    def test_format_directory_name_trim(self) -> None:
        """Test formatage nom dossier avec trim."""
        service = ReleaseFormatterService()
        result = service.format_directory_name("  Test-Book-TESTGROUP-20250124  ")
        assert result == "Test-Book-TESTGROUP-20250124"

    def test_format_filename_with_extension(self) -> None:
        """Test formatage nom fichier avec extension."""
        service = ReleaseFormatterService()
        result = service.format_filename("Test-Book-TESTGROUP-20250124", ".epub")
        assert result == "Test-Book-TESTGROUP-20250124.epub"

    def test_format_filename_without_extension(self) -> None:
        """Test formatage nom fichier sans extension."""
        service = ReleaseFormatterService()
        result = service.format_filename("Test-Book-TESTGROUP-20250124", "")
        assert result == "Test-Book-TESTGROUP-20250124"

    def test_format_filename_adds_dot_if_missing(self) -> None:
        """Test ajout point si extension sans point."""
        service = ReleaseFormatterService()
        result = service.format_filename("Test-Book-TESTGROUP-20250124", "epub")
        assert result == "Test-Book-TESTGROUP-20250124.epub"

    def test_normalize_metadata_removes_none(self) -> None:
        """Test normalisation métadonnées supprime None."""
        service = ReleaseFormatterService()
        metadata = {
            "title": "Test Book",
            "author": None,
            "year": 2025,
        }
        result = service.normalize_metadata(metadata)
        assert "title" in result
        assert "author" not in result
        assert "year" in result

    def test_normalize_metadata_trims_strings(self) -> None:
        """Test normalisation métadonnées trim chaînes."""
        service = ReleaseFormatterService()
        metadata = {
            "title": "  Test Book  ",
            "author": "  Test Author  ",
        }
        result = service.normalize_metadata(metadata)
        assert result["title"] == "Test Book"
        assert result["author"] == "Test Author"

    def test_normalize_metadata_removes_empty_strings(self) -> None:
        """Test normalisation métadonnées supprime chaînes vides."""
        service = ReleaseFormatterService()
        metadata = {
            "title": "Test Book",
            "author": "   ",
            "year": 2025,
        }
        result = service.normalize_metadata(metadata)
        assert "title" in result
        assert "author" not in result
        assert "year" in result

    def test_normalize_metadata_converts_year_to_int(self) -> None:
        """Test conversion année en int."""
        service = ReleaseFormatterService()
        metadata = {
            "year": "2025",
            "pages": "300",
        }
        result = service.normalize_metadata(metadata)
        assert result["year"] == 2025
        assert result["pages"] == 300

    def test_normalize_metadata_keeps_invalid_int_as_string(self) -> None:
        """Test garde valeur invalide comme chaîne."""
        service = ReleaseFormatterService()
        metadata = {
            "year": "invalid",
        }
        result = service.normalize_metadata(metadata)
        assert result["year"] == "invalid"

    def test_normalize_metadata_normalizes_list(self) -> None:
        """Test normalisation liste."""
        service = ReleaseFormatterService()
        metadata = {
            "tags": ["  tag1  ", "tag2", None, "  tag3  "],
        }
        result = service.normalize_metadata(metadata)
        assert result["tags"] == ["tag1", "tag2", "tag3"]

    def test_normalize_metadata_removes_empty_list(self) -> None:
        """Test suppression liste vide."""
        service = ReleaseFormatterService()
        metadata = {
            "tags": [],
            "title": "Test Book",
        }
        result = service.normalize_metadata(metadata)
        assert "tags" not in result
        assert "title" in result

    def test_normalize_metadata_preserves_int_and_float(self) -> None:
        """Test préservation int et float."""
        service = ReleaseFormatterService()
        metadata = {
            "year": 2025,
            "price": 29.99,
        }
        result = service.normalize_metadata(metadata)
        assert result["year"] == 2025
        assert result["price"] == 29.99

