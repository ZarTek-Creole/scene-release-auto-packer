"""Tests unitaires pour JobStateMachine.

Ce module teste la machine à états finis pour les transitions d'état des jobs.
La machine à états garantit que seules les transitions valides sont autorisées,
évitant ainsi les transitions invalides comme PENDING → COMPLETED sans passer par RUNNING.
"""

from __future__ import annotations

import pytest

from web.services.job.job_state_machine import JobStateMachine, InvalidTransitionError


class TestJobStateMachine:
    """Tests unitaires pour JobStateMachine."""

    def test_can_transition_pending_to_running(self):
        """Test transition valide PENDING → RUNNING."""
        machine = JobStateMachine()
        assert machine.can_transition("pending", "running") is True

    def test_can_transition_running_to_completed(self):
        """Test transition valide RUNNING → COMPLETED."""
        machine = JobStateMachine()
        assert machine.can_transition("running", "completed") is True

    def test_can_transition_running_to_failed(self):
        """Test transition valide RUNNING → FAILED."""
        machine = JobStateMachine()
        assert machine.can_transition("running", "failed") is True

    def test_can_transition_running_to_cancelled(self):
        """Test transition valide RUNNING → CANCELLED."""
        machine = JobStateMachine()
        assert machine.can_transition("running", "cancelled") is True

    def test_can_transition_pending_to_cancelled(self):
        """Test transition valide PENDING → CANCELLED."""
        machine = JobStateMachine()
        assert machine.can_transition("pending", "cancelled") is True

    def test_cannot_transition_pending_to_completed(self):
        """Test transition invalide PENDING → COMPLETED (doit passer par RUNNING)."""
        machine = JobStateMachine()
        assert machine.can_transition("pending", "completed") is False

    def test_cannot_transition_pending_to_failed(self):
        """Test transition invalide PENDING → FAILED (doit passer par RUNNING)."""
        machine = JobStateMachine()
        assert machine.can_transition("pending", "failed") is False

    def test_cannot_transition_completed_to_running(self):
        """Test transition invalide COMPLETED → RUNNING (état final)."""
        machine = JobStateMachine()
        assert machine.can_transition("completed", "running") is False

    def test_cannot_transition_failed_to_running(self):
        """Test transition invalide FAILED → RUNNING (état final)."""
        machine = JobStateMachine()
        assert machine.can_transition("failed", "running") is False

    def test_cannot_transition_cancelled_to_running(self):
        """Test transition invalide CANCELLED → RUNNING (état final)."""
        machine = JobStateMachine()
        assert machine.can_transition("cancelled", "running") is False

    def test_validate_transition_success(self):
        """Test validation transition valide ne lève pas d'exception."""
        machine = JobStateMachine()
        # Ne doit pas lever d'exception
        machine.validate_transition("pending", "running")

    def test_validate_transition_invalid_raises_error(self):
        """Test validation transition invalide lève InvalidTransitionError."""
        machine = JobStateMachine()
        with pytest.raises(InvalidTransitionError) as exc_info:
            machine.validate_transition("pending", "completed")
        
        assert "pending" in str(exc_info.value).lower()
        assert "completed" in str(exc_info.value).lower()

    def test_get_allowed_transitions_from_pending(self):
        """Test récupération transitions autorisées depuis PENDING."""
        machine = JobStateMachine()
        transitions = machine.get_allowed_transitions("pending")
        assert "running" in transitions
        assert "cancelled" in transitions
        assert "completed" not in transitions
        assert "failed" not in transitions

    def test_get_allowed_transitions_from_running(self):
        """Test récupération transitions autorisées depuis RUNNING."""
        machine = JobStateMachine()
        transitions = machine.get_allowed_transitions("running")
        assert "completed" in transitions
        assert "failed" in transitions
        assert "cancelled" in transitions
        assert "pending" not in transitions

    def test_get_allowed_transitions_from_final_states(self):
        """Test récupération transitions depuis états finaux (aucune transition)."""
        machine = JobStateMachine()
        final_states = ["completed", "failed", "cancelled"]
        
        for state in final_states:
            transitions = machine.get_allowed_transitions(state)
            assert len(transitions) == 0

    def test_invalid_status_raises_error(self):
        """Test statut invalide lève ValueError."""
        machine = JobStateMachine()
        
        with pytest.raises(ValueError):
            machine.can_transition("invalid_status", "running")
        
        with pytest.raises(ValueError):
            machine.can_transition("pending", "invalid_status")
        
        with pytest.raises(ValueError):
            machine.get_allowed_transitions("invalid_status")

    def test_case_insensitive_status(self):
        """Test que les statuts sont gérés de manière case-insensitive."""
        machine = JobStateMachine()
        
        # Test avec différentes casses
        assert machine.can_transition("PENDING", "RUNNING") is True
        assert machine.can_transition("Pending", "Running") is True
        assert machine.can_transition("pending", "RUNNING") is True

