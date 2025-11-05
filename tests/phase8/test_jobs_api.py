"""Tests for Jobs API (TDD - Red phase)."""

from __future__ import annotations

import pytest

from web.extensions import db
from web.models import Group, Job, Permission, Release, Role, User


def test_list_jobs(client) -> None:
    """Test listing jobs."""
    with client.application.app_context():
        db.create_all()
        
        # Create admin role with jobs:read permission
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role.query.filter_by(name="admin").first()
            if not admin_role:
                admin_role = Role(name="admin", description="Administrator")
                db.session.add(admin_role)
        
        jobs_read_permission = Permission(resource="jobs", action="read")
        db.session.add(jobs_read_permission)
        admin_role.permissions.append(jobs_read_permission)
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()
        
        # Create jobs
        job1 = Job(
            release_id=None,
            created_by=user.id,
            status="pending",
            job_type="nfofix",
        )
        job2 = Job(
            release_id=None,
            created_by=user.id,
            status="completed",
            job_type="readnfo",
        )
        db.session.add_all([job1, job2])
        db.session.commit()
    
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]
    
    # List jobs
    response = client.get(
        "/api/jobs",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert "jobs" in data
    assert len(data["jobs"]) == 2


def test_list_jobs_with_filters(client) -> None:
    """Test listing jobs with filters."""
    with client.application.app_context():
        db.create_all()
        
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role.query.filter_by(name="admin").first()
            if not admin_role:
                admin_role = Role(name="admin", description="Administrator")
                db.session.add(admin_role)
        
        jobs_read_permission = Permission(resource="jobs", action="read")
        db.session.add(jobs_read_permission)
        admin_role.permissions.append(jobs_read_permission)
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()
        
        job1 = Job(
            release_id=None,
            created_by=user.id,
            status="pending",
            job_type="nfofix",
        )
        job2 = Job(
            release_id=None,
            created_by=user.id,
            status="completed",
            job_type="readnfo",
        )
        db.session.add_all([job1, job2])
        db.session.commit()
    
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]
    
    # Filter by status
    response = client.get(
        "/api/jobs?status=pending",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["jobs"]) == 1
    assert data["jobs"][0]["status"] == "pending"


def test_get_job(client) -> None:
    """Test getting a job."""
    with client.application.app_context():
        db.create_all()
        
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role.query.filter_by(name="admin").first()
            if not admin_role:
                admin_role = Role(name="admin", description="Administrator")
                db.session.add(admin_role)
        
        jobs_read_permission = Permission(resource="jobs", action="read")
        db.session.add(jobs_read_permission)
        admin_role.permissions.append(jobs_read_permission)
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            release_id=None,
            created_by=user.id,
            status="running",
            job_type="nfofix",
            logs="Test log\n",
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
    
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]
    
    # Get job
    response = client.get(
        f"/api/jobs/{job_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == job_id
    assert data["status"] == "running"


def test_get_job_not_found(client) -> None:
    """Test getting a non-existent job."""
    with client.application.app_context():
        db.create_all()
        
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role.query.filter_by(name="admin").first()
            if not admin_role:
                admin_role = Role(name="admin", description="Administrator")
                db.session.add(admin_role)
        
        jobs_read_permission = Permission(resource="jobs", action="read")
        db.session.add(jobs_read_permission)
        admin_role.permissions.append(jobs_read_permission)
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()
    
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]
    
    # Get non-existent job
    response = client.get(
        "/api/jobs/99999",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 404


def test_get_job_logs(client) -> None:
    """Test getting job logs."""
    with client.application.app_context():
        db.create_all()
        
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role.query.filter_by(name="admin").first()
            if not admin_role:
                admin_role = Role(name="admin", description="Administrator")
                db.session.add(admin_role)
        
        jobs_read_permission = Permission(resource="jobs", action="read")
        db.session.add(jobs_read_permission)
        admin_role.permissions.append(jobs_read_permission)
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            release_id=None,
            created_by=user.id,
            status="running",
            job_type="nfofix",
            logs="Log line 1\nLog line 2\n",
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
    
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]
    
    # Get logs
    response = client.get(
        f"/api/jobs/{job_id}/logs",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["job_id"] == job_id
    assert "Log line 1" in data["logs"]


def test_get_job_status(client) -> None:
    """Test getting job status."""
    with client.application.app_context():
        db.create_all()
        
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role.query.filter_by(name="admin").first()
            if not admin_role:
                admin_role = Role(name="admin", description="Administrator")
                db.session.add(admin_role)
        
        jobs_read_permission = Permission(resource="jobs", action="read")
        db.session.add(jobs_read_permission)
        admin_role.permissions.append(jobs_read_permission)
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            release_id=None,
            created_by=user.id,
            status="running",
            job_type="nfofix",
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
    
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]
    
    # Get status
    response = client.get(
        f"/api/jobs/{job_id}/status",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["job_id"] == job_id
    assert data["status"] == "running"
    assert "progress" in data


def test_cancel_job(client) -> None:
    """Test canceling a running job."""
    with client.application.app_context():
        db.create_all()
        
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role.query.filter_by(name="admin").first()
            if not admin_role:
                admin_role = Role(name="admin", description="Administrator")
                db.session.add(admin_role)
        
        jobs_mod_permission = Permission(resource="jobs", action="mod")
        db.session.add(jobs_mod_permission)
        admin_role.permissions.append(jobs_mod_permission)
        
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        user.roles.append(admin_role)
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            release_id=None,
            created_by=user.id,
            status="running",
            job_type="nfofix",
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
    
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]
    
    # Cancel job
    response = client.put(
        f"/api/jobs/{job_id}/cancel",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Job cancelled successfully"
    
    # Verify job is cancelled
    with client.application.app_context():
        job = db.session.get(Job, job_id)
        assert job.status == "cancelled"


def test_cancel_job_permission_denied(client) -> None:
    """Test canceling a job without permissions."""
    with client.application.app_context():
        db.create_all()
        
        # Create user without mod permission
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            release_id=None,
            created_by=user.id,
            status="running",
            job_type="nfofix",
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
    
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]
    
    # Try to cancel job (should fail - no mod permission)
    response = client.put(
        f"/api/jobs/{job_id}/cancel",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 403
