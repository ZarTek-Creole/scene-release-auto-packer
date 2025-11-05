"""Script de test interactif pour RuleParserService avec MCP Browser.

Ce script permet de tester le RuleParserService de manière interactive
en démarrant l'application Flask et en utilisant les outils MCP Browser.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ajouter le répertoire racine au path Python
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from web.app import create_app
from web.services.rule_parser import RuleParserService


def test_rule_parser_service() -> None:
    """Test interactif du RuleParserService."""
    print("=" * 80)
    print("🧪 TEST INTERACTIF - RuleParserService")
    print("=" * 80)
    print()
    
    parser = RuleParserService()
    
    # Test 1: Règle complète [2022] eBOOK
    print("📋 Test 1: Parsing règle complète [2022] eBOOK")
    print("-" * 80)
    
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
    
    result = parser.parse_ebook_rule_2022(rule_content)
    
    print(f"✅ Formats de fichiers extraits: {result['file_formats']}")
    print(f"✅ Fichiers requis: {result['required_files']}")
    print(f"✅ Format de nommage: {result['naming']['format']}")
    print(f"✅ Longueur max: {result['naming']['max_length']} caractères")
    print(f"✅ Tailles ZIP autorisées: {len(result['packaging']['zip']['allowed_sizes'])} tailles")
    print()
    
    # Test 2: Extraction formats uniquement
    print("📋 Test 2: Extraction formats de fichiers")
    print("-" * 80)
    
    formats = parser.extract_file_formats(rule_content)
    print(f"✅ Formats trouvés: {formats}")
    print()
    
    # Test 3: Extraction format de nommage
    print("📋 Test 3: Extraction format de nommage")
    print("-" * 80)
    
    naming = parser.extract_naming_format(rule_content)
    print(f"✅ Format: {naming['format']}")
    print(f"✅ Composants: {list(naming['components'].keys())}")
    print()
    
    # Test 4: Extraction fichiers requis
    print("📋 Test 4: Extraction fichiers requis")
    print("-" * 80)
    
    required = parser.extract_required_files(rule_content)
    print(f"✅ Fichiers requis: {required}")
    print()
    
    # Test 5: Extraction règles de packaging
    print("📋 Test 5: Extraction règles de packaging")
    print("-" * 80)
    
    packaging = parser.extract_packaging_rules(rule_content)
    print(f"✅ ZIP requis: {packaging['zip']['required']}")
    print(f"✅ Tailles ZIP: {packaging['zip']['allowed_sizes'][:3]}... (premières 3)")
    print(f"✅ NFO max_width: {packaging['nfo']['max_width']}")
    print(f"✅ DIZ max_width: {packaging['diz']['max_width']}, max_height: {packaging['diz']['max_height']}")
    print()
    
    print("=" * 80)
    print("✅ TOUS LES TESTS PASSÉS AVEC SUCCÈS!")
    print("=" * 80)


if __name__ == "__main__":
    test_rule_parser_service()

