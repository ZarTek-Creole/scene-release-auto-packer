"""Security callbacks for JWT."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from web.models import TokenBlocklist, User

if TYPE_CHECKING:
    from flask_jwt_extended import JWTManager


def init_jwt(jwt: JWTManager) -> None:
    """Initialize JWT callbacks.

    Args:
        jwt: JWTManager instance.
    """

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(_jwt_header: dict[str, Any], jwt_payload: dict[str, Any]) -> bool:
        """Check if token is revoked.

        Args:
            jwt_header: JWT header.
            jwt_payload: JWT payload.

        Returns:
            True if token is revoked.
        """
        jti = jwt_payload.get("jti")
        if jti is None:
            return True

        token = TokenBlocklist.query.filter_by(jti=jti).first()
        return token is not None

    @jwt.user_identity_loader
    def user_identity_lookup(identity: int | str | User) -> str:
        """User identity loader.

        This callback is called when creating a token. It should return
        the identity to be stored in the token (typically user ID as string).

        Args:
            identity: User ID (int/str) or User instance (if passed directly).

        Returns:
            User ID as string (required by Flask-JWT-Extended).
        """
        # If identity is already a string, return it
        if isinstance(identity, str):
            return identity
        # If identity is an integer, convert to string
        if isinstance(identity, int):
            return str(identity)
        # If identity is a User object, return its ID as string
        if isinstance(identity, User):
            return str(identity.id)
        # Fallback: convert to string
        return str(identity)

    @jwt.user_lookup_loader
    def user_lookup_callback(
        _jwt_header: dict[str, Any], jwt_payload: dict[str, Any]
    ) -> User | None:
        """User lookup callback.

        This callback is called when using @jwt_required() to load
        the user from the token's identity (subject).

        Args:
            jwt_header: JWT header.
            jwt_payload: JWT payload containing 'sub' (subject) field.

        Returns:
            User instance or None if not found or inactive.
        """
        identity = jwt_payload.get("sub")
        if identity is None:
            return None

        # Ensure identity is converted to integer (it's stored as string in token)
        try:
            user_id = int(identity) if not isinstance(identity, int) else identity
        except (ValueError, TypeError):
            return None

        user: User | None = User.query.filter_by(id=user_id, active=True).first()
        return user

    @jwt.expired_token_loader
    def expired_token_callback(
        _jwt_header: dict[str, Any], _jwt_payload: dict[str, Any]
    ) -> tuple[dict[str, Any], int]:
        """Expired token callback.

        Args:
            jwt_header: JWT header.
            jwt_payload: JWT payload.

        Returns:
            Error response.
        """
        return {"message": "Token has expired"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error: str) -> tuple[dict[str, Any], int]:
        """Invalid token callback.

        Args:
            error: Error message.

        Returns:
            Error response.
        """
        return {"message": f"Invalid token: {error}"}, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error: str) -> tuple[dict[str, Any], int]:
        """Missing token callback.

        Args:
            error: Error message.

        Returns:
            Error response.
        """
        return {"message": f"Authorization required: {error}"}, 401
