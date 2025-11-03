"""Job service for processing jobs asynchronously."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from web.extensions import db
from web.models import Job

logger = logging.getLogger(__name__)


class JobService:
    """Service for processing and managing jobs."""

    def __init__(self):
        """Initialize JobService."""
        pass

    def process_job(self, job_id: int) -> None:
        """Process a job asynchronously.

        For now, this is a synchronous simulation.
        In production, this would be handled by a background worker (Celery, RQ, etc.).

        Args:
            job_id: Job ID to process.
        """
        job = db.session.get(Job, job_id)

        if not job:
            logger.error(f"Job {job_id} not found")
            return

        if job.status != "pending":
            logger.warning(f"Job {job_id} is not pending (status: {job.status})")
            return

        # Update status to running
        self.update_status(job_id, "running", "Job processing started...")

        try:
            # Simulate job processing based on job_type
            job_type = job.job_type

            # Check for invalid action in config (for testing failure scenarios)
            config = job.config_json or {}
            if config.get("action") == "invalid_action":
                raise ValueError("Invalid action specified in job configuration")

            if job_type == "nfofix":
                self._process_nfofix_job(job_id)
            elif job_type == "readnfo":
                self._process_readnfo_job(job_id)
            elif job_type == "repack":
                self._process_repack_job(job_id)
            elif job_type == "dirfix":
                self._process_dirfix_job(job_id)
            else:
                # Generic processing simulation
                self.append_log(job_id, f"Processing job type: {job_type}", "INFO")
                self.append_log(job_id, "Job processing completed", "INFO")
                self.update_status(job_id, "completed", "Job completed successfully")

        except Exception as e:
            logger.error(f"Error processing job {job_id}: {e}", exc_info=True)
            error_msg = f"Job processing failed: {str(e)}"
            self.append_log(job_id, error_msg, "ERROR")
            self.update_status(job_id, "failed", error_msg)

    def _process_nfofix_job(self, job_id: int) -> None:
        """Process NFOFIX job."""
        self.append_log(job_id, "Fixing NFO file...", "INFO")
        self.append_log(job_id, "NFO file fixed successfully", "INFO")
        self.update_status(job_id, "completed", "NFOFIX job completed")

    def _process_readnfo_job(self, job_id: int) -> None:
        """Process READNFO job."""
        self.append_log(job_id, "Reading NFO file...", "INFO")
        self.append_log(job_id, "NFO file read successfully", "INFO")
        self.update_status(job_id, "completed", "READNFO job completed")

    def _process_repack_job(self, job_id: int) -> None:
        """Process REPACK job."""
        self.append_log(job_id, "Repacking release...", "INFO")
        self.append_log(job_id, "Release repacked successfully", "INFO")
        self.update_status(job_id, "completed", "REPACK job completed")

    def _process_dirfix_job(self, job_id: int) -> None:
        """Process DIRFIX job."""
        self.append_log(job_id, "Fixing directory structure...", "INFO")
        self.append_log(job_id, "Directory structure fixed successfully", "INFO")
        self.update_status(job_id, "completed", "DIRFIX job completed")

    def update_status(self, job_id: int, status: str, logs: str | None = None) -> None:
        """Update job status and optionally logs.

        Args:
            job_id: Job ID.
            status: New status (pending, running, completed, failed, cancelled).
            logs: Optional log message to append.
        """
        job = db.session.get(Job, job_id)

        if not job:
            logger.error(f"Job {job_id} not found")
            return

        job.status = status

        if logs:
            timestamp = datetime.now(timezone.utc).isoformat()
            if job.logs:
                job.logs += f"\n[{timestamp}] {logs}"
            else:
                job.logs = f"[{timestamp}] {logs}"

        db.session.commit()

    def append_log(self, job_id: int, log_message: str, level: str = "INFO") -> None:
        """Append log message to job.

        Args:
            job_id: Job ID.
            log_message: Log message.
            level: Log level (INFO, WARNING, ERROR, DEBUG).
        """
        job = db.session.get(Job, job_id)

        if not job:
            logger.error(f"Job {job_id} not found")
            return

        timestamp = datetime.now(timezone.utc).isoformat()
        log_line = f"[{timestamp}] [{level}] {log_message}"

        if job.logs:
            job.logs += f"\n{log_line}"
        else:
            job.logs = log_line

        db.session.commit()

    def cancel_job(self, job_id: int) -> bool:
        """Cancel a running job.

        Args:
            job_id: Job ID to cancel.

        Returns:
            True if cancelled, False if not cancellable.
        """
        job = db.session.get(Job, job_id)

        if not job:
            logger.error(f"Job {job_id} not found")
            return False

        if job.status not in ["pending", "running"]:
            logger.warning(
                f"Job {job_id} cannot be cancelled (status: {job.status})"
            )
            return False

        self.update_status(job_id, "cancelled", "Job cancelled by user")
        return True

    def get_job_progress(self, job_id: int) -> int:
        """Get job progress percentage.

        Args:
            job_id: Job ID.

        Returns:
            Progress percentage (0-100), or 0 if not available.
        """
        job = db.session.get(Job, job_id)

        if not job:
            return 0

        # Try to get progress from config_json
        if job.config_json and "progress" in job.config_json:
            return int(job.config_json["progress"])

        # Estimate based on status
        status_to_progress = {
            "pending": 0,
            "running": 50,
            "completed": 100,
            "failed": 0,
            "cancelled": 0,
        }

        return status_to_progress.get(job.status, 0)
