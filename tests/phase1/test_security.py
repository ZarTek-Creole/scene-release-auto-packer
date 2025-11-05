"""Tests for JWT security callbacks."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt
from flask_jwt_extended import create_access_token

from web.extensions import db
from web.models import TokenBlocklist, User


def test_token_blocklist_check(client) -> None:
    """Test token blocklist check."""
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
    access_token = login_response.get_json()["access_token"]

    # Decode token to get jti
    decoded = jwt.decode(
        access_token, options={"verify_signature": False}, algorithms=["HS256"]
    )
    jti = decoded.get("jti")

    # Decode to get exp
    exp = decoded.get("exp")
    expires_at = datetime.fromtimestamp(
        exp, tz=UTC) if exp else datetime.now(UTC)

    # Add token to blocklist
    with client.application.app_context():
        blocked_token = TokenBlocklist(
            jti=jti, token_type="access", expires_at=expires_at
        )
        db.session.add(blocked_token)
        db.session.commit()

    # Try to use blocked token
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 401


def test_expired_token_callback(client) -> None:
    """Test expired token callback."""
    with client.application.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id  # Store ID before session closes

    # Get user object within app context for token creation
    with client.application.app_context():
        user = User.query.get(user_id)
        expired_token = create_access_token(
            identity=user, expires_delta=timedelta(seconds=-1)
        )

    # Try to use expired token
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )

    assert response.status_code == 401
    data = response.get_json()
    assert (
        "expired" in data["message"].lower(
        ) or "Token has expired" in data["message"]
    )


def test_invalid_token_callback(client) -> None:
    """Test invalid token callback."""
    # Try to use invalid token
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token_format"},
    )

    assert response.status_code == 401
    data = response.get_json()
    assert "Invalid token" in data["message"] or "invalid" in data["message"].lower(
    )


def test_missing_token_callback(client) -> None:
    """Test missing token callback."""
    # Try to access protected route without token
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    data = response.get_json()
    assert (
        "Authorization required" in data["message"]
        or "required" in data["message"].lower()
    )


def test_user_lookup_callback_inactive_user(client) -> None:
    """Test user lookup callback with inactive user."""
    with client.application.app_context():
        db.create_all()
        user = User(username="inactiveuser",
                    email="inactive@example.com", active=False)
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    # Login should fail for inactive user
    response = client.post(
        "/api/auth/login",
        json={"username": "inactiveuser", "password": "password123"},
    )

    assert response.status_code == 403
    data = response.get_json()
    assert "inactive" in data["message"].lower()


def test_user_identity_lookup_with_int(client) -> None:
    """Test user identity lookup with integer."""
    from flask_jwt_extended import create_access_token

    with client.application.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # Create token with integer identity
    with client.application.app_context():
        token = create_access_token(identity=user_id)

    # Token should be valid
    assert token is not None


def test_user_identity_lookup_with_user_object(client) -> None:
    """Test user identity lookup with User object."""
    from flask_jwt_extended import create_access_token

    with client.application.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        # Use user within same app context
        token = create_access_token(identity=user)
        db.session.expunge(user)  # Expunge to avoid detached instance error

    # Token should be valid
    assert token is not None


def test_user_identity_lookup_fallback(client) -> None:
    """Test user identity lookup fallback."""
    from flask_jwt_extended import create_access_token

    # Create token with invalid identity type (should use fallback)
    with client.application.app_context():
        # Use a float as identity (not handled explicitly, should use fallback)
        token = create_access_token(identity=123.45)

    # Token should be created (fallback converts to string)
    assert token is not None


def test_token_blocklist_check_no_jti(client) -> None:
    """Test token blocklist check with no jti in payload."""
    import jwt

    with client.application.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id  # Store ID before session closes

    # Create a token manually without jti
    with client.application.app_context():
        from flask import current_app
        token = jwt.encode(
            {"sub": str(user_id), "exp": 9999999999},
            current_app.config["JWT_SECRET_KEY"],
            algorithm="HS256"
        )

    # Try to use token without jti (should be considered revoked)
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Should fail because token has no jti
    assert response.status_code == 401


def test_user_lookup_callback_no_sub(client) -> None:
    """Test user lookup callback with no sub in payload."""
    from flask_jwt_extended import create_access_token
    import jwt

    with client.application.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    # Create a token manually without sub
    with client.application.app_context():
        from flask import current_app
        token = jwt.encode(
            {"exp": 9999999999},
            current_app.config["JWT_SECRET_KEY"],
            algorithm="HS256"
        )

    # Try to use token without sub (should fail)
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Should fail because token has no sub
    assert response.status_code == 401


def test_user_lookup_callback_invalid_sub_type(client) -> None:
    """Test user lookup callback with invalid sub type."""
    from flask_jwt_extended import create_access_token
    import jwt

    with client.application.app_context():
        db.create_all()

    # Create a token manually with invalid sub (not int/str)
    with client.application.app_context():
        from flask import current_app
        token = jwt.encode(
            {"sub": None, "exp": 9999999999},
            current_app.config["JWT_SECRET_KEY"],
            algorithm="HS256"
        )

    # Try to use token with invalid sub (should fail)
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Should fail because sub is invalid
    assert response.status_code == 401


def test_user_lookup_callback_invalid_sub_value(client) -> None:
    """Test user lookup callback with invalid sub value (non-numeric string)."""
    from flask_jwt_extended import create_access_token
    import jwt

    with client.application.app_context():
        db.create_all()

    # Create a token manually with invalid sub (non-numeric string)
    with client.application.app_context():
        from flask import current_app
        token = jwt.encode(
            {"sub": "invalid_string", "exp": 9999999999},
            current_app.config["JWT_SECRET_KEY"],
            algorithm="HS256"
        )

    # Try to use token with invalid sub (should fail)
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Should fail because sub cannot be converted to int
    assert response.status_code == 401


def test_user_lookup_callback_with_int_sub(client) -> None:
    """Test user lookup callback with int sub (already integer)."""
    from flask_jwt_extended import create_access_token
    import jwt

    with client.application.app_context():
        db.create_all()
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    # Create a token using Flask-JWT-Extended to ensure proper format with jti
    with client.application.app_context():
        token = create_access_token(identity=user_id)

    # Try to use token with int sub (should work)
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Should work because sub is already int and token has proper jti
    assert response.status_code == 200
