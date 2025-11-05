"""Jobs blueprint for job management."""

from __future__ import annotations

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from web.extensions import db
from web.models import Job, User
from web.utils.permissions import check_permission

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.route("/jobs", methods=["GET"])
@jwt_required()
def list_jobs() -> tuple[dict, int]:
    """List jobs with filters and pagination.

    Query parameters:
        - status: Filter by status (pending, running, completed, failed, cancelled)
        - job_type: Filter by job type (nfofix, readnfo, repack, dirfix, etc.)
        - release_id: Filter by release ID
        - page: Page number (default: 1)
        - per_page: Items per page (default: 50)

    Returns:
        JSON response with jobs list and pagination info.
    """
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)

    if not user:
        return {"message": "User not found"}, 404

    # Check permissions (all users can list their own jobs, admin can list all)
    if not check_permission(user, "jobs", "read"):
        return {"message": "Permission denied"}, 403

    # Parse query parameters
    status = request.args.get("status")
    job_type = request.args.get("job_type")
    release_id = request.args.get("release_id", type=int)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)

    # Build query
    query = Job.query

    # Non-admin users can only see their own jobs
    if not check_permission(user, "jobs", "mod"):  # mod allows seeing all jobs (admin)
        query = query.filter_by(created_by=current_user_id)

    # Apply filters
    if status:
        query = query.filter_by(status=status)
    if job_type:
        query = query.filter_by(job_type=job_type)
    if release_id:
        query = query.filter_by(release_id=release_id)

    # Order by created_at desc
    query = query.order_by(Job.created_at.desc())

    # Pagination
    total = query.count()
    jobs = query.paginate(page=page, per_page=per_page, error_out=False)

    return (
        {
            "jobs": [job.to_dict() for job in jobs.items],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": jobs.pages,
        },
        200,
    )


@jobs_bp.route("/jobs/<int:job_id>", methods=["GET"])
@jwt_required()
def get_job(job_id: int) -> tuple[dict, int]:
    """Get job details.

    Args:
        job_id: Job ID.

    Returns:
        JSON response with job details including logs.
    """
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)

    if not user:
        return {"message": "User not found"}, 404

    # Get job
    job = db.session.get(Job, job_id)

    if not job:
        return {"message": "Job not found"}, 404

    # Check permissions (users can see their own jobs, admin can see all)
    if not check_permission(user, "jobs", "read"):
        return {"message": "Permission denied"}, 403

    if not check_permission(user, "jobs", "mod") and job.created_by != current_user_id:
        return {"message": "Permission denied"}, 403

    return (job.to_dict(), 200)


@jobs_bp.route("/jobs/<int:job_id>/logs", methods=["GET"])
@jwt_required()
def get_job_logs(job_id: int) -> tuple[dict, int]:
    """Get job logs.

    Args:
        job_id: Job ID.

    Returns:
        JSON response with job logs.
    """
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)

    if not user:
        return {"message": "User not found"}, 404

    # Get job
    job = db.session.get(Job, job_id)

    if not job:
        return {"message": "Job not found"}, 404

    # Check permissions
    if not check_permission(user, "jobs", "read"):
        return {"message": "Permission denied"}, 403

    if not check_permission(user, "jobs", "mod") and job.created_by != current_user_id:
        return {"message": "Permission denied"}, 403

    return (
        {
            "job_id": job.id,
            "logs": job.logs or "",
        },
        200,
    )


@jobs_bp.route("/jobs/<int:job_id>/status", methods=["GET"])
@jwt_required()
def get_job_status(job_id: int) -> tuple[dict, int]:
    """Get job status.

    Args:
        job_id: Job ID.

    Returns:
        JSON response with job status and progress.
    """
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)

    if not user:
        return {"message": "User not found"}, 404

    # Get job
    job = db.session.get(Job, job_id)

    if not job:
        return {"message": "Job not found"}, 404

    # Check permissions
    if not check_permission(user, "jobs", "read"):
        return {"message": "Permission denied"}, 403

    if not check_permission(user, "jobs", "mod") and job.created_by != current_user_id:
        return {"message": "Permission denied"}, 403

    # Calculate progress
    from web.services.job import JobService

    service = JobService()
    progress = service.get_job_progress(job_id)

    return (
        {
            "job_id": job.id,
            "status": job.status,
            "progress": progress,
            "created_at": job.created_at.isoformat() if job.created_at else None,
        },
        200,
    )


@jobs_bp.route("/jobs/<int:job_id>/cancel", methods=["PUT"])
@jwt_required()
def cancel_job(job_id: int) -> tuple[dict, int]:
    """Cancel a running job.

    Args:
        job_id: Job ID to cancel.

    Returns:
        JSON response with cancellation result.
    """
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)

    if not user:
        return {"message": "User not found"}, 404

    # Get job
    job = db.session.get(Job, job_id)

    if not job:
        return {"message": "Job not found"}, 404

    # Check permissions
    if not check_permission(user, "jobs", "mod"):
        return {"message": "Permission denied"}, 403

    # Cancel job
    from web.services.job import JobService

    service = JobService()
    success = service.cancel_job(job_id)

    if not success:
        return {"message": "Job cannot be cancelled (not pending or running)"}, 400

    return (
        {
            "message": "Job cancelled successfully",
            "job_id": job_id,
        },
        200,
    )
