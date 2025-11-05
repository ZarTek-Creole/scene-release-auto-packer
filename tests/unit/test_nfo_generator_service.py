"""Tests for NfoGeneratorService.

Tests unitaires pour le service de génération de fichiers NFO conformes aux standards Scene.
"""

from __future__ import annotations

import pytest

from web.services.packaging.nfo_generator import NfoGeneratorService


class TestNfoGeneratorService:
    """Tests pour NfoGeneratorService."""

    def test_init(self) -> None:
        """Test initialisation du service."""
        service = NfoGeneratorService()
        assert service is not None
        assert service.MAX_LINE_WIDTH == 80

    def test_generate_nfo_basic(self) -> None:
        """Test génération NFO basique."""
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book",
            "group": "TESTGROUP",
            "date": "20250124",
        }
        result = service.generate_nfo(metadata)
        assert "Title: Test Book" in result
        assert "TESTGROUP" in result
        assert "20250124" in result
        assert len(result) > 0

    def test_generate_nfo_with_all_fields(self) -> None:
        """Test génération NFO avec tous les champs."""
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "isbn": "1234567890",
            "year": 2025,
            "language": "English",
            "format": "EPUB",
            "size": "1.5MB",
            "pages": 300,
            "description": "Test description",
            "group": "TESTGROUP",
            "date": "20250124",
        }
        result = service.generate_nfo(metadata)
        assert "Title: Test Book" in result
        assert "Author: Test Author" in result
        assert "Publisher: Test Publisher" in result
        assert "ISBN: 1234567890" in result
        assert "Year: 2025" in result

    def test_generate_nfo_with_template(self) -> None:
        """Test génération NFO avec template personnalisé."""
        service = NfoGeneratorService()
        template = "Title: {{title}}\nAuthor: {{author}}"
        metadata = {
            "title": "Test Book",
            "author": "Test Author",
        }
        result = service.generate_nfo(metadata, template=template)
        assert "Title: Test Book" in result
        assert "Author: Test Author" in result

    def test_generate_nfo_template_single_braces(self) -> None:
        """Test template avec accolades simples."""
        service = NfoGeneratorService()
        template = "Title: {title}\nAuthor: {author}"
        metadata = {
            "title": "Test Book",
            "author": "Test Author",
        }
        result = service.generate_nfo(metadata, template=template)
        assert "Title: Test Book" in result
        assert "Author: Test Author" in result

    def test_generate_nfo_template_with_none(self) -> None:
        """Test template avec valeurs None."""
        service = NfoGeneratorService()
        template = "Title: {{title}}\nAuthor: {{author}}"
        metadata = {
            "title": "Test Book",
            "author": None,
        }
        result = service.generate_nfo(metadata, template=template)
        assert "Title: Test Book" in result
        assert "Author:" in result  # None remplacé par chaîne vide

    def test_generate_nfo_respects_max_line_width(self) -> None:
        """Test respect contrainte 80 colonnes."""
        service = NfoGeneratorService()
        # Créer une ligne très longue
        long_line = "A" * 200
        template = f"{{{{long_line}}}}"
        metadata = {"long_line": long_line}
        result = service.generate_nfo(metadata, template=template)
        # Vérifier que toutes les lignes respectent 80 colonnes
        for line in result.split("\n"):
            assert len(line) <= 80

    def test_generate_header(self) -> None:
        """Test génération header."""
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book",
            "group": "TESTGROUP",
            "date": "20250124",
        }
        result = service._generate_header(metadata)
        assert len(result) > 0
        assert "=" * 80 in result  # Séparateur ASCII

    def test_generate_header_without_title(self) -> None:
        """Test génération header sans titre."""
        service = NfoGeneratorService()
        metadata = {
            "group": "TESTGROUP",
        }
        result = service._generate_header(metadata)
        assert len(result) > 0
        # Le header contient "Untitled Release" si pas de titre
        result_str = "\n".join(result)
        assert "Untitled Release" in result_str or "Group: TESTGROUP" in result_str

    def test_generate_body(self) -> None:
        """Test génération body."""
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book",
            "author": "Test Author",
            "year": 2025,
        }
        result = service._generate_body(metadata)
        assert "Title: Test Book" in result
        assert "Author: Test Author" in result
        assert "Year: 2025" in result

    def test_generate_body_ignores_none(self) -> None:
        """Test génération body ignore None."""
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book",
            "author": None,
            "year": 2025,
        }
        result = service._generate_body(metadata)
        assert "Title: Test Book" in result
        assert "Author:" not in result  # None ignoré
        assert "Year: 2025" in result

    def test_generate_footer(self) -> None:
        """Test génération footer."""
        service = NfoGeneratorService()
        metadata = {
            "group": "TESTGROUP",
            "date": "20250124",
        }
        result = service._generate_footer(metadata)
        assert "Released by: TESTGROUP" in result
        assert "Release Date: 20250124" in result

    def test_generate_footer_with_checksums(self) -> None:
        """Test génération footer avec checksums."""
        service = NfoGeneratorService()
        metadata = {
            "group": "TESTGROUP",
            "date": "20250124",
            "checksums": {
                "sha256": "abc123",
                "md5": "def456",
            },
        }
        result = service._generate_footer(metadata)
        assert "SHA-256: abc123" in result
        assert "MD5: def456" in result

    def test_format_line_short(self) -> None:
        """Test formatage ligne courte."""
        service = NfoGeneratorService()
        result = service._format_line("Short line", max_width=80)
        assert len(result) == 1
        assert result[0] == "Short line"

    def test_format_line_long(self) -> None:
        """Test formatage ligne longue."""
        service = NfoGeneratorService()
        long_line = "A" * 200
        result = service._format_line(long_line, max_width=80)
        # Vérifier que toutes les lignes respectent max_width
        for line in result:
            assert len(line) <= 80
        # Vérifier que la ligne a été coupée
        assert len(result) > 1

    def test_format_line_multiline(self) -> None:
        """Test formatage ligne multi-lignes."""
        service = NfoGeneratorService()
        multiline = "Line 1\nLine 2\nLine 3"
        result = service._format_line(multiline, max_width=80)
        assert len(result) == 3
        assert result[0] == "Line 1"
        assert result[1] == "Line 2"
        assert result[2] == "Line 3"

    def test_render_template_double_braces(self) -> None:
        """Test rendu template avec doubles accolades."""
        service = NfoGeneratorService()
        template = "Title: {{title}}"
        metadata = {"title": "Test Book"}
        result = service._render_template(template, metadata)
        assert result == "Title: Test Book"

    def test_render_template_single_braces(self) -> None:
        """Test rendu template avec accolades simples."""
        service = NfoGeneratorService()
        template = "Title: {title}"
        metadata = {"title": "Test Book"}
        result = service._render_template(template, metadata)
        assert result == "Title: Test Book"

    def test_render_template_multiple_placeholders(self) -> None:
        """Test rendu template avec plusieurs placeholders."""
        service = NfoGeneratorService()
        template = "Title: {{title}}, Author: {{author}}"
        metadata = {"title": "Test Book", "author": "Test Author"}
        result = service._render_template(template, metadata)
        assert "Title: Test Book" in result
        assert "Author: Test Author" in result

    def test_render_template_missing_placeholder(self) -> None:
        """Test rendu template avec placeholder manquant."""
        service = NfoGeneratorService()
        template = "Title: {{title}}, Author: {{author}}"
        metadata = {"title": "Test Book"}
        result = service._render_template(template, metadata)
        assert "Title: Test Book" in result
        assert "Author:" in result  # Placeholder manquant remplacé par chaîne vide

    def test_render_template_none_value(self) -> None:
        """Test rendu template avec valeur None."""
        service = NfoGeneratorService()
        template = "Title: {{title}}"
        metadata = {"title": None}
        result = service._render_template(template, metadata)
        assert result == "Title: "  # None remplacé par chaîne vide

