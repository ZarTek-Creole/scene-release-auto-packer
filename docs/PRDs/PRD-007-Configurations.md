# PRD-007 : Configurations

**ID** : PRD-007  
**Version** : 1.0.0  
**Date** : 2025-11-01  
**Statut** : Draft  
**Auteur** : Dev Team

---

## Vue d'Ensemble

Interface de configuration centralisée permettant la gestion des paramètres système, des APIs externes, des destinations FTP/SSH, des templates NFO et des préférences globales, avec chiffrement sécurisé des credentials.

**Priorité MoSCoW** : Must Have

**Phase** : Phase 7 (après Rôles)

---

## User Stories

### US-007-001 : Paramètres Système
**En tant que** administrateur  
**Je veux** configurer les paramètres système  
**Afin de** personnaliser l'environnement

**Critères d'acceptation** :
- Configuration chemins de base (uploads, releases, cache)
- Configuration limites (taille fichiers, timeouts)
- Configuration logs (niveau, rotation)
- Sauvegarde paramètres
- Validation avant sauvegarde

### US-007-002 : Configuration APIs Externes
**En tant que** administrateur  
**Je veux** configurer les clés API externes  
**Afin de** activer l'enrichissement automatique

**Critères d'acceptation** :
- Configuration clés API : OpenLibrary, Google Books, OMDb, TVDB, TMDb
- Chiffrement clés API (Fernet)
- Test connexion pour chaque API
- Activation/désactivation par API
- Affichage statut API (configurée, active, erreur)

### US-007-003 : Configuration Destinations FTP/SSH
**En tant que** administrateur  
**Je veux** configurer les destinations FTP/SSH  
**Afin de** définir où uploader les releases

**Critères d'acceptation** :
- Création/modification/suppression destinations
- Champs : Nom, host, port, user, password (chiffré)
- Test connexion avant sauvegarde
- Configuration paramètres (passive mode, timeout, etc.)
- Chiffrement mots de passe (Fernet)

### US-007-004 : Configuration Templates
**En tant que** administrateur  
**Je veux** configurer le stockage des templates  
**Afin de** choisir entre disque ou base de données

**Critères d'acceptation** :
- Choix stockage : Disque ou base de données
- Configuration chemin templates (si disque)
- Migration templates (disque ↔ DB)
- Validation templates existants

### US-007-005 : Test Connexion API
**En tant que** administrateur  
**Je veux** tester la connexion à une API  
**Afin de** vérifier que la configuration est correcte

**Critères d'acceptation** :
- Bouton "Tester" sur chaque API configurée
- Appel API de test
- Affichage résultat (succès/échec + message)
- Détails erreur si échec

### US-007-006 : Test Connexion FTP/SSH
**En tant que** administrateur  
**Je veux** tester la connexion FTP/SSH  
**Afin de** vérifier que les credentials sont corrects

**Critères d'acceptation** :
- Bouton "Tester" sur chaque destination
- Test connexion avec credentials
- Affichage résultat (succès/échec + message)
- Détails erreur si échec (timeout, credentials, etc.)

### US-007-007 : Gestion Préférences Utilisateur
**En tant que** utilisateur  
**Je veux** configurer mes préférences personnelles  
**Afin de** personnaliser mon expérience

**Critères d'acceptation** :
- Préférences par utilisateur (table `preferences`)
- Configuration : Ordre priorité APIs, préférences wizard, etc.
- Sauvegarde préférences
- Restauration valeurs par défaut

---

## Détails Fonctionnels

### Interface Configuration

**Layout** :
- Onglets ou sections :
  1. Paramètres Système
  2. APIs Externes
  3. Destinations FTP/SSH
  4. Templates
  5. Préférences Utilisateur

**Navigation** :
- Menu latéral ou tabs
- Indicateur modifications non sauvegardées
- Bouton "Sauvegarder" global ou par section

### Paramètres Système

**Chemins de Base** :
- **Uploads** : Chemin répertoire uploads fichiers
- **Releases** : Chemin répertoire releases packagées
- **Cache** : Chemin répertoire cache (rules, etc.)
- **Logs** : Chemin répertoire logs

**Limites** :
- **Taille fichier max** : 20GB (défaut)
- **Timeout API** : 30s (défaut)
- **Timeout FTP** : 60s (défaut)
- **Taille upload max** : 20GB

**Logs** :
- **Niveau** : DEBUG, INFO, WARNING, ERROR (sélecteur)
- **Rotation** : Taille max fichier log, nombre fichiers conservés
- **Format** : JSON, TEXT

**Validation** :
- Vérification chemins existants/créables
- Validation limites (nombres positifs)
- Messages erreur clairs

### Configuration APIs Externes

**APIs Disponibles** :
- **OpenLibrary** : Clé API (optionnelle)
- **Google Books** : Clé API (recommandée)
- **OMDb** : Clé API (pour TV)
- **TVDB** : Clé API + token (pour TV)
- **TMDb** : Clé API (pour TV)
- Autres APIs selon besoins

**Interface** :
- Card ou section par API
- Champs : Nom API, Clé API (masquée, bouton "Afficher/Masquer")
- Checkbox "Activer" pour chaque API
- Bouton "Tester" pour connexion
- Affichage statut : Configurée, Active, Erreur

**Sécurité** :
- Chiffrement clés API avec Fernet
- Stockage chiffré en base (`api_configs`)
- Déchiffrement uniquement pour usage
- Masquage clés dans UI (****)

**Test Connexion** :
- Appel API de test (ex: recherche simple)
- Affichage résultat : Succès/Échec + message
- Détails erreur si échec
- Timeout configuré

**Ordre Priorité** :
- Configuration ordre priorité APIs (pour enrichissement étape 6 wizard)
- Drag & drop ou liste ordonnée
- Sauvegarde ordre par utilisateur (préférences)

### Configuration Destinations FTP/SSH

**Interface Liste** :
- Liste destinations configurées
- Informations : Nom, host, port, user, statut
- Actions : Éditer, Supprimer, Tester

**Création/Modification Destination** :
- Formulaire avec champs :
  - **Nom** : Nom descriptif
  - **Host** : Adresse serveur
  - **Port** : Port (défaut : 21 FTP, 22 SSH)
  - **User** : Nom d'utilisateur
  - **Password** : Mot de passe (masqué)
  - **Type** : FTP, SFTP, SSH
  - **Options** : Passive mode, timeout, etc.

**Sécurité** :
- Chiffrement mots de passe avec Fernet
- Stockage chiffré en base (`destinations`)
- Masquage password dans UI (****)

**Test Connexion** :
- Bouton "Tester" visible
- Test connexion avec credentials
- Affichage résultat : Succès/Échec + message
- Détails erreur si échec (timeout, credentials, etc.)

**Validation** :
- Host non vide
- Port valide (1-65535)
- User non vide
- Password non vide
- Test connexion obligatoire avant sauvegarde

### Configuration Templates

**Stockage Templates** :
- **Option 1** : Disque (fichiers `.nfo` ou `.template`)
- **Option 2** : Base de données (table `templates`)
- Sélecteur choix stockage

**Si Disque** :
- Configuration chemin répertoire templates
- Validation chemin existant/créable
- Scan templates existants

**Si Base de Données** :
- Liste templates en base
- CRUD templates via interface

**Migration** :
- Option migration templates (disque ↔ DB)
- Processus guidé
- Vérification avant migration

**Validation** :
- Validation format templates
- Détection templates invalides
- Rapport validation

### Préférences Utilisateur

**Préférences Disponibles** :
- Ordre priorité APIs (pour enrichissement)
- Préférences wizard (valeurs par défaut)
- Filtres sauvegardés (Liste Releases, Rules)
- Préférences affichage (vue liste/cards, etc.)

**Interface** :
- Formulaire par catégorie préférence
- Sauvegarde automatique ou manuelle
- Restauration valeurs par défaut

**Stockage** :
- Table `preferences` (user_id, key, value)
- Fallback valeurs globales si préférence non définie

---

## Contraintes Techniques

### Frontend

**Technologies** :
- React 18+ avec TypeScript
- React Router v6
- Bootstrap 5
- Formik ou React Hook Form pour formulaires

**Composants** :
- `ConfigTabs` : Navigation onglets configuration
- `SystemSettings` : Paramètres système
- `ApiConfig` : Configuration APIs externes
- `DestinationConfig` : Configuration destinations FTP/SSH
- `TemplateConfig` : Configuration templates
- `UserPreferences` : Préférences utilisateur

**Performance** :
- Chargement configuration : < 1s
- Test connexion : < 5s (selon API/FTP)

### Backend

**Endpoints API** :
- `GET /api/config/system` : Récupération paramètres système
- `PUT /api/config/system` : Mise à jour paramètres système
- `GET /api/config/apis` : Liste APIs configurées
- `POST /api/config/apis` : Création configuration API
- `PUT /api/config/apis/:id` : Modification configuration API
- `DELETE /api/config/apis/:id` : Suppression configuration API
- `POST /api/config/apis/:id/test` : Test connexion API
- `GET /api/config/destinations` : Liste destinations FTP/SSH
- `POST /api/config/destinations` : Création destination
- `PUT /api/config/destinations/:id` : Modification destination
- `DELETE /api/config/destinations/:id` : Suppression destination
- `POST /api/config/destinations/:id/test` : Test connexion FTP/SSH
- `GET /api/config/templates` : Configuration stockage templates
- `PUT /api/config/templates` : Mise à jour configuration templates
- `POST /api/config/templates/migrate` : Migration templates (disque ↔ DB)
- `GET /api/config/preferences` : Préférences utilisateur
- `PUT /api/config/preferences` : Mise à jour préférences utilisateur

**Sécurité** :
- Chiffrement Fernet pour :
  - Clés API (`api_configs.api_key_encrypted`)
  - Mots de passe FTP/SSH (`destinations.password_encrypted`)
- Clé de chiffrement stockée dans variables d'environnement
- Déchiffrement uniquement pour usage (pas stockage mémoire long terme)

**Base de Données** :
- Table `api_configs` : id, name, api_key_encrypted, active, user_id, created_at
- Table `destinations` : id, name, host, port, user, password_encrypted, type, options_json, user_id, created_at
- Table `preferences` : id, user_id, key, value, created_at, updated_at
- Table globale `system_settings` : key, value (paramètres système)

**Permissions** :
- Endpoints protégés admin uniquement
- Préférences utilisateur : Accès propre compte uniquement

**Performance** :
- Temps réponse configuration : < 200ms
- Test connexion API : < 5s (selon API)
- Test connexion FTP/SSH : < 10s (selon connexion)

---

## Tests (TDD)

### Tests Unitaires Frontend

```typescript
describe('SystemSettings', () => {
  it('should validate paths exist', () => {
    // Test validation chemins
  });
});

describe('ApiConfig', () => {
  it('should mask API keys in UI', () => {
    // Test masquage clés API
  });
  
  it('should test API connection', () => {
    // Test connexion API
  });
});

describe('DestinationConfig', () => {
  it('should test FTP connection', () => {
    // Test connexion FTP
  });
});
```

### Tests Backend

```python
def test_system_settings():
    """Test configuration paramètres système."""
    # Test sauvegarde/chargement paramètres

def test_api_config_encryption():
    """Test chiffrement clés API."""
    # Test chiffrement/déchiffrement Fernet

def test_destination_ftp_test():
    """Test connexion FTP."""
    # Test connexion FTP avec credentials

def test_template_storage_config():
    """Test configuration stockage templates."""
    # Test choix disque/DB et migration
```

### Tests E2E (Playwright MCP)

```python
def test_configuration_e2e():
    """Test configuration E2E avec Playwright MCP."""
    mcp_playwright_browser_navigate(url="http://localhost:5000/config")
    
    # Configurer API
    mcp_playwright_browser_click(element="APIs tab")
    mcp_playwright_browser_type(element="Google Books API key", text="test-key")
    mcp_playwright_browser_click(element="test API button")
    mcp_playwright_browser_wait_for(text="Connection successful")
    
    # Configurer destination FTP
    mcp_playwright_browser_click(element="Destinations tab")
    mcp_playwright_browser_click(element="create destination button")
    mcp_playwright_browser_type(element="host", text="ftp.example.com")
    mcp_playwright_browser_type(element="user", text="ftpuser")
    mcp_playwright_browser_type(element="password", text="ftppass")
    mcp_playwright_browser_click(element="test connection button")
    mcp_playwright_browser_wait_for(text="Connection successful")
```

---

## Critères de Réussite

### Fonctionnels
- ✅ Paramètres système configurables
- ✅ Configuration APIs externes avec chiffrement
- ✅ Configuration destinations FTP/SSH avec chiffrement
- ✅ Test connexion API fonctionnel
- ✅ Test connexion FTP/SSH fonctionnel
- ✅ Configuration stockage templates fonctionnelle
- ✅ Préférences utilisateur fonctionnelles

### Sécurité
- ✅ Chiffrement clés API (Fernet)
- ✅ Chiffrement mots de passe FTP/SSH (Fernet)
- ✅ Masquage credentials dans UI
- ✅ Validation strict inputs

### Performance
- Chargement configuration : < 1s
- Test connexion : < 10s

### Qualité
- Accessibilité WCAG 2.2 AA
- Responsive design
- Tests couverture 100%

---

## Dépendances

- **Phase 1** : Infrastructure Core (JWT, DB, Models, Crypto)
- **PRD-002** : Nouvelle Release Wizard (utilisation APIs et destinations)
- **PRD-006** : Rôles (permissions admin)

---

**Liens** :
- [Backlog Agile](../BACKLOG_AGILE.md)
- [Test Plan](../TEST_PLAN.md)
- [DEVBOOK](../DEVBOOK.md)
- [CDC](../cdc.md)

