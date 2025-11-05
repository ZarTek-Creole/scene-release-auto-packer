"""Tests for Config API endpoints (Phase 1)."""

from __future__ import annotations

from web.extensions import db
from web.models import Configuration, Role, User


def test_list_configurations(client, app):
    """Test listing configurations."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        # Create configurations
        config1 = Configuration(key="test.key1", value="value1", category="test")
        config2 = Configuration(key="test.key2", value="value2", category="test")
        db.session.add_all([config1, config2])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/config", headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert "configurations" in data
        assert len(data["configurations"]) >= 2


def test_list_configurations_with_category_filter(client, app):
    """Test listing configurations with category filter."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config1 = Configuration(key="test.key1", value="value1", category="test")
        config2 = Configuration(key="prod.key1", value="value1", category="prod")
        db.session.add_all([config1, config2])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/config?category=test", headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert all(c["category"] == "test" for c in data["configurations"])


def test_list_configurations_with_key_filter(client, app):
    """Test listing configurations with key filter."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config1 = Configuration(key="test.key1", value="value1")
        config2 = Configuration(key="test.key2", value="value2")
        db.session.add_all([config1, config2])
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/config?key=key1", headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert all("key1" in c["key"] for c in data["configurations"])


def test_get_configuration(client, app):
    """Test getting configuration by ID."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config = Configuration(key="test.key", value="test_value", category="test")
        db.session.add(config)
        db.session.commit()
        config_id = config.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(f"/api/config/{config_id}", headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["configuration"]["key"] == "test.key"
        assert data["configuration"]["value"] == "test_value"


def test_get_configuration_not_found(client, app):
    """Test getting non-existent configuration."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/config/99999", headers=headers)
        assert response.status_code == 404


def test_get_configuration_by_key(client, app):
    """Test getting configuration by key."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config = Configuration(key="test.key", value="test_value")
        db.session.add(config)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/config/key/test.key", headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["configuration"]["key"] == "test.key"


def test_get_configuration_by_key_not_found(client, app):
    """Test getting configuration by non-existent key."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/config/key/nonexistent.key", headers=headers)
        assert response.status_code == 404


def test_create_configuration(client, app):
    """Test creating configuration."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/api/config",
            json={
                "key": "new.key",
                "value": "new_value",
                "category": "test",
                "description": "Test description",
            },
            headers=headers,
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["configuration"]["key"] == "new.key"
        assert data["configuration"]["value"] == "new_value"


def test_create_configuration_missing_fields(client, app):
    """Test creating configuration with missing required fields."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Missing key
        response = client.post(
            "/api/config",
            json={"value": "value"},
            headers=headers,
        )
        assert response.status_code == 400

        # Missing value
        response = client.post(
            "/api/config",
            json={"key": "test.key"},
            headers=headers,
        )
        assert response.status_code == 400


def test_create_configuration_duplicate_key(client, app):
    """Test creating configuration with duplicate key."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config = Configuration(key="existing.key", value="value1")
        db.session.add(config)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.post(
            "/api/config",
            json={"key": "existing.key", "value": "value2"},
            headers=headers,
        )
        assert response.status_code == 400
        assert "already exists" in response.get_json()["message"].lower()


def test_update_configuration(client, app):
    """Test updating configuration."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config = Configuration(key="test.key", value="old_value")
        db.session.add(config)
        db.session.commit()
        config_id = config.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(
            f"/api/config/{config_id}",
            json={"value": "new_value", "description": "Updated"},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["configuration"]["value"] == "new_value"


def test_update_configuration_not_found(client, app):
    """Test updating non-existent configuration."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(
            "/api/config/99999",
            json={"value": "new_value"},
            headers=headers,
        )
        assert response.status_code == 404


def test_update_configuration_duplicate_key(client, app):
    """Test updating configuration with duplicate key."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config1 = Configuration(key="key1", value="value1")
        config2 = Configuration(key="key2", value="value2")
        db.session.add_all([config1, config2])
        db.session.commit()
        config2_id = config2.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Try to change config2's key to key1
        response = client.put(
            f"/api/config/{config2_id}",
            json={"key": "key1"},
            headers=headers,
        )
        assert response.status_code == 400
        assert "already exists" in response.get_json()["message"].lower()


def test_delete_configuration(client, app):
    """Test deleting configuration."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config = Configuration(key="test.key", value="value")
        db.session.add(config)
        db.session.commit()
        config_id = config.id

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete(f"/api/config/{config_id}", headers=headers)
        assert response.status_code == 200

        # Verify deleted
        deleted_config = db.session.get(Configuration, config_id)
        assert deleted_config is None


def test_delete_configuration_not_found(client, app):
    """Test deleting non-existent configuration."""
    with app.app_context():
        # Create user with admin role
        admin_role = Role.query.filter_by(name="admin").first()
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        if admin_role:
            user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        login_response = client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password"},
        )
        token = login_response.get_json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete("/api/config/99999", headers=headers)
        assert response.status_code == 404
