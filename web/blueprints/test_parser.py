"""Route de test pour RuleParserService accessible via API.

Cette route permet de tester le RuleParserService via l'interface web.
"""

from __future__ import annotations

from typing import Any

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from web.services.rule import RuleParserService

test_parser_bp = Blueprint("test_parser", __name__)


@test_parser_bp.route("/test/rule-parser", methods=["POST"])
@jwt_required(optional=True)  # type: ignore[misc]  # MyPy: Flask decorators not fully typed
def test_rule_parser() -> tuple[dict[str, Any], int]:
    """Test du RuleParserService avec contenu de règle fourni.

    Body JSON:
        {
            "rule_content": "contenu de la règle Scene..."
        }

    Returns:
        Résultat du parsing avec toutes les sections extraites.
    """
    data = request.get_json() or {}
    rule_content = data.get("rule_content", "")

    if not rule_content:
        return {"error": "rule_content requis dans le body"}, 400

    parser = RuleParserService()

    try:
        result = parser.parse_ebook_rule_2022(rule_content)

        return {
            "success": True,
            "result": {
                "file_formats": result["file_formats"],
                "naming": result["naming"],
                "required_files": result["required_files"],
                "packaging": result["packaging"],
            },
        }, 200
    except Exception as e:
        return {"error": str(e), "success": False}, 500


@test_parser_bp.route("/test/rule-parser/extract-formats", methods=["POST"])
@jwt_required(optional=True)  # type: ignore[misc]  # MyPy: Flask decorators not fully typed
def test_extract_formats() -> tuple[dict[str, Any], int]:
    """Test extraction formats de fichiers uniquement."""
    data = request.get_json() or {}
    rule_content = data.get("rule_content", "")

    parser = RuleParserService()
    formats = parser.extract_file_formats(rule_content)

    return {"success": True, "formats": formats}, 200


@test_parser_bp.route("/test/rule-parser/extract-naming", methods=["POST"])
@jwt_required(optional=True)  # type: ignore[misc]  # MyPy: Flask decorators not fully typed
def test_extract_naming() -> tuple[dict[str, Any], int]:
    """Test extraction format de nommage uniquement."""
    data = request.get_json() or {}
    rule_content = data.get("rule_content", "")

    parser = RuleParserService()
    naming = parser.extract_naming_format(rule_content)

    return {"success": True, "naming": naming}, 200
