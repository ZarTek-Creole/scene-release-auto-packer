"""Tests for JobService (TDD - Red phase)."""

from __future__ import annotations

import pytest

from web.extensions import db
from web.models import Group, Job, Release, User
from web.services.job_service import JobService


def test_process_job_success(app) -> None:
    """Test processing a job successfully (pending → running → completed)."""
    with app.app_context():
        db.create_all()
        
        # Create user
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.flush()
        
        # Create group
        group = Group(name="TestGroup")
        db.session.add(group)
        db.session.flush()
        
        # Create release
        release = Release(
            user_id=user.id,
            group_id=group.id,
            release_type="EBOOK",
            status="draft",
        )
        db.session.add(release)
        db.session.commit()
        
        # Create pending job
        job = Job(
            release_id=release.id,
            created_by=user.id,
            status="pending",
            job_type="nfofix",
            config_json={"action": "nfofix"},
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
        
        # Process job
        service = JobService()
        service.process_job(job_id)
        
        # Verify job status updated
        job = db.session.get(Job, job_id)
        assert job.status == "completed"
        assert job.logs is not None


def test_process_job_failure(app) -> None:
    """Test processing a job that fails (pending → running → failed)."""
    with app.app_context():
        db.create_all()
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        
        # Create job with invalid config to force failure
        job = Job(
            release_id=None,
            created_by=user.id,
            status="pending",
            job_type="nfofix",
            config_json={"action": "invalid_action"},
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
        
        # Process job (should fail)
        service = JobService()
        service.process_job(job_id)
        
        # Verify job status is failed
        job = db.session.get(Job, job_id)
        assert job.status == "failed"
        assert "error" in job.logs.lower() or "failed" in job.logs.lower()


def test_update_status(app) -> None:
    """Test updating job status."""
    with app.app_context():
        db.create_all()
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            release_id=None,
            created_by=user.id,
            status="pending",
            job_type="test",
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
        
        # Update status
        service = JobService()
        service.update_status(job_id, "running", "Starting job...")
        
        # Verify status updated
        job = db.session.get(Job, job_id)
        assert job.status == "running"
        assert "Starting job" in job.logs


def test_append_log(app) -> None:
    """Test appending log to job."""
    with app.app_context():
        db.create_all()
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            release_id=None,
            created_by=user.id,
            status="running",
            job_type="test",
            logs="Initial log\n",
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
        
        # Append log
        service = JobService()
        service.append_log(job_id, "Processing step 1", "INFO")
        
        # Verify job updated
        job = db.session.get(Job, job_id)
        assert "Initial log" in job.logs
        assert "Processing step 1" in job.logs
        assert "INFO" in job.logs


def test_cancel_job(app) -> None:
    """Test canceling a running job."""
    with app.app_context():
        db.create_all()
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            release_id=None,
            created_by=user.id,
            status="running",
            job_type="test",
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
        
        # Cancel job
        service = JobService()
        success = service.cancel_job(job_id)
        
        # Verify cancellation
        assert success is True
        job = db.session.get(Job, job_id)
        assert job.status == "cancelled"


def test_cancel_job_not_running(app) -> None:
    """Test canceling a job that is not running (should fail)."""
    with app.app_context():
        db.create_all()
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            release_id=None,
            created_by=user.id,
            status="completed",
            job_type="test",
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
        
        # Try to cancel completed job
        service = JobService()
        success = service.cancel_job(job_id)
        
        # Should fail
        assert success is False
        job = db.session.get(Job, job_id)
        assert job.status == "completed"  # Unchanged


def test_get_job_progress(app) -> None:
    """Test getting job progress."""
    with app.app_context():
        db.create_all()
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            release_id=None,
            created_by=user.id,
            status="running",
            job_type="test",
            config_json={"progress": 50},
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
        
        # Get progress
        service = JobService()
        progress = service.get_job_progress(job_id)
        
        # Verify progress
        assert progress == 50
