"""Pytest configuration and shared fixtures."""
import pytest
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope='session')
def app():
    """Create test application."""
    # Will be implemented when Flask app factory is created
    # For now, return None as placeholder
    return None


@pytest.fixture
def client(app):
    """Test client."""
    if app is None:
        pytest.skip("Flask app not yet implemented")
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Authenticated headers."""
    # Will be implemented when auth is set up
    # For now, return empty dict
    return {}


@pytest.fixture(autouse=True)
def clean_db(app):
    """Clean database before each test."""
    # Will be implemented when DB is set up
    yield
    # Cleanup after test

