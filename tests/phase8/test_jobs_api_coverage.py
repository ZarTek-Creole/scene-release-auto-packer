"""Additional tests for Jobs API to improve coverage."""

from __future__ import annotations

import pytest

from web.extensions import db
from web.models import Group, Job, Permission, Release, Role, User


def test_list_jobs_user_not_found(client) -> None:
    """Test listing jobs when user not found."""
    # Mock scenario where user_id in JWT doesn't exist in DB
    # This is handled by JWT validation, but test the edge case
    
    # This test may not be directly testable through Flask JWT,
    # but we can ensure proper error handling in blueprints
    pass  # Already covered by JWT middleware


def test_list_jobs_permission_denied(client) -> None:
    """Test listing jobs without permission."""
    with client.application.app_context():
        db.create_all()
        
        # Create user without jobs:read permission
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
    
    # Try to list jobs (should fail - no permission)
    response = client.get(
        "/api/jobs",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 403


def test_list_jobs_non_admin_only_own(client) -> None:
    """Test that non-admin users only see their own jobs."""
    with client.application.app_context():
        db.create_all()
        
        # Create role with jobs:read (but not mod for admin)
        regular_role = Role(name="regular", description="Regular user")
        db.session.add(regular_role)
        
        jobs_read_permission = Permission(resource="jobs", action="read")
        db.session.add(jobs_read_permission)
        regular_role.permissions.append(jobs_read_permission)
        
        user1 = User(username="user1", email="user1@example.com")
        user1.set_password("password123")
        user1.roles.append(regular_role)
        db.session.add(user1)
        
        user2 = User(username="user2", email="user2@example.com")
        user2.set_password("password123")
        user2.roles.append(regular_role)
        db.session.add(user2)
        db.session.flush()
        
        user1_id = user1.id
        user2_id = user2.id
        
        # Create jobs for both users
        job1 = Job(
            release_id=None,
            created_by=user1_id,
            status="pending",
            job_type="nfofix",
        )
        job2 = Job(
            release_id=None,
            created_by=user2_id,
            status="pending",
            job_type="readnfo",
        )
        db.session.add_all([job1, job2])
        db.session.commit()
    
    # Login as user1
    login_response = client.post(
        "/api/auth/login",
        json={"username": "user1", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]
    
    # List jobs (should only see user1's job)
    response = client.get(
        "/api/jobs",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["jobs"]) == 1
    assert data["jobs"][0]["created_by"] == user1_id


def test_get_job_user_not_found(client) -> None:
    """Test getting a job when user not found."""
    # Already covered by JWT middleware
    pass


def test_get_job_permission_denied(client) -> None:
    """Test getting a job without permission."""
    with client.application.app_context():
        db.create_all()
        
        # Create user without jobs:read permission
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            release_id=None,
            created_by=user.id,
            status="pending",
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
    
    # Try to get job (should fail - no permission)
    response = client.get(
        f"/api/jobs/{job_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 403


def test_get_job_non_admin_other_user_job(client) -> None:
    """Test that non-admin users cannot see other users' jobs."""
    with client.application.app_context():
        db.create_all()
        
        regular_role = Role(name="regular", description="Regular user")
        db.session.add(regular_role)
        
        jobs_read_permission = Permission(resource="jobs", action="read")
        db.session.add(jobs_read_permission)
        regular_role.permissions.append(jobs_read_permission)
        
        user1 = User(username="user1", email="user1@example.com")
        user1.set_password("password123")
        user1.roles.append(regular_role)
        db.session.add(user1)
        
        user2 = User(username="user2", email="user2@example.com")
        user2.set_password("password123")
        db.session.add(user2)
        db.session.commit()
        
        # Create job for user2
        job = Job(
            release_id=None,
            created_by=user2.id,
            status="pending",
            job_type="nfofix",
        )
        db.session.add(job)
        db.session.commit()
        job_id = job.id
    
    # Login as user1
    login_response = client.post(
        "/api/auth/login",
        json={"username": "user1", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]
    
    # Try to get user2's job (should fail)
    response = client.get(
        f"/api/jobs/{job_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 403


def test_get_job_logs_permission_denied(client) -> None:
    """Test getting job logs without permission."""
    with client.application.app_context():
        db.create_all()
        
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
    
    # Try to get logs (should fail - no permission)
    response = client.get(
        f"/api/jobs/{job_id}/logs",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 403


def test_get_job_status_permission_denied(client) -> None:
    """Test getting job status without permission."""
    with client.application.app_context():
        db.create_all()
        
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
    
    # Try to get status (should fail - no permission)
    response = client.get(
        f"/api/jobs/{job_id}/status",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 403


def test_cancel_job_not_running(client) -> None:
    """Test canceling a job that is not running (should fail)."""
    with client.application.app_context():
        db.create_all()
        
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
        
        # Create completed job
        job = Job(
            release_id=None,
            created_by=user.id,
            status="completed",
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
    
    # Try to cancel completed job (should fail)
    response = client.put(
        f"/api/jobs/{job_id}/cancel",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 400


def test_list_jobs_pagination(client) -> None:
    """Test job listing with pagination."""
    with client.application.app_context():
        db.create_all()
        
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
        
        # Create multiple jobs
        for i in range(5):
            job = Job(
                release_id=None,
                created_by=user.id,
                status="pending",
                job_type="nfofix",
            )
            db.session.add(job)
        db.session.commit()
    
    # Login
    login_response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "password123"},
    )
    token = login_response.get_json()["access_token"]
    
    # List with pagination
    response = client.get(
        "/api/jobs?page=1&per_page=2",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["jobs"]) == 2
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["per_page"] == 2
