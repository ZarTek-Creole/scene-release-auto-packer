# 📋 Phase 8 : Jobs & Processing - Plan d'Implémentation

**Date** : 2025-11-03  
**Objectif** : Implémenter système complet de gestion des jobs avec traitement asynchrone

---

## 🎯 SCOPE PHASE 8

### Fonctionnalités Requises

1. **JobService** : Service métier pour traiter les jobs
   - Traitement jobs en attente
   - Mise à jour statut (pending → running → completed/failed)
   - Gestion logs
   - Gestion progression

2. **Blueprint jobs.py** : API REST complète
   - `GET /api/jobs` : Liste jobs avec filtres (status, job_type, release_id, user_id)
   - `GET /api/jobs/{id}` : Détails job complet
   - `GET /api/jobs/{id}/logs` : Logs job (temps réel)
   - `GET /api/jobs/{id}/status` : Statut job
   - `PUT /api/jobs/{id}/cancel` : Annuler job en cours
   - `GET /api/releases/{id}/jobs` : Jobs d'une release

3. **Endpoints Wizard** :
   - `GET /api/wizard/jobs/{job_id}/status` : Statut job wizard
   - `GET /api/wizard/jobs/{job_id}/logs` : Logs job wizard
   - `GET /api/wizard/jobs/{job_id}/analysis` : Résultats analyse

---

## 📊 MODÈLE JOB EXISTANT

Le modèle `Job` existe déjà (`web/models/job.py`) :

```python
class Job(db.Model):
    id: int (PK)
    release_id: int | None (FK releases.id)
    status: str (pending, running, completed, failed)
    job_type: str | None (nfofix, readnfo, repack, dirfix, packaging, etc.)
    config_json: dict (JSON configuration)
    logs: str | None (TEXT logs)
    created_at: datetime
    created_by: int (FK users.id)
```

**Statuts possibles** :
- `pending` : En attente de traitement
- `running` : En cours de traitement
- `completed` : Terminé avec succès
- `failed` : Échec
- `cancelled` : Annulé
- `draft` : Draft (wizard)

---

## 🏗️ ARCHITECTURE

### 1. JobService (`web/services/job_service.py`)

**Responsabilités** :
- Traitement jobs asynchrone (simulation pour l'instant)
- Mise à jour statut jobs
- Gestion logs (append_log)
- Gestion progression

**Méthodes principales** :
```python
class JobService:
    def process_job(job_id: int) -> None:
        """Traiter un job de manière asynchrone."""
        
    def update_status(job_id: int, status: str, logs: str | None = None) -> None:
        """Mettre à jour statut job."""
        
    def append_log(job_id: int, log_message: str, level: str = "INFO") -> None:
        """Ajouter log au job."""
        
    def cancel_job(job_id: int) -> bool:
        """Annuler job en cours."""
```

### 2. Blueprint jobs.py (`web/blueprints/jobs.py`)

**Endpoints** :
- `GET /api/jobs` : Liste avec filtres/pagination
- `GET /api/jobs/{id}` : Détails job
- `GET /api/jobs/{id}/logs` : Logs
- `GET /api/jobs/{id}/status` : Statut
- `PUT /api/jobs/{id}/cancel` : Annulation

**Permissions** :
- READ : Tous utilisateurs (leurs jobs) ou admin (tous)
- WRITE/MOD : Owner ou admin

### 3. Endpoints Releases (`web/blueprints/releases.py`)

**Ajouter** :
- `GET /api/releases/{id}/jobs` : Jobs d'une release

### 4. Endpoints Wizard (`web/blueprints/wizard.py`)

**Ajouter** :
- `GET /api/wizard/jobs/{job_id}/status`
- `GET /api/wizard/jobs/{job_id}/logs`
- `GET /api/wizard/jobs/{job_id}/analysis`

---

## 🧪 TESTS REQUIS (Coverage ≥90%)

### Tests JobService
- `test_process_job_success`
- `test_process_job_failure`
- `test_update_status`
- `test_append_log`
- `test_cancel_job`

### Tests API Jobs
- `test_list_jobs`
- `test_list_jobs_with_filters`
- `test_get_job`
- `test_get_job_not_found`
- `test_get_job_logs`
- `test_get_job_status`
- `test_cancel_job`
- `test_cancel_job_permission_denied`
- `test_list_release_jobs`

### Tests Wizard Jobs
- `test_wizard_job_status`
- `test_wizard_job_logs`
- `test_wizard_job_analysis`

---

## 📝 DÉPENDANCES

- ✅ Phase 1 : Infrastructure Core
- ✅ Phase 4 : Releases Management
- ✅ Phase 6 : Users & Roles (Permissions)
- ✅ Phase 7 : Configurations

---

## ✅ CRITÈRES DE VALIDATION

- ✅ JobService créé et testé (coverage ≥90%)
- ✅ Blueprint jobs.py créé et testé (coverage ≥90%)
- ✅ Endpoints releases/{id}/jobs implémenté
- ✅ Endpoints wizard/jobs/{id}/* implémentés
- ✅ Tous tests passent
- ✅ Documentation mise à jour

---

**Dernière mise à jour** : 2025-11-03
