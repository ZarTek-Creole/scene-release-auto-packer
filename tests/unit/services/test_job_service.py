"""Tests unitaires pour JobService.

Ces tests vérifient la gestion des jobs asynchrones : création, transitions d'état,
gestion des logs, et suivi de progression.

Approche TDD : Tests écrits avant toute modification du service.
"""

from __future__ import annotations

import pytest
from web.extensions import db
from web.models import Job, User
from web.services.job import JobService


class TestJobService:
    """Tests unitaires pour JobService."""

    def test_process_job_success(self, app) -> None:
        """Test traitement réussi d'un job en statut pending.

        Vérifie que la méthode process_job traite correctement un job
        et effectue les transitions d'état attendues.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job en statut pending
        job = Job(
            status="pending",
            job_type="nfofix",
            config_json={},
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Traitement du job
        service.process_job(job.id)

        # Vérification que le job est maintenant completed
        db.session.refresh(job)
        assert job.status == "completed"
        assert "NFOFIX job completed" in job.logs
        assert "Fixing NFO file" in job.logs

    def test_process_job_not_found(self, app) -> None:
        """Test traitement d'un job inexistant.

        Vérifie que la méthode gère correctement le cas d'un job qui n'existe pas.
        """
        service = JobService()

        # Tentative de traitement d'un job inexistant
        service.process_job(99999)

        # Ne doit pas lever d'exception, juste logger l'erreur
        # (vérification via logs si nécessaire)

    def test_process_job_not_pending(self, app) -> None:
        """Test traitement d'un job qui n'est pas en statut pending.

        Vérifie que la méthode refuse de traiter un job déjà en cours ou terminé.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job déjà completed
        job = Job(
            status="completed",
            job_type="nfofix",
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Tentative de traitement (doit être refusée)
        service.process_job(job.id)

        # Vérification que le statut n'a pas changé
        db.session.refresh(job)
        assert job.status == "completed"

    def test_process_job_transitions(self, app) -> None:
        """Test transitions d'état valides lors du traitement.

        Vérifie que les transitions d'état suivent le cycle :
        pending → running → completed
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job
        job = Job(
            status="pending",
            job_type="readnfo",
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Vérification état initial
        assert job.status == "pending"

        # Traitement du job
        service.process_job(job.id)

        # Vérification transition vers completed
        db.session.refresh(job)
        assert job.status == "completed"
        assert "running" in job.logs or "READNFO job completed" in job.logs

    def test_process_job_error_handling(self, app) -> None:
        """Test gestion des erreurs lors du traitement.

        Vérifie que les erreurs sont correctement capturées et que le job
        passe en statut "failed" avec les logs d'erreur appropriés.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job avec configuration invalide (pour déclencher erreur)
        job = Job(
            status="pending",
            job_type="nfofix",
            config_json={"action": "invalid_action"},
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Traitement du job (doit déclencher une erreur)
        service.process_job(job.id)

        # Vérification que le job est en statut failed
        db.session.refresh(job)
        assert job.status == "failed"
        assert "ERROR" in job.logs or "failed" in job.logs.lower()
        assert "Invalid action" in job.logs

    def test_update_status(self, app) -> None:
        """Test mise à jour du statut d'un job.

        Vérifie que la méthode update_status met à jour correctement le statut
        et ajoute les logs si fournis.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job
        job = Job(
            status="pending",
            job_type="repack",
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Mise à jour du statut avec log
        service.update_status(job.id, "running", "Job started")

        # Vérification
        db.session.refresh(job)
        assert job.status == "running"
        assert "Job started" in job.logs
        assert job.logs.startswith("[")  # Format timestamp

    def test_update_status_no_logs(self, app) -> None:
        """Test mise à jour du statut sans logs.

        Vérifie que la méthode update_status fonctionne sans logs optionnels.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job
        job = Job(
            status="pending",
            job_type="dirfix",
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Mise à jour du statut sans logs
        service.update_status(job.id, "running")

        # Vérification
        db.session.refresh(job)
        assert job.status == "running"

    def test_append_log(self, app) -> None:
        """Test ajout de logs à un job.

        Vérifie que la méthode append_log ajoute correctement des logs
        avec niveau de sévérité.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job
        job = Job(
            status="running",
            job_type="nfofix",
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Ajout de logs
        service.append_log(job.id, "Processing step 1", "INFO")
        service.append_log(job.id, "Warning: minor issue", "WARNING")
        service.append_log(job.id, "Critical error", "ERROR")

        # Vérification
        db.session.refresh(job)
        assert "Processing step 1" in job.logs
        assert "[INFO]" in job.logs
        assert "[WARNING]" in job.logs
        assert "[ERROR]" in job.logs
        assert job.logs.count("\n") >= 2  # Au moins 2 sauts de ligne (3 logs)

    def test_append_log_not_found(self, app) -> None:
        """Test ajout de logs à un job inexistant.

        Vérifie que la méthode gère correctement le cas d'un job qui n'existe pas.
        """
        service = JobService()

        # Tentative d'ajout de log à un job inexistant
        service.append_log(99999, "Test log", "INFO")

        # Ne doit pas lever d'exception, juste logger l'erreur

    def test_cancel_job_pending(self, app) -> None:
        """Test annulation d'un job en statut pending.

        Vérifie qu'un job en attente peut être annulé correctement.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job en pending
        job = Job(
            status="pending",
            job_type="repack",
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Annulation du job
        result = service.cancel_job(job.id)

        # Vérification
        assert result is True
        db.session.refresh(job)
        assert job.status == "cancelled"
        assert "cancelled" in job.logs.lower()

    def test_cancel_job_running(self, app) -> None:
        """Test annulation d'un job en statut running.

        Vérifie qu'un job en cours peut être annulé correctement.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job en running
        job = Job(
            status="running",
            job_type="dirfix",
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Annulation du job
        result = service.cancel_job(job.id)

        # Vérification
        assert result is True
        db.session.refresh(job)
        assert job.status == "cancelled"

    def test_cancel_job_completed(self, app) -> None:
        """Test annulation d'un job déjà terminé.

        Vérifie qu'un job terminé ne peut pas être annulé.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job completed
        job = Job(
            status="completed",
            job_type="nfofix",
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Tentative d'annulation (doit échouer)
        result = service.cancel_job(job.id)

        # Vérification
        assert result is False
        db.session.refresh(job)
        assert job.status == "completed"  # Statut inchangé

    def test_cancel_job_not_found(self, app) -> None:
        """Test annulation d'un job inexistant.

        Vérifie que la méthode gère correctement le cas d'un job qui n'existe pas.
        """
        service = JobService()

        # Tentative d'annulation d'un job inexistant
        result = service.cancel_job(99999)

        # Vérification
        assert result is False

    def test_get_job_progress_from_config(self, app) -> None:
        """Test récupération progression depuis config_json.

        Vérifie que la progression peut être lue depuis config_json si disponible.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job avec progression dans config_json
        job = Job(
            status="running",
            job_type="repack",
            config_json={"progress": 75},
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Récupération de la progression
        progress = service.get_job_progress(job.id)

        # Vérification
        assert progress == 75

    def test_get_job_progress_from_status(self, app) -> None:
        """Test estimation progression basée sur statut.

        Vérifie que la progression est estimée correctement selon le statut
        si config_json ne contient pas de progression.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Test avec différents statuts
        test_cases = [
            ("pending", 0),
            ("running", 50),
            ("completed", 100),
            ("failed", 0),
            ("cancelled", 0),
        ]

        for status, expected_progress in test_cases:
            job = Job(
                status=status,
                job_type="nfofix",
                created_by=user.id
            )
            db.session.add(job)
            db.session.commit()

            progress = service.get_job_progress(job.id)
            assert progress == expected_progress, f"Progress mismatch for status {status}"

            # Nettoyage pour le prochain test
            db.session.delete(job)
            db.session.commit()

    def test_get_job_progress_not_found(self, app) -> None:
        """Test récupération progression d'un job inexistant.

        Vérifie que la méthode retourne 0 pour un job qui n'existe pas.
        """
        service = JobService()

        # Récupération de la progression d'un job inexistant
        progress = service.get_job_progress(99999)

        # Vérification
        assert progress == 0

    def test_process_job_types(self, app) -> None:
        """Test traitement des différents types de jobs.

        Vérifie que chaque type de job est traité correctement par sa méthode spécialisée.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Test de chaque type de job
        job_types = ["nfofix", "readnfo", "repack", "dirfix"]

        for job_type in job_types:
            job = Job(
                status="pending",
                job_type=job_type,
                created_by=user.id
            )
            db.session.add(job)
            db.session.commit()

            # Traitement du job
            service.process_job(job.id)

            # Vérification que le job est completed
            db.session.refresh(job)
            assert job.status == "completed", f"Job type {job_type} should be completed"
            assert job_type.upper() in job.logs or "completed" in job.logs.lower()

            # Nettoyage pour le prochain test
            db.session.delete(job)
            db.session.commit()

    def test_process_job_generic_type(self, app) -> None:
        """Test traitement d'un job avec type générique.

        Vérifie qu'un job avec un type non spécialisé utilise le traitement générique.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job avec type générique
        job = Job(
            status="pending",
            job_type="unknown_type",
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Traitement du job
        service.process_job(job.id)

        # Vérification que le job est completed avec traitement générique
        db.session.refresh(job)
        assert job.status == "completed"
        assert "unknown_type" in job.logs or "Processing job type" in job.logs

    def test_update_status_invalid_transition(self, app) -> None:
        """Test mise à jour statut avec transition invalide.

        Vérifie que la méthode lève une exception pour les transitions invalides.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job completed
        job = Job(
            status="completed",
            job_type="nfofix",
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Tentative de transition invalide (completed → pending)
        with pytest.raises(ValueError, match="Transition invalide"):
            service.update_status(job.id, "pending", "Invalid transition")

    def test_update_status_not_found(self, app) -> None:
        """Test mise à jour statut avec job inexistant.

        Vérifie que la méthode gère correctement le cas d'un job qui n'existe pas.
        """
        service = JobService()

        # Tentative de mise à jour d'un job inexistant
        service.update_status(99999, "running", "Test")

        # Ne doit pas lever d'exception, juste logger l'erreur

    def test_process_job_invalid_transition(self, app) -> None:
        """Test traitement job avec transition invalide.

        Vérifie que la méthode gère correctement les transitions invalides.
        """
        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job avec statut invalide pour traitement
        # On crée un job directement en "completed" (sans passer par "pending")
        job = Job(
            status="completed",
            job_type="nfofix",
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Tentative de traitement (doit être refusée car pas en "pending")
        service.process_job(job.id)

        # Vérification que le statut n'a pas changé
        db.session.refresh(job)
        assert job.status == "completed"

    def test_process_job_invalid_transition_error(self, app) -> None:
        """Test traitement job avec InvalidTransitionError.

        Vérifie que la méthode gère correctement InvalidTransitionError lors de la validation.
        """
        from unittest.mock import patch
        from web.services.job.job_state_machine import InvalidTransitionError

        service = JobService()

        # Création d'un utilisateur de test
        user = User(username="testuser", email="test@test.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Création d'un job en pending
        job = Job(
            status="pending",
            job_type="nfofix",
            created_by=user.id
        )
        db.session.add(job)
        db.session.commit()

        # Mock pour simuler InvalidTransitionError
        with patch.object(service.state_machine, 'validate_transition', side_effect=InvalidTransitionError("pending", "running")):
            service.process_job(job.id)

        # Vérification que le job n'a pas été traité
        db.session.refresh(job)
        assert job.status == "pending"  # Statut inchangé
