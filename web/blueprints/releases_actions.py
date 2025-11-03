"""Releases actions blueprint for special actions (NFOFIX, READNFO, REPACK, DIRFIX)."""

from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from web.extensions import db
from web.models import Job, Release, User

releases_actions_bp = Blueprint("releases_actions", __name__)


@releases_actions_bp.route(
    "/releases/<int:release_id>/actions/nfofix", methods=["POST"]
)
@jwt_required()
def nfofix(release_id: int) -> tuple[dict, int]:
    """Fix NFO file for a release.

    Args:
        release_id: Release ID.

    Returns:
        JSON response with job ID for async processing.
    """
    current_user_id = get_jwt_identity()
    release = Release.query.get(release_id)

    if not release:
        return {"message": "Release not found"}, 404

    # TODO: Check MOD permission
    if release.user_id != current_user_id:
        return {"message": "Permission denied"}, 403

    # Create job for NFOFIX action
    job = Job(
        release_id=release.id,
        created_by=current_user_id,
        status="pending",
        config_json={"action": "nfofix"},
    )
    db.session.add(job)
    db.session.commit()

    # TODO: Queue async task for NFOFIX processing
    # For now, just mark job as completed
    job.status = "completed"
    db.session.commit()

    return (
        {
            "job_id": job.id,
            "message": "NFOFIX job created successfully",
        },
        202,
    )


@releases_actions_bp.route(
    "/releases/<int:release_id>/actions/readnfo", methods=["POST"]
)
@jwt_required()
def readnfo(release_id: int) -> tuple[dict, int]:
    """Read NFO and regenerate release structure.

    Args:
        release_id: Release ID.

    Returns:
        JSON response with job ID for async processing.
    """
    current_user_id = get_jwt_identity()
    release = Release.query.get(release_id)

    if not release:
        return {"message": "Release not found"}, 404

    # TODO: Check MOD permission
    if release.user_id != current_user_id:
        return {"message": "Permission denied"}, 403

    # Create job for READNFO action
    job = Job(
        release_id=release.id,
        created_by=current_user_id,
        status="pending",
        config_json={"action": "readnfo"},
    )
    db.session.add(job)
    db.session.commit()

    # TODO: Queue async task for READNFO processing
    job.status = "completed"
    db.session.commit()

    return (
        {
            "job_id": job.id,
            "message": "READNFO job created successfully",
        },
        202,
    )


@releases_actions_bp.route(
    "/releases/<int:release_id>/actions/repack", methods=["POST"]
)
@jwt_required()
def repack(release_id: int) -> tuple[dict, int]:
    """Repack release with new options.

    Args:
        release_id: Release ID.

    Request body:
        - config: New packaging config (optional)

    Returns:
        JSON response with job ID for async processing.
    """
    current_user_id = get_jwt_identity()
    release = Release.query.get(release_id)

    if not release:
        return {"message": "Release not found"}, 404

    # TODO: Check MOD permission
    if release.user_id != current_user_id:
        return {"message": "Permission denied"}, 403

    data = request.get_json() or {}
    new_config = data.get("config", release.config or {})

    # Create job for REPACK action
    job = Job(
        release_id=release.id,
        created_by=current_user_id,
        status="pending",
        config_json={"action": "repack", "config": new_config},
    )
    db.session.add(job)
    db.session.commit()

    # TODO: Queue async task for REPACK processing
    job.status = "processing"
    db.session.commit()

    return (
        {
            "job_id": job.id,
            "message": "REPACK job created successfully",
        },
        202,
    )


@releases_actions_bp.route(
    "/releases/<int:release_id>/actions/dirfix", methods=["POST"]
)
@jwt_required()
def dirfix(release_id: int) -> tuple[dict, int]:
    """Fix directory structure for a release.

    Args:
        release_id: Release ID.

    Returns:
        JSON response with job ID for async processing.
    """
    current_user_id = get_jwt_identity()
    release = Release.query.get(release_id)

    if not release:
        return {"message": "Release not found"}, 404

    # TODO: Check MOD permission
    if release.user_id != current_user_id:
        return {"message": "Permission denied"}, 403

    # Create job for DIRFIX action
    job = Job(
        release_id=release.id,
        created_by=current_user_id,
        status="pending",
        config_json={"action": "dirfix"},
    )
    db.session.add(job)
    db.session.commit()

    # TODO: Queue async task for DIRFIX processing
    job.status = "completed"
    db.session.commit()

    return (
        {
            "job_id": job.id,
            "message": "DIRFIX job created successfully",
        },
        202,
    )
