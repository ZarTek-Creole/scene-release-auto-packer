"""Tests for permissions utilities."""

from __future__ import annotations

from web.extensions import db
from web.models import Permission, Role, User
from web.utils.permissions import (
    can_manage_user,
    check_permission,
    get_user_permissions,
    is_admin,
)


def test_is_admin_with_admin_role(app):
    """Test is_admin returns True for user with admin role."""
    with app.app_context():
        admin_role = Role(name="admin", description="Administrator")
        db.session.add(admin_role)
        db.session.commit()

        user = User(username="admin", email="admin@test.com")
        user.set_password("password")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        assert is_admin(user) is True


def test_is_admin_without_admin_role(app):
    """Test is_admin returns False for user without admin role."""
    with app.app_context():
        user = User(username="user", email="user@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        assert is_admin(user) is False


def test_check_permission_admin_has_all(app):
    """Test check_permission returns True for admin for all resources."""
    with app.app_context():
        admin_role = Role(name="admin", description="Administrator")
        db.session.add(admin_role)
        db.session.commit()

        user = User(username="admin", email="admin@test.com")
        user.set_password("password")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        assert check_permission(user, "releases", "read") is True
        assert check_permission(user, "releases", "write") is True
        assert check_permission(user, "rules", "mod") is True
        assert check_permission(user, "users", "delete") is True


def test_check_permission_user_with_role_permission(app):
    """Test check_permission returns strength for user with role permission."""
    with app.app_context():
        editor_role = Role(name="editor", description="Editor")
        permission = Permission(resource="releases", action="mod")
        editor_role.permissions.append(permission)
        db.session.add_all([editor_role, permission])
        db.session.commit()

        user = User(username="editor", email="editor@test.com")
        user.set_password("password")
        user.roles.append(editor_role)
        db.session.add(user)
        db.session.commit()

        assert check_permission(user, "releases", "mod") is True
        assert check_permission(user, "releases", "delete") is False
        assert check_permission(user, "rules", "read") is False


def test_check_permission_user_own_release(app):
    """Test check_permission allows user to manage own releases."""
    with app.app_context():
        user = User(username="user", email="user@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # User can read their own releases
        assert check_permission(user, "releases", "read", release_user_id=user.id) is True
        # User can write their own releases
        assert (
            check_permission(user, "releases", "write", release_user_id=user.id)
            is True
        )
        # User can delete their own releases
        assert (
            check_permission(user, "releases", "delete", release_user_id=user.id)
            is True
        )


def test_can_manage_user_admin_can_manage_all(app):
    """Test can_manage_user allows admin to manage all users."""
    with app.app_context():
        admin_role = Role(name="admin", description="Administrator")
        db.session.add(admin_role)
        db.session.commit()

        admin_user = User(username="admin", email="admin@test.com")
        admin_user.set_password("password")
        admin_user.roles.append(admin_role)
        db.session.add(admin_user)
        db.session.commit()

        target_user = User(username="target", email="target@test.com")
        target_user.set_password("password")
        db.session.add(target_user)
        db.session.commit()

        assert can_manage_user(admin_user, target_user.id) is True


def test_can_manage_user_can_manage_self(app):
    """Test can_manage_user allows user to manage themselves."""
    with app.app_context():
        user = User(username="user", email="user@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        assert can_manage_user(user, user.id) is True


def test_can_manage_user_cannot_manage_others(app):
    """Test can_manage_user prevents user from managing others."""
    with app.app_context():
        user1 = User(username="user1", email="user1@test.com")
        user1.set_password("password")
        user2 = User(username="user2", email="user2@test.com")
        user2.set_password("password")
        db.session.add_all([user1, user2])
        db.session.commit()

        assert can_manage_user(user1, user2.id) is False


def test_get_user_permissions_admin(app):
    """Test get_user_permissions returns all permissions for admin."""
    with app.app_context():
        admin_role = Role(name="admin", description="Administrator")
        db.session.add(admin_role)
        db.session.commit()

        user = User(username="admin", email="admin@test.com")
        user.set_password("password")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()

        permissions = get_user_permissions(user)

        assert "releases" in permissions
        assert "read" in permissions["releases"]
        assert "write" in permissions["releases"]
        assert "mod" in permissions["releases"]
        assert "delete" in permissions["releases"]


def test_get_user_permissions_user_with_role(app):
    """Test get_user_permissions returns permissions from role."""
    with app.app_context():
        editor_role = Role(name="editor", description="Editor")
        permission_read = Permission(resource="releases", action="read")
        permission_mod = Permission(resource="releases", action="mod")
        editor_role.permissions.extend([permission_read, permission_mod])
        db.session.add_all([editor_role, permission_read, permission_mod])
        db.session.commit()

        user = User(username="editor", email="editor@test.com")
        user.set_password("password")
        user.roles.append(editor_role)
        db.session.add(user)
        db.session.commit()

        permissions = get_user_permissions(user)

        assert "releases" in permissions
        assert "read" in permissions["releases"]
        assert "mod" in permissions["releases"]
        assert "write" not in permissions["releases"]
        assert "delete" not in permissions["releases"]
