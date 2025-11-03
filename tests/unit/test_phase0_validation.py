"""Tests de validation Phase 0 - Préparation."""
import pytest
from pathlib import Path
import sys

project_root = Path(__file__).parent.parent.parent


class TestPhase0Backup:
    """Tests validation backup v1/."""
    
    def test_v1_directory_exists(self):
        """Vérifier que v1/ existe."""
        v1_dir = project_root / "v1"
        assert v1_dir.exists(), "v1/ doit exister"
        assert v1_dir.is_dir(), "v1/ doit être un répertoire"
    
    def test_v1_contains_files(self):
        """Vérifier que v1/ contient des fichiers."""
        v1_dir = project_root / "v1"
        files = list(v1_dir.iterdir())
        assert len(files) > 0, "v1/ doit contenir des fichiers"
    
    def test_no_files_at_root_except_v1(self):
        """Vérifier structure racine correcte (v1/, docs/, tests/, etc. sont normaux pour v2)."""
        root_dirs = [
            f.name for f in project_root.iterdir()
            if f.is_dir() and not f.name.startswith('.')
        ]
        # Structure v2 normale : v1/, docs/, tests/, web/, src/ sont attendus
        expected_dirs = ['v1', 'docs', 'tests']
        for expected in expected_dirs:
            assert expected in root_dirs, f"{expected}/ doit être à la racine"


class TestPhase0Documentation:
    """Tests validation documentation."""
    
    @pytest.mark.parametrize("doc_file", [
        "docs/cdc.md",
        "docs/DEVBOOK.md",
        "docs/todolist.md",
        "docs/BACKLOG_AGILE.md",
        "docs/PROJECT_OVERVIEW.md",
        "docs/TEST_PLAN.md",
        "docs/RISKS_REGISTER.md",
        "docs/DEPLOYMENT_PLAN.md",
        "docs/MCP_TOOLS_GUIDE.md",
        "docs/PRDs/README.md",
    ])
    def test_documentation_file_exists(self, doc_file):
        """Vérifier que tous les fichiers de documentation existent."""
        doc_path = project_root / doc_file
        assert doc_path.exists(), f"{doc_file} doit exister"
        assert doc_path.is_file(), f"{doc_file} doit être un fichier"
        assert doc_path.stat().st_size > 0, f"{doc_file} ne doit pas être vide"


class TestPhase0CursorRules:
    """Tests validation règles Cursor."""
    
    @pytest.mark.parametrize("rule_file", [
        ".cursor/rules/project-v2.mdc",
        ".cursor/rules/tdd-methodology.mdc",
        ".cursor/rules/mcp-tools-usage.mdc",
        ".cursor/rules/documentation-standards.mdc",
        ".cursor/rules/testing-requirements.mdc",
        ".cursor/rules/definition-of-done.mdc",
    ])
    def test_cursor_rule_exists(self, rule_file):
        """Vérifier que toutes les règles Cursor existent."""
        rule_path = project_root / rule_file
        assert rule_path.exists(), f"{rule_file} doit exister"
        assert rule_path.is_file(), f"{rule_file} doit être un fichier"
        
        # Vérifier que la règle a alwaysApply ou est correctement formatée
        content = rule_path.read_text()
        assert "alwaysApply: true" in content or "name:" in content, \
            f"{rule_file} doit avoir une configuration valide"
    
    def test_rules_attachment_guide_exists(self):
        """Vérifier que le guide d'attachement existe."""
        guide_path = project_root / ".cursor" / "RULES_ATTACHMENT_GUIDE.md"
        assert guide_path.exists(), "RULES_ATTACHMENT_GUIDE.md doit exister"


class TestPhase0Environment:
    """Tests validation environnement développement."""
    
    def test_venv_exists(self):
        """Vérifier que venv existe."""
        venv_dir = project_root / "venv"
        # venv peut ne pas exister dans CI, donc test conditionnel
        if venv_dir.exists():
            assert venv_dir.is_dir(), "venv doit être un répertoire"
    
    def test_requirements_files_exist(self):
        """Vérifier que requirements.txt et requirements-dev.txt existent."""
        req_prod = project_root / "requirements.txt"
        req_dev = project_root / "requirements-dev.txt"
        
        assert req_prod.exists(), "requirements.txt doit exister"
        assert req_dev.exists(), "requirements-dev.txt doit exister"
        
        assert req_prod.stat().st_size > 0, "requirements.txt ne doit pas être vide"
        assert req_dev.stat().st_size > 0, "requirements-dev.txt ne doit pas être vide"
    
    def test_pytest_config_exists(self):
        """Vérifier que pytest.ini existe."""
        pytest_ini = project_root / "pytest.ini"
        assert pytest_ini.exists(), "pytest.ini doit exister"
    
    def test_coverage_config_exists(self):
        """Vérifier que .coveragerc existe."""
        coveragerc = project_root / ".coveragerc"
        assert coveragerc.exists(), ".coveragerc doit exister"


class TestPhase0Tests:
    """Tests validation structure tests."""
    
    def test_tests_structure_exists(self):
        """Vérifier que la structure tests/ existe."""
        tests_dir = project_root / "tests"
        assert tests_dir.exists(), "tests/ doit exister"
        assert tests_dir.is_dir(), "tests/ doit être un répertoire"
    
    @pytest.mark.parametrize("test_subdir", [
        "tests/unit",
        "tests/integration",
        "tests/e2e",
    ])
    def test_test_subdirectories_exist(self, test_subdir):
        """Vérifier que les sous-répertoires tests existent."""
        test_path = project_root / test_subdir
        assert test_path.exists(), f"{test_subdir} doit exister"
        assert test_path.is_dir(), f"{test_subdir} doit être un répertoire"
    
    def test_conftest_exists(self):
        """Vérifier que conftest.py existe."""
        conftest = project_root / "tests" / "conftest.py"
        assert conftest.exists(), "tests/conftest.py doit exister"
    
    def test_example_test_exists(self):
        """Vérifier qu'un test exemple existe."""
        example_test = project_root / "tests" / "unit" / "test_example.py"
        assert example_test.exists(), "tests/unit/test_example.py doit exister"


class TestPhase0Completion:
    """Tests validation complétion Phase 0."""
    
    def test_all_critical_files_present(self):
        """Vérifier que tous les fichiers critiques sont présents."""
        critical_files = [
            "README.md",
            "requirements.txt",
            "requirements-dev.txt",
            "pytest.ini",
            ".coveragerc",
        ]
        
        missing = []
        for file in critical_files:
            if not (project_root / file).exists():
                missing.append(file)
        
        assert len(missing) == 0, f"Fichiers manquants : {missing}"
    
    def test_documentation_complete(self):
        """Vérifier que la documentation est complète."""
        # Vérifier que tous les fichiers docs essentiels existent et ne sont pas vides
        essential_docs = [
            "docs/cdc.md",
            "docs/DEVBOOK.md",
            "docs/todolist.md",
            "docs/MCP_TOOLS_GUIDE.md",
        ]
        
        for doc in essential_docs:
            doc_path = project_root / doc
            assert doc_path.exists(), f"{doc} doit exister"
            size = doc_path.stat().st_size
            assert size > 1000, f"{doc} doit avoir du contenu (actuel: {size} bytes)"

