# 🚀 Deployment Plan - eBook Scene Packer v2

**Date de création** : 2025-11-01  
**Version** : 1.0.0

---

## 🎯 Objectif

Plan complet pour déployer l'application v2 en production avec sécurité, monitoring et rollback.

---

## 📋 Pré-requis

### Infrastructure
- **Serveur** : Linux (Ubuntu 22.04+ recommandé)
- **RAM** : Minimum 4GB, recommandé 8GB+
- **CPU** : Minimum 2 cores, recommandé 4+
- **Storage** : 50GB+ (releases, logs)

### Logiciels
- **Python** : 3.11+
- **MySQL** : 8.0+
- **Nginx** : 1.20+ (reverse proxy)
- **Docker** : 20.10+ (optionnel, recommandé)
- **Certbot** : Pour SSL (optionnel mais recommandé)

### Comptes/Services
- **MySQL** : Base de données configurée
- **Domain** : Nom de domaine configuré (optionnel)
- **Note** : Service de notifications externe pour alertes système (Slack/Discord/PagerDuty) - optionnel, non utilisé dans l'application pour les utilisateurs

---

## 🔧 Configuration Production

### Variables d'Environnement

```bash
# .env.production
FLASK_ENV=production
SECRET_KEY=<generate_secure_key>
JWT_SECRET_KEY=<generate_secure_key>
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379/0

# Security
BCRYPT_LOG_ROUNDS=12
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=86400

# Uploads
MAX_UPLOAD_SIZE=1073741824  # 1GB
UPLOAD_FOLDER=/var/www/uploads
RELEASES_FOLDER=/var/www/releases

# APIs
OPENLIBRARY_API_KEY=<key>
GOOGLE_BOOKS_API_KEY=<key>
OMDB_API_KEY=<key>
TVDB_API_KEY=<key>
TMDB_API_KEY=<key>

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/app/app.log
```

### Génération Secrets
```bash
# Générer SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Générer JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📦 Déploiement Docker (Recommandé)

### Étape 1 : Préparation

```bash
# Cloner repository
git clone <repo-url>
cd ebook.scene.packer

# Vérifier branch
git checkout v2

# Créer .env.production
cp .env.example .env.production
# Éditer .env.production avec valeurs production
```

### Étape 2 : Build Images

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Vérifier images
docker images
```

### Étape 3 : Initialisation Base de Données

```bash
# Lancer MySQL seulement
docker-compose -f docker-compose.prod.yml up -d mysql

# Attendre MySQL prêt
sleep 30

# Initialiser DB
docker-compose -f docker-compose.prod.yml run --rm backend \
  flask db upgrade

# Créer utilisateur admin
docker-compose -f docker-compose.prod.yml run --rm backend \
  python scripts/seed_admin.py
```

### Étape 4 : Déploiement Application

```bash
# Démarrer tous services
docker-compose -f docker-compose.prod.yml up -d

# Vérifier santé
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Étape 5 : Configuration Nginx (Reverse Proxy)

```nginx
# /etc/nginx/sites-available/ebook-scene-packer

server {
    listen 80;
    server_name your-domain.com;

    # Redirection HTTPS (si SSL configuré)
    # return 301 https://$server_name$request_uri;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Activer site
sudo ln -s /etc/nginx/sites-available/ebook-scene-packer \
           /etc/nginx/sites-enabled/

# Tester configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### Étape 6 : SSL (Optionnel mais Recommandé)

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx

# Obtenir certificat
sudo certbot --nginx -d your-domain.com

# Auto-renewal configuré automatiquement
```

---

## 📦 Déploiement Manuel (Sans Docker)

### Étape 1 : Installation Dépendances

```bash
# Python venv
python3.11 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install -r requirements.txt
pip install gunicorn  # WSGI server
```

### Étape 2 : Configuration Application

```bash
# Créer .env.production
cp .env.example .env.production
# Éditer avec valeurs production

# Créer dossiers
mkdir -p /var/www/uploads
mkdir -p /var/www/releases
mkdir -p /var/log/app
```

### Étape 3 : Initialisation Base de Données

```bash
# Migrations
export FLASK_ENV=production
flask db upgrade

# Seed data
python scripts/seed_admin.py
```

### Étape 4 : Configuration Gunicorn

```bash
# Créer /etc/systemd/system/ebook-scene-packer.service

[Unit]
Description=eBook Scene Packer Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ebook-scene-packer
Environment="PATH=/var/www/ebook-scene-packer/venv/bin"
ExecStart=/var/www/ebook-scene-packer/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/var/www/ebook-scene-packer/app.sock \
    --access-logfile /var/log/app/access.log \
    --error-logfile /var/log/app/error.log \
    web.app:create_app()

[Install]
WantedBy=multi-user.target
```

```bash
# Activer service
sudo systemctl daemon-reload
sudo systemctl enable ebook-scene-packer
sudo systemctl start ebook-scene-packer
sudo systemctl status ebook-scene-packer
```

### Étape 5 : Configuration Nginx

```nginx
# /etc/nginx/sites-available/ebook-scene-packer

server {
    listen 80;
    server_name your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/ebook-scene-packer/app.sock;
    }

    # Static files (si nécessaire)
    location /static {
        alias /var/www/ebook-scene-packer/web/static;
    }
}
```

---

## ✅ Checklist Déploiement

### Avant Déploiement
- [ ] Tests passent (100% couverture)
- [ ] Documentation à jour
- [ ] Variables d'environnement configurées
- [ ] Secrets générés et sécurisés
- [ ] Base de données préparée
- [ ] Backups configurés

### Pendant Déploiement
- [ ] Images Docker buildées (si Docker)
- [ ] Base de données initialisée
- [ ] Migrations appliquées
- [ ] Services démarrés
- [ ] Nginx configuré
- [ ] SSL configuré (si applicable)

### Après Déploiement
- [ ] Health check passe
- [ ] Login fonctionne
- [ ] Dashboard s'affiche
- [ ] API endpoints répondent
- [ ] Logs vérifiés (pas d'erreurs)
- [ ] Monitoring actif
- [ ] Alertes configurées

---

## 🔄 Rollback

### Plan de Rollback

#### Si Déploiement Échoue
```bash
# Arrêter nouveaux services
docker-compose -f docker-compose.prod.yml down

# Restaurer backup base de données
mysql -u user -p dbname < backup.sql

# Restaurer code précédent
git checkout <previous-commit>
docker-compose -f docker-compose.prod.yml up -d
```

#### Rollback Code Seulement
```bash
# Revenir à version précédente
git checkout <previous-tag>

# Rebuild si nécessaire
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

#### Rollback Base de Données
```bash
# Restaurer backup
mysql -u user -p dbname < backup.sql

# Ou rollback migration
flask db downgrade -1
```

---

## 📊 Monitoring

### Health Checks
- **Endpoint** : `GET /health`
- **Fréquence** : Toutes les 30s
- **Alertes** : Si échec > 2 fois consécutives

### Logs
- **Emplacement** : `/var/log/app/`
- **Rotation** : Quotidienne, 30 jours rétention
- **Niveau** : INFO en production

### Métriques
- **CPU** : < 80%
- **RAM** : < 80%
- **Disk** : < 80%
- **Response Time** : < 2s p95

### Alertes
- **Notifications** : Erreurs critiques (Slack/Discord/PagerDuty)
- **Slack/Discord** : Warnings (optionnel)
- **PagerDuty** : Critical (optionnel)

---

## 🔒 Sécurité Production

### Checklist Sécurité
- [ ] HTTPS configuré (SSL/TLS)
- [ ] Secrets dans variables d'environnement (pas en code)
- [ ] Firewall configuré (ports 80, 443 seulement)
- [ ] MySQL accès restreint (localhost)
- [ ] Utilisateurs système séparés
- [ ] Permissions fichiers restrictives
- [ ] Logs sensibles masqués
- [ ] Rate limiting configuré
- [ ] CORS configuré correctement
- [ ] Headers sécurité (HSTS, X-Frame-Options, etc.)

---

## 📝 Post-Déploiement

### Actions Immédiates
1. Vérifier health check
2. Tester login/logout
3. Vérifier logs (pas d'erreurs)
4. Tester fonctionnalité critique (création release)
5. Notifier équipe déploiement réussi

### Actions Suivantes (24h)
1. Monitoring continu
2. Collecte feedback utilisateurs
3. Analyse logs erreurs
4. Performance check
5. Planifier optimisations si nécessaire

---

## 🔗 Liens

- **CDC** : `docs/cdc.md`
- **DEVBOOK** : `docs/DEVBOOK.md`
- **Test Plan** : `docs/TEST_PLAN.md`

---

**Dernière mise à jour** : 2025-11-01  
**Prochaine révision** : Avant Phase 9

