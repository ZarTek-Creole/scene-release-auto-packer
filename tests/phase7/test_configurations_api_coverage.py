"""Additional tests for Configurations API to achieve ≥90% coverage."""

from __future__ import annotations

from web.extensions import db
from web.models import Configuration, Permission, Role, User


def test_list_configurations_user_not_found(client) -> None:
    """Test listing configurations with invalid user (404)."""
    # Mock invalid JWT token - this would normally be handled by JWT middleware
    # For this test, we'll create a user and then delete it
    with client.application.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Delete user to simulate user not found
    with client.application.app_context():
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    # Try to list configurations - should fail with 401/404
    response = client.get(
        "/api/config",
        headers={"Authorization": f"Bearer {token}"},
    )
    # JWT token is valid but user doesn't exist anymore
    assert response.status_code in [404, 401]


def test_list_configurations_permission_denied(client) -> None:
    """Test listing configurations without read permission (403)."""
    with client.application.app_context():
        db.create_all()
        # Create user without permissions
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # List configurations - should fail with permission denied
    response = client.get(
        "/api/config",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Permission denied"


def test_list_configurations_with_key_filter(client) -> None:
    """Test listing configurations filtered by key."""
    with client.application.app_context():
        db.create_all()
        # Create admin role and assign to user
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="Administrator")
            db.session.add(admin_role)
        db.session.add(admin_role)

        read_config_permission = db.session.query(Permission).filter_by(
            resource="config", action="read"
        ).first()
        if not read_config_permission:
            read_config_permission = Permission(
                resource="config", action="read")
            db.session.add(read_config_permission)

        # Check if permission already attached to avoid duplicate
        if read_config_permission not in admin_role.permissions.all():
            admin_role.permissions.append(read_config_permission)

        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config1 = Configuration(
            key="app.name", value="Scene Packer", category="app")
        config2 = Configuration(
            key="app.version", value="2.0.0", category="app")
        config3 = Configuration(
            key="db.host", value="localhost", category="database")
        db.session.add_all([config1, config2, config3])
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # List configurations filtered by key (partial match)
    response = client.get(
        "/api/config?key=app.",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["configurations"]) == 2
    assert all("app." in config["key"] for config in data["configurations"])


def test_get_configuration_by_key_not_found(client) -> None:
    """Test getting configuration by key that doesn't exist (404)."""
    with client.application.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Get configuration by non-existent key
    response = client.get(
        "/api/config/key/nonexistent.key",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.get_json()["message"] == "Configuration not found"


def test_create_configuration_permission_denied(client) -> None:
    """Test creating configuration without write permission (403)."""
    with client.application.app_context():
        db.create_all()
        # Create user without permissions
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Create configuration - should fail with permission denied
    response = client.post(
        "/api/config",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "key": "app.debug",
            "value": "false",
            "category": "app",
        },
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Permission denied"


def test_create_configuration_no_data(client) -> None:
    """Test creating configuration without data (400)."""
    with client.application.app_context():
        db.create_all()
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="Administrator")
            db.session.add(admin_role)
        db.session.add(admin_role)

        write_config_permission = db.session.query(Permission).filter_by(
            resource="config", action="write"
        ).first()
        if not write_config_permission:
            write_config_permission = Permission(
                resource="config", action="write")
            db.session.add(write_config_permission)

        # Check if permission already attached to avoid duplicate
        if write_config_permission not in admin_role.permissions.all():
            admin_role.permissions.append(write_config_permission)

        user = User(username="admin", email="admin@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Create configuration without data (don't send json parameter)
    response = client.post(
        "/api/config",
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json"},
        data="{}",
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data is not None
    assert data["message"] == "No data provided"


def test_create_configuration_missing_key(client) -> None:
    """Test creating configuration missing required field key (400)."""
    with client.application.app_context():
        db.create_all()
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="Administrator")
            db.session.add(admin_role)
        db.session.add(admin_role)

        write_config_permission = db.session.query(Permission).filter_by(
            resource="config", action="write"
        ).first()
        if not write_config_permission:
            write_config_permission = Permission(
                resource="config", action="write")
            db.session.add(write_config_permission)

        # Check if permission already attached to avoid duplicate
        if write_config_permission not in admin_role.permissions.all():
            admin_role.permissions.append(write_config_permission)

        user = User(username="admin", email="admin@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Create configuration missing key
    response = client.post(
        "/api/config",
        headers={"Authorization": f"Bearer {token}"},
        json={"value": "some value"},
    )

    assert response.status_code == 400
    assert "Missing required field: key" in response.get_json()["message"]


def test_create_configuration_missing_value(client) -> None:
    """Test creating configuration missing required field value (400)."""
    with client.application.app_context():
        db.create_all()
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="Administrator")
            db.session.add(admin_role)
        db.session.add(admin_role)

        write_config_permission = db.session.query(Permission).filter_by(
            resource="config", action="write"
        ).first()
        if not write_config_permission:
            write_config_permission = Permission(
                resource="config", action="write")
            db.session.add(write_config_permission)

        # Check if permission already attached to avoid duplicate
        if write_config_permission not in admin_role.permissions.all():
            admin_role.permissions.append(write_config_permission)

        user = User(username="admin", email="admin@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Create configuration missing value
    response = client.post(
        "/api/config",
        headers={"Authorization": f"Bearer {token}"},
        json={"key": "app.debug"},
    )

    assert response.status_code == 400
    assert "Missing required field: value" in response.get_json()["message"]


def test_create_configuration_duplicate_key(client) -> None:
    """Test creating configuration with duplicate key (400)."""
    with client.application.app_context():
        db.create_all()
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="Administrator")
            db.session.add(admin_role)
        db.session.add(admin_role)

        write_config_permission = db.session.query(Permission).filter_by(
            resource="config", action="write"
        ).first()
        if not write_config_permission:
            write_config_permission = Permission(
                resource="config", action="write")
            db.session.add(write_config_permission)

        # Check if permission already attached to avoid duplicate
        if write_config_permission not in admin_role.permissions.all():
            admin_role.permissions.append(write_config_permission)

        user = User(username="admin", email="admin@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        # Create existing configuration
        config = Configuration(key="app.debug", value="false", category="app")
        db.session.add(config)
        db.session.commit()

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Try to create configuration with duplicate key
    response = client.post(
        "/api/config",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "key": "app.debug",
            "value": "true",
            "category": "app",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "Configuration key already exists"


def test_update_configuration_user_not_found(client) -> None:
    """Test updating configuration with invalid user (404)."""
    with client.application.app_context():
        db.create_all()
        user = User(username="admin", email="admin@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

        config = Configuration(
            key="app.name", value="Scene Packer", category="app")
        db.session.add(config)
        db.session.commit()
        config_id = config.id

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Delete user to simulate user not found
    with client.application.app_context():
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    # Try to update configuration - should fail
    response = client.put(
        f"/api/config/{config_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"value": "Scene Packer v2"},
    )
    # JWT token is valid but user doesn't exist anymore
    assert response.status_code in [404, 401]


def test_update_configuration_permission_denied(client) -> None:
    """Test updating configuration without write permission (403)."""
    with client.application.app_context():
        db.create_all()
        # Create user without permissions
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        config = Configuration(
            key="app.name", value="Scene Packer", category="app")
        db.session.add(config)
        db.session.commit()
        config_id = config.id

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Update configuration - should fail with permission denied
    response = client.put(
        f"/api/config/{config_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"value": "Scene Packer v2"},
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Permission denied"


def test_update_configuration_no_data(client) -> None:
    """Test updating configuration without data (400)."""
    with client.application.app_context():
        db.create_all()
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="Administrator")
            db.session.add(admin_role)
        db.session.add(admin_role)

        write_config_permission = db.session.query(Permission).filter_by(
            resource="config", action="write"
        ).first()
        if not write_config_permission:
            write_config_permission = Permission(
                resource="config", action="write")
            db.session.add(write_config_permission)

        # Check if permission already attached to avoid duplicate
        if write_config_permission not in admin_role.permissions.all():
            admin_role.permissions.append(write_config_permission)

        user = User(username="admin", email="admin@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config = Configuration(
            key="app.name", value="Scene Packer", category="app")
        db.session.add(config)
        db.session.commit()
        config_id = config.id

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Update configuration without data (don't send json parameter)
    response = client.put(
        f"/api/config/{config_id}",
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json"},
        data="{}",
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data is not None
    assert data["message"] == "No data provided"


def test_update_configuration_duplicate_key(client) -> None:
    """Test updating configuration with duplicate key (400)."""
    with client.application.app_context():
        db.create_all()
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="Administrator")
            db.session.add(admin_role)
        db.session.add(admin_role)

        write_config_permission = db.session.query(Permission).filter_by(
            resource="config", action="write"
        ).first()
        if not write_config_permission:
            write_config_permission = Permission(
                resource="config", action="write")
            db.session.add(write_config_permission)

        # Check if permission already attached to avoid duplicate
        if write_config_permission not in admin_role.permissions.all():
            admin_role.permissions.append(write_config_permission)

        user = User(username="admin", email="admin@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config1 = Configuration(
            key="app.name", value="Scene Packer", category="app")
        config2 = Configuration(
            key="app.version", value="2.0.0", category="app")
        db.session.add_all([config1, config2])
        db.session.commit()
        config1_id = config1.id

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Try to update config1 with config2's key
    response = client.put(
        f"/api/config/{config1_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"key": "app.version"},
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "Configuration key already exists"


def test_update_configuration_category(client) -> None:
    """Test updating configuration category."""
    with client.application.app_context():
        db.create_all()
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="Administrator")
            db.session.add(admin_role)
        db.session.add(admin_role)

        write_config_permission = db.session.query(Permission).filter_by(
            resource="config", action="write"
        ).first()
        if not write_config_permission:
            write_config_permission = Permission(
                resource="config", action="write")
            db.session.add(write_config_permission)

        # Check if permission already attached to avoid duplicate
        if write_config_permission not in admin_role.permissions.all():
            admin_role.permissions.append(write_config_permission)

        user = User(username="admin", email="admin@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config = Configuration(
            key="app.name", value="Scene Packer", category="app")
        db.session.add(config)
        db.session.commit()
        config_id = config.id

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Update configuration category
    response = client.put(
        f"/api/config/{config_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"category": "database"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["configuration"]["category"] == "database"


def test_update_configuration_description(client) -> None:
    """Test updating configuration description."""
    with client.application.app_context():
        db.create_all()
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin", description="Administrator")
            db.session.add(admin_role)
        db.session.add(admin_role)

        write_config_permission = db.session.query(Permission).filter_by(
            resource="config", action="write"
        ).first()
        if not write_config_permission:
            write_config_permission = Permission(
                resource="config", action="write")
            db.session.add(write_config_permission)

        # Check if permission already attached to avoid duplicate
        if write_config_permission not in admin_role.permissions.all():
            admin_role.permissions.append(write_config_permission)

        user = User(username="admin", email="admin@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        config = Configuration(
            key="app.name", value="Scene Packer", category="app")
        db.session.add(config)
        db.session.commit()
        config_id = config.id

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Update configuration description
    response = client.put(
        f"/api/config/{config_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "Application name"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["configuration"]["description"] == "Application name"


def test_delete_configuration_permission_denied(client) -> None:
    """Test deleting configuration without delete permission (403)."""
    with client.application.app_context():
        db.create_all()
        # Create user without delete permission
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")

        # Give read permission but not delete
        read_permission = db.session.query(Permission).filter_by(
            resource="config", action="read"
        ).first()
        if not read_permission:
            read_permission = Permission(resource="config", action="read")
            db.session.add(read_permission)

        role = Role(name="viewer", description="Viewer")
        role.permissions.append(read_permission)
        db.session.add(role)
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()

        config = Configuration(
            key="app.name", value="Scene Packer", category="app")
        db.session.add(config)
        db.session.commit()
        config_id = config.id

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]

    # Delete configuration - should fail with permission denied
    response = client.delete(
        f"/api/config/{config_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert response.get_json()["message"] == "Permission denied"
