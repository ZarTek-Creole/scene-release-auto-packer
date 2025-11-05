"""Test complet du RuleParserService avec résultats détaillés pour browser MCP."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ajouter le répertoire racine au path Python
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from web.services.rule_parser import RuleParserService


def test_rule_parser_comprehensive() -> dict:
    """Test complet du RuleParserService avec tous les cas."""
    parser = RuleParserService()
    
    # Règle complète [2022] eBOOK
    rule_content = """
    [2022] eBOOK

    OTHER
    PDF, EPUB, CBZ, Kindle (.azw, .kf8), MOBIPOCKET (.prc, .mobi)

    PACKAGING
    ZIP+DIZ obligatoire
    .nfo file obligatoire

    DIRNAMING
    GroupName-Author-Title-Format-Language-Year-ISBN-eBook
    """
    
    results = {
        "test_complete_parsing": {},
        "test_extract_formats": {},
        "test_extract_naming": {},
        "test_extract_required_files": {},
        "test_extract_packaging_rules": {},
    }
    
    # Test 1: Parsing complet
    try:
        result = parser.parse_ebook_rule_2022(rule_content)
        results["test_complete_parsing"] = {
            "success": True,
            "file_formats": result["file_formats"],
            "naming_format": result["naming"]["format"],
            "required_files": result["required_files"],
            "packaging_zip_sizes": len(result["packaging"]["zip"]["allowed_sizes"]),
        }
    except Exception as e:
        results["test_complete_parsing"] = {"success": False, "error": str(e)}
    
    # Test 2: Extraction formats
    try:
        formats = parser.extract_file_formats(rule_content)
        results["test_extract_formats"] = {
            "success": True,
            "formats": formats,
            "count": len(formats),
        }
    except Exception as e:
        results["test_extract_formats"] = {"success": False, "error": str(e)}
    
    # Test 3: Extraction nommage
    try:
        naming = parser.extract_naming_format(rule_content)
        results["test_extract_naming"] = {
            "success": True,
            "format": naming["format"],
            "components": list(naming["components"].keys()),
            "max_length": naming["max_length"],
        }
    except Exception as e:
        results["test_extract_naming"] = {"success": False, "error": str(e)}
    
    # Test 4: Extraction fichiers requis
    try:
        required = parser.extract_required_files(rule_content)
        results["test_extract_required_files"] = {
            "success": True,
            "required_files": required,
            "count": len(required),
        }
    except Exception as e:
        results["test_extract_required_files"] = {"success": False, "error": str(e)}
    
    # Test 5: Extraction règles packaging
    try:
        packaging = parser.extract_packaging_rules(rule_content)
        results["test_extract_packaging_rules"] = {
            "success": True,
            "zip_required": packaging["zip"]["required"],
            "zip_sizes_count": len(packaging["zip"]["allowed_sizes"]),
            "nfo_max_width": packaging["nfo"]["max_width"],
            "diz_max_width": packaging["diz"]["max_width"],
            "diz_max_height": packaging["diz"]["max_height"],
        }
    except Exception as e:
        results["test_extract_packaging_rules"] = {"success": False, "error": str(e)}
    
    return results


if __name__ == "__main__":
    results = test_rule_parser_comprehensive()
    print(json.dumps(results, indent=2, ensure_ascii=False))

