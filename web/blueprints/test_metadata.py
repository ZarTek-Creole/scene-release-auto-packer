"""Blueprint pour tests MetadataExtractionService.

Endpoints de test pour valider l'extraction de métadonnées depuis fichiers eBook.
"""

from pathlib import Path
from typing import Any

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from web.services.metadata import MetadataExtractionService

test_metadata_bp = Blueprint("test_metadata", __name__)


@test_metadata_bp.route("/test/metadata-extraction", methods=["POST"])
@jwt_required(optional=True)  # type: ignore[misc]  # MyPy: Flask decorators not fully typed  # Optionnel pour faciliter les tests
def test_metadata_extraction() -> tuple[dict[str, Any], int]:
    """Test extraction métadonnées depuis fichier uploadé.

    Args:
        request.files['file']: Fichier eBook à analyser.

    Returns:
        JSON avec métadonnées extraites.
    """
    if "file" not in request.files:
        return {"error": "Aucun fichier fourni", "success": False}, 400

    file = request.files["file"]
    if file.filename == "":
        return {"error": "Fichier vide", "success": False}, 400

    try:
        # Sauvegarder temporairement le fichier
        import tempfile

        if file.filename is None:
            return {"error": "No filename provided", "success": False}, 400

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=Path(file.filename).suffix
        ) as tmp_file:
            file.save(tmp_file.name)
            tmp_path = Path(tmp_file.name)

        try:
            # Extraire métadonnées
            service = MetadataExtractionService()
            metadata = service.extract_metadata(tmp_path, calculate_checksums=True)

            return {
                "success": True,
                "metadata": metadata,
            }, 200
        finally:
            # Nettoyer fichier temporaire
            if tmp_path.exists():
                tmp_path.unlink()
    except Exception as e:
        return {
            "error": str(e),
            "success": False,
        }, 500


@test_metadata_bp.route("/test/metadata-extraction/normalize", methods=["POST"])
@jwt_required(optional=True)  # type: ignore[misc]  # MyPy: Flask decorators not fully typed
def test_normalize_metadata() -> tuple[dict[str, Any], int]:
    """Test normalisation métadonnées.

    Args:
        request.json['metadata']: Métadonnées brutes à normaliser.

    Returns:
        JSON avec métadonnées normalisées.
    """
    data = request.get_json()
    if not data or "metadata" not in data:
        return {"error": "Métadonnées non fournies", "success": False}, 400

    try:
        service = MetadataExtractionService()
        normalized = service._normalize_metadata(data["metadata"])

        return {
            "success": True,
            "normalized": normalized,
        }, 200
    except Exception as e:
        return {
            "error": str(e),
            "success": False,
        }, 500


@test_metadata_bp.route("/test/metadata-extraction/checksums", methods=["POST"])
@jwt_required(optional=True)  # type: ignore[misc]  # MyPy: Flask decorators not fully typed
def test_calculate_checksums() -> tuple[dict[str, Any], int]:
    """Test calcul checksums depuis fichier uploadé.

    Args:
        request.files['file']: Fichier à analyser.

    Returns:
        JSON avec checksums calculés.
    """
    if "file" not in request.files:
        return {"error": "Aucun fichier fourni", "success": False}, 400

    file = request.files["file"]
    if file.filename == "":
        return {"error": "Fichier vide", "success": False}, 400

    try:
        # Sauvegarder temporairement le fichier
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            file.save(tmp_file.name)
            tmp_path = Path(tmp_file.name)

        try:
            # Calculer checksums
            service = MetadataExtractionService()
            checksums = service._calculate_checksums(tmp_path)

            return {
                "success": True,
                "checksums": checksums,
                "file_size": tmp_path.stat().st_size,
            }, 200
        finally:
            # Nettoyer fichier temporaire
            if tmp_path.exists():
                tmp_path.unlink()
    except Exception as e:
        return {
            "error": str(e),
            "success": False,
        }, 500
