# 📡 API Reference - eBook Scene Packer v2

**Date** : 2025-11-01  
**Version** : 1.0.0  
**Statut** : Draft  
**Format** : OpenAPI 3.0 (Swagger)

---

## 🎯 Vue d'Ensemble

Documentation complète de l'API REST Flask pour eBook Scene Packer v2 avec tous les endpoints, schémas de requête/réponse, codes d'erreur et exemples.

**Base URL** : `http://localhost:5000/api` (développement)  
**Authentification** : JWT Bearer Token  
**Format** : JSON

---

## 📋 Table des Matières

1. [Authentification](#authentification)
2. [Dashboard](#dashboard)
3. [Wizard](#wizard)
4. [Releases](#releases)
5. [Rules](#rules)
6. [Users](#users)
7. [Roles](#roles)
8. [Configurations](#configurations)
9. [Schémas Communs](#schémas-communs)
10. [Codes d'Erreur](#codes-derreur)

---

## Authentification

### POST /api/auth/login

**Description** : Connexion utilisateur et obtention token JWT

**Requête** :
```json
{
  "username": "operator",
  "password": "securepassword123"
}
```

**Réponse 200** :
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "operator",
    "email": "operator@example.com",
    "roles": ["Operator"]
  }
}
```

**Erreurs** :
- `401 Unauthorized` : Credentials invalides
- `400 Bad Request` : Champs manquants

---

### POST /api/auth/refresh

**Description** : Rafraîchir access token avec refresh token

**Headers** :
```
Authorization: Bearer <refresh_token>
```

**Réponse 200** :
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Erreurs** :
- `401 Unauthorized` : Refresh token invalide/expiré

---

### POST /api/auth/logout

**Description** : Déconnexion (invalidation refresh token)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "message": "Logout successful"
}
```

---

### GET /api/auth/me

**Description** : Récupérer informations utilisateur connecté

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "id": 1,
  "username": "operator",
  "email": "operator@example.com",
  "note": "Operator account",
  "active": true,
  "roles": ["Operator"],
  "groups": ["TESTGROUP"],
  "permissions": {
    "releases": ["READ", "WRITE"],
    "rules": ["READ", "WRITE"]
  },
  "created_at": "2025-11-01T10:00:00Z"
}
```

---

## Dashboard

### GET /api/dashboard/stats

**Description** : Statistiques dashboard

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "releases_count": 150,
  "my_releases_count": 25,
  "releases_by_type": {
    "EBOOK": 100,
    "TV": 40,
    "DOCS": 10
  },
  "recent_releases": [
    {
      "id": 1,
      "group": "TESTGROUP",
      "type": "EBOOK",
      "created_at": "2025-11-01T10:00:00Z"
    }
  ]
}
```

---

## Wizard

### POST /api/wizard/step/{step}/validate

**Description** : Valider données étape wizard

**Path Parameters** :
- `step` : Numéro étape (1-9)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** (exemple étape 1 - Groupe) :
```json
{
  "group": "TESTGROUP"
}
```

**Réponse 200** :
```json
{
  "valid": true,
  "errors": []
}
```

**Réponse 200 (invalide)** :
```json
{
  "valid": false,
  "errors": ["Le nom du groupe doit contenir uniquement lettres majuscules et chiffres"]
}
```

---

### POST /api/wizard/step/{step}/save

**Description** : Sauvegarder progression étape wizard (backend draft)

**Path Parameters** :
- `step` : Numéro étape (1-9)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "data": {
    "group": "TESTGROUP",
    "release_type": "EBOOK",
    "rule_id": 1,
    "file_path": "/uploads/file.epub",
    // ... autres données étape
  }
}
```

**Réponse 200** :
```json
{
  "job_id": 123,
  "message": "Progress saved"
}
```

---

### GET /api/wizard/step/{step}/data

**Description** : Récupérer données étape sauvegardée

**Path Parameters** :
- `step` : Numéro étape (1-9)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** :
- `job_id` : ID job draft (optionnel)

**Réponse 200** :
```json
{
  "step": 1,
  "data": {
    "group": "TESTGROUP"
  }
}
```

---

### POST /api/wizard/pack

**Description** : Lancer packaging release (étape 8)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "job_id": 123,
  "options": {
    "format": "ZIP",
    "compression": "normal",
    "volumes": 50,
    "generate_nfo": true,
    "generate_diz": true,
    "generate_sfv": true
  }
}
```

**Réponse 200** :
```json
{
  "job_id": 124,
  "status": "running",
  "message": "Packaging started"
}
```

---

### GET /api/wizard/jobs/{job_id}/status

**Description** : Statut job packaging

**Path Parameters** :
- `job_id` : ID job

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "job_id": 124,
  "status": "running",
  "progress": 65,
  "message": "Packaging in progress..."
}
```

---

### GET /api/wizard/jobs/{job_id}/logs

**Description** : Logs job temps réel

**Path Parameters** :
- `job_id` : ID job

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** :
- `since` : Timestamp dernière récupération (optionnel)

**Réponse 200** :
```json
{
  "logs": [
    {
      "timestamp": "2025-11-01T10:05:00Z",
      "level": "INFO",
      "message": "Packaging started"
    },
    {
      "timestamp": "2025-11-01T10:05:30Z",
      "level": "INFO",
      "message": "File analyzed"
    }
  ]
}
```

---

### GET /api/wizard/jobs/{job_id}/analysis

**Description** : Résultats analyse fichier (étape 5)

**Path Parameters** :
- `job_id` : ID job

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "metadata": {
    "title": "Example Book",
    "author": "John Doe",
    "isbn": "1234567890",
    "year": 2024
  },
  "mediainfo": {
    "format": "EPUB",
    "size": 5242880
  },
  "structure": {
    "files": ["content.opf", "chapter1.xhtml"]
  }
}
```

---

### POST /api/wizard/step/5/analyze

**Description** : Lancer analyse fichier (étape 5)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "file_path": "/uploads/file.epub",
  "release_type": "EBOOK"
}
```

**Réponse 202** (Asynchrone) :
```json
{
  "job_id": 125,
  "status": "running",
  "message": "Analysis started"
}
```

---

### POST /api/wizard/step/6/enrich

**Description** : Enrichir métadonnées avec APIs (étape 6)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "metadata": {
    "title": "Example Book",
    "author": "John Doe"
  },
  "release_type": "EBOOK",
  "api_priority": ["OpenLibrary", "GoogleBooks"]
}
```

**Réponse 200** :
```json
{
  "enriched": {
    "title": "Example Book",
    "author": "John Doe",
    "isbn": "1234567890",
    "publisher": "Example Publisher",
    "year": 2024
  },
  "sources": {
    "isbn": "OpenLibrary",
    "publisher": "GoogleBooks"
  }
}
```

---

### POST /api/wizard/step/7/render

**Description** : Rendu prévisualisation template (étape 7)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "template_id": 1,
  "metadata": {
    "title": "Example Book",
    "author": "John Doe"
  }
}
```

**Réponse 200** :
```json
{
  "preview": "Title: Example Book\nAuthor: John Doe\n..."
}
```

---

## Releases

### GET /api/releases

**Description** : Liste releases avec filtres et pagination

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** :
- `type` : Type release (EBOOK, TV, DOCS, etc.) - multi
- `group` : Groupe Scene - multi
- `status` : Statut (draft, completed, failed) - multi
- `search` : Recherche textuelle
- `page` : Numéro page (défaut: 1)
- `per_page` : Items par page (défaut: 20)
- `sort` : Tri (created_at, name, size) - défaut: created_at
- `order` : Ordre (asc, desc) - défaut: desc
- `my_only` : Booléen - seulement mes releases

**Réponse 200** :
```json
{
  "releases": [
    {
      "id": 1,
      "group": "TESTGROUP",
      "type": "EBOOK",
      "status": "completed",
      "metadata": {
        "title": "Example Book"
      },
      "created_at": "2025-11-01T10:00:00Z",
      "user": {
        "id": 1,
        "username": "operator"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8
  }
}
```

---

### GET /api/releases/{id}

**Description** : Détail release

**Path Parameters** :
- `id` : ID release

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "id": 1,
  "group": "TESTGROUP",
  "type": "EBOOK",
  "status": "completed",
  "metadata": {
    "title": "Example Book",
    "author": "John Doe",
    "isbn": "1234567890"
  },
  "config": {
    "format": "ZIP",
    "volumes": 50
  },
  "file_path": "/releases/testgroup-example-book.epub",
  "created_at": "2025-11-01T10:00:00Z",
  "user": {
    "id": 1,
    "username": "operator"
  }
}
```

---

### PUT /api/releases/{id}

**Description** : Édition release (permission WRITE requise)

**Path Parameters** :
- `id` : ID release

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "metadata": {
    "title": "Updated Title",
    "author": "Updated Author"
  },
  "config": {
    "format": "RAR"
  }
}
```

**Réponse 200** :
```json
{
  "id": 1,
  "message": "Release updated"
}
```

---

### DELETE /api/releases/{id}

**Description** : Suppression release (admin uniquement)

**Path Parameters** :
- `id` : ID release

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "message": "Release deleted"
}
```

---

### POST /api/releases/{id}/repack

**Description** : Repackaging release (permission MOD requise)

**Path Parameters** :
- `id` : ID release

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** (optionnel) :
```json
{
  "options": {
    "format": "RAR",
    "compression": "high"
  }
}
```

**Réponse 200** :
```json
{
  "job_id": 126,
  "status": "running",
  "message": "Repackaging started"
}
```

---

### POST /api/releases/{id}/nfofix

**Description** : Correction NFO release (permission MOD requise)

**Path Parameters** :
- `id` : ID release

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "message": "NFO fixed",
  "changes": [
    "Encoding corrected to UTF-8",
    "Structure validated"
  ]
}
```

---

### POST /api/releases/{id}/readnfo

**Description** : Régénération depuis NFO (permission MOD requise)

**Path Parameters** :
- `id` : ID release

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "job_id": 127,
  "status": "running",
  "message": "Regeneration from NFO started"
}
```

---

### POST /api/releases/{id}/dirfix

**Description** : Correction structure répertoires (permission MOD requise)

**Path Parameters** :
- `id` : ID release

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "message": "Directory structure fixed",
  "changes": [
    "Filename corrected",
    "Structure validated"
  ]
}
```

---

### GET /api/releases/{id}/files

**Description** : Arborescence fichiers release

**Path Parameters** :
- `id` : ID release

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "files": [
    {
      "path": "testgroup-example-book.nfo",
      "size": 1024,
      "type": "file"
    },
    {
      "path": "testgroup-example-book.zip",
      "size": 5242880,
      "type": "file"
    }
  ]
}
```

---

### GET /api/releases/{id}/jobs

**Description** : Historique jobs release

**Path Parameters** :
- `id` : ID release

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "jobs": [
    {
      "id": 124,
      "status": "completed",
      "created_at": "2025-11-01T10:00:00Z"
    }
  ]
}
```

---

## Rules

### GET /api/rules

**Description** : Liste rules locales avec filtres

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** :
- `scene` : Scène (English, French, etc.)
- `section` : Section (eBOOK, TV-720p, etc.)
- `year` : Année
- `type` : Type release (filtrage automatique)
- `search` : Recherche textuelle
- `page` : Numéro page
- `per_page` : Items par page

**Réponse 200** :
```json
{
  "rules": [
    {
      "id": 1,
      "name": "eBOOK-2024",
      "scene": "English",
      "section": "eBOOK",
      "year": 2024,
      "created_at": "2025-11-01T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150
  }
}
```

---

### GET /api/rules/local

**Description** : Liste rules locales uniquement

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** : Identiques à `/api/rules`

**Réponse 200** : Identique à `/api/rules`

---

### GET /api/rules/scenerules

**Description** : Liste rules scenerules.org

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** :
- `scene` : Scène
- `section` : Section
- `year` : Année
- `type` : Type release
- `search` : Recherche textuelle

**Réponse 200** :
```json
{
  "rules": [
    {
      "name": "eBOOK-2024",
      "scene": "English",
      "section": "eBOOK",
      "year": 2024,
      "url": "https://scenerules.org/rules/eBOOK-2024.nfo",
      "downloaded": false
    }
  ]
}
```

---

### GET /api/rules/{id}

**Description** : Détail rule locale

**Path Parameters** :
- `id` : ID rule

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "id": 1,
  "name": "eBOOK-2024",
  "content": "Title: {{title}}\nAuthor: {{author}}\n...",
  "scene": "English",
  "section": "eBOOK",
  "year": 2024,
  "created_at": "2025-11-01T10:00:00Z",
  "updated_at": "2025-11-01T10:00:00Z"
}
```

---

### GET /api/rules/{id}/preview

**Description** : Prévisualisation rule (NFO viewer)

**Path Parameters** :
- `id` : ID rule

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "content": "Title: {{title}}\nAuthor: {{author}}\n...",
  "formatted": true
}
```

---

### POST /api/rules/upload

**Description** : Upload rule locale (permission WRITE requise)

**Headers** :
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Form Data** :
- `file` : Fichier NFO
- `name` : Nom rule (optionnel)
- `scene` : Scène (optionnel, auto-détecté si possible)
- `section` : Section (optionnel, auto-détecté si possible)
- `year` : Année (optionnel, auto-détecté si possible)

**Réponse 200** :
```json
{
  "id": 2,
  "message": "Rule uploaded successfully"
}
```

---

### POST /api/rules/download

**Description** : Téléchargement rule depuis scenerules.org (permission WRITE requise)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "name": "eBOOK-2024",
  "scene": "English",
  "section": "eBOOK",
  "year": 2024
}
```

**Réponse 200** :
```json
{
  "id": 3,
  "message": "Rule downloaded successfully"
}
```

---

### PUT /api/rules/{id}

**Description** : Édition rule locale (permission MOD requise)

**Path Parameters** :
- `id` : ID rule

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "name": "eBOOK-2024-Updated",
  "content": "Title: {{title}}\n...",
  "scene": "English",
  "section": "eBOOK",
  "year": 2024
}
```

**Réponse 200** :
```json
{
  "id": 1,
  "message": "Rule updated"
}
```

---

### DELETE /api/rules/{id}

**Description** : Suppression rule locale (permission MOD requise)

**Path Parameters** :
- `id` : ID rule

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "message": "Rule deleted"
}
```

---

### POST /api/rules/sync

**Description** : Synchronisation scenerules.org (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 202** (Asynchrone) :
```json
{
  "job_id": 128,
  "status": "running",
  "message": "Synchronization started"
}
```

---

## Users

### GET /api/users

**Description** : Liste utilisateurs (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** :
- `status` : Statut (active, inactive) - multi
- `role` : Rôle - multi
- `group` : Groupe - multi
- `search` : Recherche textuelle
- `page` : Numéro page
- `per_page` : Items par page

**Réponse 200** :
```json
{
  "users": [
    {
      "id": 1,
      "username": "operator",
      "email": "operator@example.com",
      "active": true,
      "roles": ["Operator"],
      "groups": ["TESTGROUP"],
      "created_at": "2025-11-01T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 50
  }
}
```

---

### GET /api/users/{id}

**Description** : Détail utilisateur (admin uniquement)

**Path Parameters** :
- `id` : ID utilisateur

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "id": 1,
  "username": "operator",
  "email": "operator@example.com",
  "note": "Operator account",
  "active": true,
  "roles": ["Operator"],
  "groups": ["TESTGROUP"],
  "permissions": {
    "releases": ["READ", "WRITE"],
    "rules": ["READ", "WRITE"]
  },
  "created_at": "2025-11-01T10:00:00Z",
  "modify_at": null,
  "created_by": null
}
```

---

### POST /api/users

**Description** : Création utilisateur (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "SecurePass123",
  "note": "New operator",
  "active": true
}
```

**Réponse 201** :
```json
{
  "id": 2,
  "username": "newuser",
  "message": "User created"
}
```

**Erreurs** :
- `400 Bad Request` : Validation échouée (username unique, password force, etc.)

---

### PUT /api/users/{id}

**Description** : Modification utilisateur (admin uniquement)

**Path Parameters** :
- `id` : ID utilisateur

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "email": "updated@example.com",
  "note": "Updated note",
  "password": "NewSecurePass123",
  "active": true
}
```

**Réponse 200** :
```json
{
  "id": 2,
  "message": "User updated"
}
```

---

### DELETE /api/users/{id}

**Description** : Suppression/désactivation utilisateur (admin uniquement)

**Path Parameters** :
- `id` : ID utilisateur

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** :
- `permanent` : Booléen - suppression définitive (défaut: false = désactivation)

**Réponse 200** :
```json
{
  "message": "User deleted"
}
```

---

### POST /api/users/{id}/groups

**Description** : Affectation groupes utilisateur (admin uniquement)

**Path Parameters** :
- `id` : ID utilisateur

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "group_ids": [1, 2, 3]
}
```

**Réponse 200** :
```json
{
  "message": "Groups assigned",
  "groups": [
    {"id": 1, "name": "TESTGROUP"},
    {"id": 2, "name": "OTHERGROUP"}
  ]
}
```

---

### DELETE /api/users/{id}/groups/{group_id}

**Description** : Retrait groupe utilisateur (admin uniquement)

**Path Parameters** :
- `id` : ID utilisateur
- `group_id` : ID groupe

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "message": "Group removed"
}
```

---

### POST /api/users/{id}/roles

**Description** : Affectation rôle utilisateur (admin uniquement)

**Path Parameters** :
- `id` : ID utilisateur

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "role_id": 1
}
```

**Réponse 200** :
```json
{
  "message": "Role assigned",
  "role": {
    "id": 1,
    "name": "Operator"
  }
}
```

---

### GET /api/users/{id}/permissions

**Description** : Récupération permissions utilisateur (admin uniquement)

**Path Parameters** :
- `id` : ID utilisateur

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "role_permissions": {
    "releases": ["READ", "WRITE"],
    "rules": ["READ", "WRITE"]
  },
  "custom_permissions": {
    "releases": ["MOD"]
  },
  "final_permissions": {
    "releases": ["READ", "WRITE", "MOD"],
    "rules": ["READ", "WRITE"]
  }
}
```

---

### PUT /api/users/{id}/permissions

**Description** : Configuration permissions personnalisées utilisateur (admin uniquement)

**Path Parameters** :
- `id` : ID utilisateur

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "permissions": [
    {
      "resource": "releases",
      "action": "MOD"
    },
    {
      "resource": "rules",
      "action": "DELETE"
    }
  ]
}
```

**Réponse 200** :
```json
{
  "message": "Permissions updated"
}
```

---

## Roles

### GET /api/roles

**Description** : Liste rôles

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "roles": [
    {
      "id": 1,
      "name": "Admin",
      "description": "Administrateur avec accès complet",
      "users_count": 2,
      "created_at": "2025-11-01T10:00:00Z"
    },
    {
      "id": 2,
      "name": "Operator",
      "description": "Opérateur packaging uniquement",
      "users_count": 10,
      "created_at": "2025-11-01T10:00:00Z"
    }
  ]
}
```

---

### GET /api/roles/{id}

**Description** : Détail rôle

**Path Parameters** :
- `id` : ID rôle

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "id": 1,
  "name": "Admin",
  "description": "Administrateur avec accès complet",
  "permissions": {
    "releases": ["READ", "WRITE", "MOD", "DELETE"],
    "rules": ["READ", "WRITE", "MOD", "DELETE"],
    "users": ["READ", "WRITE", "MOD", "DELETE"],
    "roles": ["READ", "WRITE", "MOD", "DELETE"],
    "config": ["READ", "WRITE", "MOD", "DELETE"]
  },
  "users_count": 2,
  "created_at": "2025-11-01T10:00:00Z"
}
```

---

### POST /api/roles

**Description** : Création rôle (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "name": "CustomRole",
  "description": "Custom role description"
}
```

**Réponse 201** :
```json
{
  "id": 3,
  "message": "Role created"
}
```

---

### PUT /api/roles/{id}

**Description** : Modification rôle (admin uniquement)

**Path Parameters** :
- `id` : ID rôle

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "name": "UpdatedRole",
  "description": "Updated description"
}
```

**Réponse 200** :
```json
{
  "id": 3,
  "message": "Role updated"
}
```

---

### DELETE /api/roles/{id}

**Description** : Suppression rôle (admin uniquement)

**Path Parameters** :
- `id` : ID rôle

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** :
- `reassign_to` : ID rôle pour réassigner utilisateurs (optionnel)

**Réponse 200** :
```json
{
  "message": "Role deleted",
  "users_reassigned": 5
}
```

**Erreurs** :
- `400 Bad Request` : Rôle utilisé par utilisateurs sans réassignation

---

### GET /api/roles/{id}/permissions

**Description** : Récupération permissions rôle

**Path Parameters** :
- `id` : ID rôle

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "permissions": {
    "releases": ["READ", "WRITE"],
    "rules": ["READ", "WRITE"],
    "users": ["READ"],
    "roles": ["READ"],
    "config": ["READ"]
  }
}
```

---

### PUT /api/roles/{id}/permissions

**Description** : Configuration permissions rôle (admin uniquement)

**Path Parameters** :
- `id` : ID rôle

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "permissions": {
    "releases": ["READ", "WRITE", "MOD"],
    "rules": ["READ", "WRITE"],
    "users": [],
    "roles": [],
    "config": []
  }
}
```

**Réponse 200** :
```json
{
  "message": "Permissions updated",
  "users_affected": 10
}
```

---

### GET /api/roles/{id}/users

**Description** : Liste utilisateurs ayant ce rôle

**Path Parameters** :
- `id` : ID rôle

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "users": [
    {
      "id": 1,
      "username": "operator",
      "email": "operator@example.com",
      "active": true
    }
  ]
}
```

---

## Configurations

### GET /api/config/system

**Description** : Récupération paramètres système (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "paths": {
    "uploads": "/uploads",
    "releases": "/releases",
    "cache": "/cache",
    "logs": "/logs"
  },
  "limits": {
    "max_file_size": 21474836480,
    "api_timeout": 30,
    "ftp_timeout": 60
  },
  "logs": {
    "level": "INFO",
    "rotation_size": 10485760,
    "rotation_count": 10,
    "format": "JSON"
  }
}
```

---

### PUT /api/config/system

**Description** : Mise à jour paramètres système (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "paths": {
    "uploads": "/new/uploads"
  },
  "limits": {
    "max_file_size": 10737418240
  },
  "logs": {
    "level": "DEBUG"
  }
}
```

**Réponse 200** :
```json
{
  "message": "System settings updated"
}
```

---

### GET /api/config/apis

**Description** : Liste configurations APIs (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** :
- `user_id` : ID utilisateur (optionnel, filtrage)

**Réponse 200** :
```json
{
  "apis": [
    {
      "id": 1,
      "name": "OpenLibrary",
      "active": true,
      "user_id": null,
      "configured": true,
      "created_at": "2025-11-01T10:00:00Z"
    },
    {
      "id": 2,
      "name": "GoogleBooks",
      "active": true,
      "user_id": 1,
      "configured": true,
      "created_at": "2025-11-01T10:00:00Z"
    }
  ]
}
```

---

### POST /api/config/apis

**Description** : Création configuration API (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "name": "GoogleBooks",
  "api_key": "AIzaSyC-example-key",
  "active": true,
  "user_id": null
}
```

**Réponse 201** :
```json
{
  "id": 3,
  "message": "API config created"
}
```

**Note** : `api_key` est chiffré avant stockage (Fernet).

---

### PUT /api/config/apis/{id}

**Description** : Modification configuration API (admin uniquement)

**Path Parameters** :
- `id` : ID configuration

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "api_key": "AIzaSyC-new-key",
  "active": false
}
```

**Réponse 200** :
```json
{
  "id": 3,
  "message": "API config updated"
}
```

---

### DELETE /api/config/apis/{id}

**Description** : Suppression configuration API (admin uniquement)

**Path Parameters** :
- `id` : ID configuration

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "message": "API config deleted"
}
```

---

### POST /api/config/apis/{id}/test

**Description** : Test connexion API

**Path Parameters** :
- `id` : ID configuration

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** (optionnel) :
```json
{
  "query": "test search"
}
```

**Réponse 200** :
```json
{
  "success": true,
  "message": "API connection successful",
  "response_time": 245
}
```

**Réponse 200 (échec)** :
```json
{
  "success": false,
  "message": "Invalid API key",
  "error": "401 Unauthorized"
}
```

---

### GET /api/config/destinations

**Description** : Liste destinations FTP/SSH (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** :
- `user_id` : ID utilisateur (optionnel, filtrage)

**Réponse 200** :
```json
{
  "destinations": [
    {
      "id": 1,
      "name": "Production FTP",
      "host": "ftp.example.com",
      "port": 21,
      "user": "ftpuser",
      "type": "FTP",
      "user_id": null,
      "created_at": "2025-11-01T10:00:00Z"
    }
  ]
}
```

**Note** : `password_encrypted` n'est jamais retourné dans la réponse.

---

### POST /api/config/destinations

**Description** : Création destination FTP/SSH (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "name": "Production FTP",
  "host": "ftp.example.com",
  "port": 21,
  "user": "ftpuser",
  "password": "ftppassword",
  "type": "FTP",
  "options": {
    "passive": true,
    "timeout": 60
  },
  "user_id": null
}
```

**Réponse 201** :
```json
{
  "id": 1,
  "message": "Destination created"
}
```

**Note** : `password` est chiffré avant stockage (Fernet).

---

### PUT /api/config/destinations/{id}

**Description** : Modification destination (admin uniquement)

**Path Parameters** :
- `id` : ID destination

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "host": "new.ftp.example.com",
  "password": "newpassword",
  "options": {
    "passive": false
  }
}
```

**Réponse 200** :
```json
{
  "id": 1,
  "message": "Destination updated"
}
```

---

### DELETE /api/config/destinations/{id}

**Description** : Suppression destination (admin uniquement)

**Path Parameters** :
- `id` : ID destination

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "message": "Destination deleted"
}
```

---

### POST /api/config/destinations/{id}/test

**Description** : Test connexion FTP/SSH

**Path Parameters** :
- `id` : ID destination

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "success": true,
  "message": "Connection successful",
  "response_time": 1250
}
```

**Réponse 200 (échec)** :
```json
{
  "success": false,
  "message": "Connection failed: Timeout",
  "error": "TimeoutError"
}
```

---

### GET /api/config/templates

**Description** : Configuration stockage templates (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Réponse 200** :
```json
{
  "storage": "db",
  "disk_path": null,
  "templates_count": 10
}
```

**Réponse 200 (si disque)** :
```json
{
  "storage": "disk",
  "disk_path": "/templates",
  "templates_count": 15
}
```

---

### PUT /api/config/templates

**Description** : Mise à jour configuration stockage templates (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "storage": "disk",
  "disk_path": "/templates"
}
```

**Réponse 200** :
```json
{
  "message": "Template storage updated"
}
```

---

### POST /api/config/templates/migrate

**Description** : Migration templates (disque ↔ DB) (admin uniquement)

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "from": "db",
  "to": "disk",
  "disk_path": "/templates"
}
```

**Réponse 202** (Asynchrone) :
```json
{
  "job_id": 129,
  "status": "running",
  "message": "Migration started"
}
```

---

### GET /api/config/preferences

**Description** : Préférences utilisateur connecté

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** :
- `key` : Clé préférence spécifique (optionnel)

**Réponse 200** :
```json
{
  "preferences": {
    "api_priority_order": ["OpenLibrary", "GoogleBooks"],
    "wizard_defaults": {
      "group": "TESTGROUP",
      "release_type": "EBOOK"
    },
    "list_filters": {
      "type": ["EBOOK"],
      "status": ["completed"]
    },
    "view_mode": "cards"
  }
}
```

---

### PUT /api/config/preferences

**Description** : Mise à jour préférences utilisateur

**Headers** :
```
Authorization: Bearer <access_token>
```

**Requête** :
```json
{
  "api_priority_order": ["GoogleBooks", "OpenLibrary"],
  "view_mode": "table"
}
```

**Réponse 200** :
```json
{
  "message": "Preferences updated"
}
```

---

## Schémas Communs

### User Object

```json
{
  "id": 1,
  "username": "operator",
  "email": "operator@example.com",
  "note": "Operator account",
  "active": true,
  "roles": ["Operator"],
  "groups": ["TESTGROUP"],
  "created_at": "2025-11-01T10:00:00Z"
}
```

### Release Object

```json
{
  "id": 1,
  "group": "TESTGROUP",
  "type": "EBOOK",
  "status": "completed",
  "metadata": {
    "title": "Example Book",
    "author": "John Doe",
    "isbn": "1234567890"
  },
  "config": {
    "format": "ZIP",
    "volumes": 50
  },
  "file_path": "/releases/testgroup-example-book.epub",
  "created_at": "2025-11-01T10:00:00Z",
  "user": {
    "id": 1,
    "username": "operator"
  }
}
```

### Job Object

```json
{
  "id": 124,
  "release_id": 1,
  "status": "completed",
  "config_json": {
    "format": "ZIP",
    "compression": "normal"
  },
  "logs": "Packaging started...\nFile analyzed...\nPackaging completed.",
  "created_at": "2025-11-01T10:00:00Z",
  "created_by": 1
}
```

### Rule Object

```json
{
  "id": 1,
  "name": "eBOOK-2024",
  "content": "Title: {{title}}\nAuthor: {{author}}\n...",
  "scene": "English",
  "section": "eBOOK",
  "year": 2024,
  "created_at": "2025-11-01T10:00:00Z",
  "updated_at": "2025-11-01T10:00:00Z"
}
```

### Pagination Object

```json
{
  "page": 1,
  "per_page": 20,
  "total": 150,
  "pages": 8
}
```

### Error Object

```json
{
  "error": "ValidationError",
  "message": "Le nom du groupe doit contenir uniquement lettres majuscules et chiffres",
  "errors": {
    "group": ["Format invalide"]
  }
}
```

---

## Codes d'Erreur

### 200 OK
Requête réussie

### 201 Created
Ressource créée avec succès

### 202 Accepted
Requête acceptée, traitement asynchrone

### 400 Bad Request
Requête invalide (validation échouée, champs manquants)

**Exemple** :
```json
{
  "error": "ValidationError",
  "message": "Invalid input",
  "errors": {
    "username": ["Username is required"],
    "password": ["Password must be at least 8 characters"]
  }
}
```

### 401 Unauthorized
Non authentifié ou token invalide/expiré

**Exemple** :
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

### 403 Forbidden
Authentifié mais pas permission (READ/WRITE/MOD)

**Exemple** :
```json
{
  "error": "Forbidden",
  "message": "You don't have WRITE permission on releases"
}
```

### 404 Not Found
Ressource non trouvée

**Exemple** :
```json
{
  "error": "NotFound",
  "message": "Release with id 999 not found"
}
```

### 409 Conflict
Conflit (ex: username dupliqué)

**Exemple** :
```json
{
  "error": "Conflict",
  "message": "Username already exists"
}
```

### 422 Unprocessable Entity
Entité non traitable (validation métier)

**Exemple** :
```json
{
  "error": "UnprocessableEntity",
  "message": "Cannot delete role: 5 users have this role"
}
```

### 500 Internal Server Error
Erreur serveur interne

**Exemple** :
```json
{
  "error": "InternalServerError",
  "message": "An unexpected error occurred"
}
```

---

## Authentification JWT

**Format** : Bearer Token

**Headers** :
```
Authorization: Bearer <access_token>
```

**Access Token** :
- Durée de vie : 15 minutes
- Claims : `user_id`, `username`, `roles`, `permissions`
- Format : JWT (HS256)

**Refresh Token** :
- Durée de vie : 7 jours
- Usage : Rafraîchir access token
- Stockage : Base de données ou cookie httpOnly

**Exemple Token** :
```json
{
  "user_id": 1,
  "username": "operator",
  "roles": ["Operator"],
  "permissions": {
    "releases": ["READ", "WRITE"],
    "rules": ["READ", "WRITE"]
  },
  "exp": 1730457600
}
```

---

## Rate Limiting

**Limites** :
- Endpoints publics : 10 requêtes/minute
- Endpoints authentifiés : 100 requêtes/minute
- Endpoints admin : 200 requêtes/minute

**Headers de Réponse** :
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1730457600
```

---

## Versioning

**Format** : `/api/v1/...` (futur)

**Version actuelle** : v1 (implicite)

**Déprication** : Notification via header `Deprecation: true`

---

## Pagination

**Format Standard** :
- `page` : Numéro page (défaut: 1)
- `per_page` : Items par page (défaut: 20, max: 100)

**Réponse** :
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8
  }
}
```

---

## Filtrage et Recherche

**Recherche Textuelle** :
- Paramètre `search` : Recherche dans champs textuels
- Support wildcards : `*` (optionnel)

**Filtres Multiples** :
- Paramètres répétés : `?type=EBOOK&type=TV`
- Ou paramètres séparés par virgule : `?type=EBOOK,TV`

**Tri** :
- Paramètre `sort` : Champ de tri
- Paramètre `order` : `asc` ou `desc`

---

## WebSockets (Futur)

**Endpoints** :
- `ws://localhost:5000/ws/jobs/{job_id}` : Logs job temps réel
- `ws://localhost:5000/ws/notifications` : Notifications utilisateur

**Format Messages** :
```json
{
  "type": "job_log",
  "job_id": 124,
  "data": {
    "timestamp": "2025-11-01T10:05:00Z",
    "level": "INFO",
    "message": "Packaging in progress..."
  }
}
```

---

## Liens

- [PRDs](../PRDs/)
- [Database ERD](../DATABASE_ERD.md)
- [DEVBOOK](../DEVBOOK.md)
- [CDC](../cdc.md)
- [OpenAPI YAML](../api/openapi.yaml) - Spécification OpenAPI 3.0.3 pour documentation interactive Swagger UI/Redoc

---

**Dernière mise à jour** : 2025-11-01  
**Version API** : 1.0.0

