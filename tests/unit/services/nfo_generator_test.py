"""Tests unitaires pour NfoGeneratorService.

Ce module teste la génération de fichiers NFO conformes aux standards Scene.
Le NFO doit respecter les contraintes ASCII 80 colonnes et être formaté correctement.
"""

from __future__ import annotations

import pytest

from web.services.packaging.nfo_generator import NfoGeneratorService


class TestNfoGeneratorService:
    """Tests unitaires pour NfoGeneratorService."""

    def test_generate_nfo_basic(self):
        """Test génération NFO basique avec métadonnées minimales."""
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book",
            "author": "Test Author",
            "group": "TESTGROUP",
            "date": "20250124",
        }
        
        nfo = service.generate_nfo(metadata)
        
        assert "Test Book" in nfo
        assert "Test Author" in nfo
        assert "TESTGROUP" in nfo
        assert "20250124" in nfo

    def test_nfo_lines_max_80_columns(self):
        """Test que toutes les lignes respectent la contrainte 80 colonnes."""
        service = NfoGeneratorService()
        metadata = {
            "title": "A" * 100,  # Titre très long
            "author": "B" * 100,  # Auteur très long
            "group": "TESTGROUP",
            "date": "20250124",
        }
        
        nfo = service.generate_nfo(metadata)
        lines = nfo.split("\n")
        
        for line in lines:
            # Exclure les lignes vides et les lignes de séparation
            if line.strip() and not line.strip().startswith("="):
                assert len(line) <= 80, f"Ligne dépasse 80 colonnes: {len(line)} caractères"

    def test_format_line_long_text(self):
        """Test formatage ligne avec texte long (coupure intelligente)."""
        service = NfoGeneratorService()
        long_text = "A" * 100
        
        formatted = service._format_line(long_text, max_width=80)
        
        # Vérifier que toutes les lignes résultantes respectent la limite
        # formatted est une liste, pas une chaîne
        assert isinstance(formatted, list)
        for line in formatted:
            assert len(line) <= 80

    def test_generate_header(self):
        """Test génération header NFO."""
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book",
            "group": "TESTGROUP",
        }
        
        header = service._generate_header(metadata)
        
        assert isinstance(header, list)
        assert len(header) > 0
        # Vérifier contrainte 80 colonnes
        for line in header:
            assert len(line) <= 80

    def test_generate_body(self):
        """Test génération body NFO avec métadonnées."""
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "isbn": "1234567890",
            "year": "2025",
            "language": "English",
        }
        
        body = service._generate_body(metadata)
        
        assert isinstance(body, list)
        assert len(body) > 0
        # Vérifier contrainte 80 colonnes
        for line in body:
            assert len(line) <= 80

    def test_generate_nfo_with_special_characters(self):
        """Test génération NFO avec caractères spéciaux UTF-8."""
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book avec accents é à ç",
            "author": "Auteur français",
            "group": "TESTGROUP",
            "date": "20250124",
        }
        
        nfo = service.generate_nfo(metadata)
        
        # Vérifier que les caractères spéciaux sont présents
        assert "é" in nfo or "é" in nfo.encode("utf-8").decode("utf-8")
        assert "à" in nfo or "à" in nfo.encode("utf-8").decode("utf-8")

    def test_generate_nfo_empty_metadata(self):
        """Test génération NFO avec métadonnées vides."""
        service = NfoGeneratorService()
        metadata = {}
        
        nfo = service.generate_nfo(metadata)
        
        # Doit générer un NFO minimal même avec métadonnées vides
        assert isinstance(nfo, str)
        assert len(nfo) > 0

    def test_generate_nfo_with_template(self):
        """Test génération NFO avec template personnalisé."""
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book",
            "author": "Test Author",
            "group": "TESTGROUP",
            "date": "20250124",
        }
        template = "Title: {title}\nAuthor: {author}"
        
        nfo = service.generate_nfo(metadata, template=template)
        
        assert "Title: Test Book" in nfo
        assert "Author: Test Author" in nfo

    def test_format_line_preserves_short_lines(self):
        """Test que les lignes courtes ne sont pas modifiées."""
        service = NfoGeneratorService()
        short_text = "Short line"
        
        formatted = service._format_line(short_text, max_width=80)
        
        # formatted retourne une liste
        assert isinstance(formatted, list)
        assert len(formatted) == 1
        assert formatted[0] == short_text

    def test_format_line_multiple_lines(self):
        """Test formatage texte avec plusieurs lignes."""
        service = NfoGeneratorService()
        multi_line_text = "Line 1\n" + "A" * 100 + "\nLine 3"
        
        formatted = service._format_line(multi_line_text, max_width=80)
        
        # Vérifier que toutes les lignes respectent la limite
        # formatted est une liste, pas une chaîne
        assert isinstance(formatted, list)
        for line in formatted:
            if line.strip():  # Ignorer lignes vides
                assert len(line) <= 80

    def test_generate_nfo_structure(self):
        """Test structure générale du NFO généré."""
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book",
            "author": "Test Author",
            "group": "TESTGROUP",
            "date": "20250124",
        }
        
        nfo = service.generate_nfo(metadata)
        
        # Vérifier structure basique
        assert isinstance(nfo, str)
        assert len(nfo) > 0
        # Vérifier encodage UTF-8
        assert nfo.encode("utf-8").decode("utf-8") == nfo

    def test_generate_nfo_with_none_values(self):
        """Test génération NFO avec valeurs None dans métadonnées."""
        service = NfoGeneratorService()
        metadata = {
            "title": "Test Book",
            "author": None,
            "publisher": None,
            "group": "TESTGROUP",
            "date": "20250124",
        }
        
        nfo = service.generate_nfo(metadata)
        
        # Ne doit pas lever d'exception
        assert isinstance(nfo, str)
        assert len(nfo) > 0

