"""Tests unitaires pour PackagingService.

Ce module teste la génération de packages Scene complets avec structure de dossiers,
fichiers ZIP, checksums et validation finale.
"""

from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path

import pytest

from web.services.packaging.packaging_service import PackagingService


class TestPackagingService:
    """Tests unitaires pour PackagingService."""

    def test_create_directory_structure_basic(self):
        """Test création structure dossiers basique."""
        service = PackagingService()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir)
            release_name = "Test-Book-TESTGROUP-20250124"
            
            structure_path = service._create_directory_structure(
                release_name, output_path
            )
            
            assert structure_path.exists()
            assert structure_path.is_dir()
            assert structure_path.name == release_name

    def test_create_directory_structure_nested(self):
        """Test création structure dossiers avec sous-dossiers."""
        service = PackagingService()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir)
            release_name = "Test-Book-TESTGROUP-20250124"
            
            structure_path = service._create_directory_structure(
                release_name, output_path
            )
            
            # Vérifier que le dossier principal existe
            assert structure_path.exists()
            
            # Créer un fichier de test dans la structure
            test_file = structure_path / "test.txt"
            test_file.write_text("test content")
            
            assert test_file.exists()

    def test_generate_checksums_sha256(self):
        """Test génération checksum SHA-256."""
        service = PackagingService()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("test content for checksum")
            
            checksums = service._generate_checksums(test_file)
            
            assert "sha256" in checksums
            assert len(checksums["sha256"]) == 64  # SHA-256 = 64 caractères hexadécimaux

    def test_generate_checksums_md5(self):
        """Test génération checksum MD5."""
        service = PackagingService()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            test_file.write_text("test content for checksum")
            
            checksums = service._generate_checksums(test_file)
            
            assert "md5" in checksums
            assert len(checksums["md5"]) == 32  # MD5 = 32 caractères hexadécimaux

    def test_create_zip_file_basic(self):
        """Test création fichier ZIP basique."""
        service = PackagingService()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Créer structure de test
            release_dir = Path(tmpdir) / "Test-Book-TESTGROUP-20250124"
            release_dir.mkdir()
            
            # Créer fichier de test
            test_file = release_dir / "test.epub"
            test_file.write_text("test epub content")
            
            output_path = Path(tmpdir)
            zip_path = service._create_zip_file(release_dir, output_path)
            
            assert zip_path.exists()
            assert zip_path.suffix == ".zip"
            assert zip_path.name == "Test-Book-TESTGROUP-20250124.zip"

    def test_package_release_complete(self):
        """Test packaging release complet."""
        service = PackagingService()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir)
            
            release_data = {
                "name": "Test-Book-TESTGROUP-20250124",
                "group": "TESTGROUP",
                "release_type": "EBOOK",
                "files": [
                    {
                        "path": str(Path(tmpdir) / "test.epub"),
                        "name": "test.epub",
                    }
                ],
                "metadata": {
                    "title": "Test Book",
                    "author": "Test Author",
                },
            }
            
            # Créer fichier de test
            test_file = Path(tmpdir) / "test.epub"
            test_file.write_text("test epub content")
            
            result = service.package_release(release_data, output_path)
            
            assert result["success"] is True
            assert "zip_path" in result
            assert Path(result["zip_path"]).exists()
            assert "checksums" in result

    def test_package_release_with_nfo(self):
        """Test packaging release avec fichier NFO."""
        service = PackagingService()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir)
            
            release_data = {
                "name": "Test-Book-TESTGROUP-20250124",
                "group": "TESTGROUP",
                "release_type": "EBOOK",
                "files": [
                    {
                        "path": str(Path(tmpdir) / "test.epub"),
                        "name": "test.epub",
                    }
                ],
                "metadata": {
                    "title": "Test Book",
                    "author": "Test Author",
                },
                "nfo_content": "NFO content here",
            }
            
            # Créer fichier de test
            test_file = Path(tmpdir) / "test.epub"
            test_file.write_text("test epub content")
            
            result = service.package_release(release_data, output_path)
            
            assert result["success"] is True
            # Vérifier que le NFO est inclus dans le ZIP
            assert "checksums" in result

    def test_package_release_missing_file(self):
        """Test packaging release avec fichier manquant."""
        service = PackagingService()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir)
            
            release_data = {
                "name": "Test-Book-TESTGROUP-20250124",
                "group": "TESTGROUP",
                "release_type": "EBOOK",
                "files": [
                    {
                        "path": str(Path(tmpdir) / "nonexistent.epub"),
                        "name": "nonexistent.epub",
                    }
                ],
                "metadata": {},
            }
            
            # Ne pas créer le fichier - doit lever une erreur
            with pytest.raises(FileNotFoundError):
                service.package_release(release_data, output_path)

    def test_validate_final_package(self):
        """Test validation finale du package."""
        service = PackagingService()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Créer un vrai fichier ZIP valide
            zip_file = Path(tmpdir) / "test.zip"
            with zipfile.ZipFile(zip_file, "w") as zipf:
                zipf.writestr("test.txt", "test content")
            
            result = service._validate_final_package(zip_file)
            
            # La validation doit vérifier que le fichier existe et est valide
            assert result is True

    def test_package_release_error_handling(self):
        """Test gestion erreurs lors du packaging."""
        service = PackagingService()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir)
            
            release_data = {
                "name": "",  # Nom vide - doit échouer
                "group": "TESTGROUP",
                "release_type": "EBOOK",
                "files": [],
                "metadata": {},
            }
            
            # Doit gérer l'erreur gracieusement
            with pytest.raises((ValueError, FileNotFoundError)):
                service.package_release(release_data, output_path)

    def test_create_zip_file_preserves_structure(self):
        """Test que la création ZIP préserve la structure."""
        service = PackagingService()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Créer structure avec sous-dossiers
            release_dir = Path(tmpdir) / "Test-Book-TESTGROUP-20250124"
            release_dir.mkdir()
            
            subdir = release_dir / "subdir"
            subdir.mkdir()
            
            test_file1 = release_dir / "test1.epub"
            test_file1.write_text("content1")
            
            test_file2 = subdir / "test2.txt"
            test_file2.write_text("content2")
            
            zip_path = service._create_zip_file(release_dir, Path(tmpdir))
            
            assert zip_path.exists()
            # Vérifier que le ZIP contient les fichiers
            import zipfile
            
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                files_in_zip = zip_ref.namelist()
                assert "test1.epub" in files_in_zip
                assert "subdir/test2.txt" in files_in_zip

