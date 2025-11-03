"""Permission utilities for granular permissions checking."""

from __future__ import annotations

from typing import TYPE_CHECKING

from web.extensions import db

if TYPE_CHECKING:
    from web.models import User


def check_permission(
    user: "User", resource: str, action: str, release_user_id: int | None = None
) -> bool:
    """Check if user has permission for resource and action.

    Args:
        user: User object.
        resource: Resource name (releases, rules, users, roles, config).
        action: Action name (read, write, mod, delete).
        release_user_id: Optional release owner user ID (for ownership checks).

    Returns:
        True if user has permission, False otherwise.
    """
    # Admin users have all permissions
    if is_admin(user):
        return True

    # Check if user has permission through role
    for role in user.roles:
        for permission in role.permissions:
            if permission.resource == resource and permission.action == action:
                return True

    # Note: Direct user permissions not implemented (only via roles)

    # Special case: Users can perform actions on their own releases
    if resource == "releases" and release_user_id and user.id == release_user_id:
        # For releases, users can always READ their own
        if action == "read":
            return True
        # Users can WRITE/MOD/DELETE their own releases
        if action in ("write", "mod", "delete"):
            return True

    return False


def require_permission(resource: str, action: str, require_admin: bool = False) -> bool:
    """Require permission decorator helper.

    Args:
        resource: Resource name.
        action: Action name.
        require_admin: Whether to require admin role.

    Returns:
        True if access granted, False otherwise.

    Note:
        This is a helper function. Use in blueprint routes with
        flask_jwt_extended.get_jwt_identity() to get current user.
    """
    # Placeholder for decorator helper
    # Actual implementation uses check_permission() directly in routes
    return True


def get_user_permissions(user: "User") -> dict[str, list[str]]:
    """Get all permissions for a user grouped by resource.

    Args:
        user: User object.

    Returns:
        Dictionary mapping resource to list of allowed actions.
    """
    permissions: dict[str, list[str]] = {}

    # Admin users have all permissions
    if is_admin(user):
        resources = ["releases", "rules", "users", "roles", "config"]
        actions = ["read", "write", "mod", "delete"]
        for resource in resources:
            permissions[resource] = actions.copy()
        return permissions

    # Collect permissions from roles
    for role in user.roles:
        for permission in role.permissions:
            if permission.resource not in permissions:
                permissions[permission.resource] = []
            if permission.action not in permissions[permission.resource]:
                permissions[permission.resource].append(permission.action)

    # Note: Direct user permissions not implemented (only via roles)

    # Users always have READ on their own releases
    if "releases" not in permissions:
        permissions["releases"] = []
    if "read" not in permissions["releases"]:
        permissions["releases"].append("read")

    return permissions


def is_admin(user: "User") -> bool:
    """Check if user is admin.

    Admin is determined by having a role named "admin" or "administrator".

    Args:
        user: User object.

    Returns:
        True if user is admin, False otherwise.
    """
    return user.is_admin()


def can_manage_user(current_user: "User", target_user_id: int) -> bool:
    """Check if current user can manage target user.

    Args:
        current_user: Current user object.
        target_user_id: Target user ID.

    Returns:
        True if current user can manage target user, False otherwise.
    """
    # Admin can manage all users
    if is_admin(current_user):
        return True

    # Users can manage themselves (limited actions)
    return current_user.id == target_user_id


def create_default_permissions() -> None:
    """Create default permissions if they don't exist.

    This should be called during database initialization.
    """
    from web.models import Permission

    default_permissions = [
        # Releases permissions
        ("releases", "read"),
        ("releases", "write"),
        ("releases", "mod"),
        ("releases", "delete"),
        # Rules permissions
        ("rules", "read"),
        ("rules", "write"),
        ("rules", "mod"),
        ("rules", "delete"),
        # Users permissions
        ("users", "read"),
        ("users", "write"),
        ("users", "mod"),
        ("users", "delete"),
        # Roles permissions
        ("roles", "read"),
        ("roles", "write"),
        ("roles", "mod"),
        ("roles", "delete"),
        # Config permissions
        ("config", "read"),
        ("config", "write"),
        ("config", "mod"),
        ("config", "delete"),
    ]

    for resource, action in default_permissions:
        existing = Permission.query.filter_by(resource=resource, action=action).first()
        if not existing:
            permission = Permission(resource=resource, action=action)
            db.session.add(permission)

    db.session.commit()
