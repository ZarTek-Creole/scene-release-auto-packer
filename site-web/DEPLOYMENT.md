# Guide de Déploiement - Site Web Next.js

Ce guide détaille les différentes méthodes de déploiement pour le site web Next.js.

## 🚀 Méthodes de Déploiement

### 1. Vercel (Recommandé)

Vercel est la plateforme recommandée pour déployer Next.js, offrant des performances optimales et une intégration native.

#### Prérequis

1. Créer un compte Vercel : https://vercel.com
2. Installer Vercel CLI :
   ```bash
   npm install -g vercel
   ```

#### Déploiement Automatique via GitHub

1. Connecter le repository GitHub à Vercel
2. Configurer les variables d'environnement dans Vercel Dashboard :
   - `NEXT_PUBLIC_SITE_URL` : URL de production
   - `NEXT_PUBLIC_GA_ID` : (optionnel) Google Analytics ID
   - `NEXT_PUBLIC_SENTRY_DSN` : (optionnel) Sentry DSN

3. Vercel déploiera automatiquement à chaque push sur `main`

#### Déploiement Manuel via CLI

```bash
cd site-web
vercel login
vercel --prod
```

#### Configuration Vercel

Le fichier `vercel.json` configure automatiquement :
- Headers de sécurité
- Routes et rewrites
- Configuration framework Next.js

### 2. Docker

#### Prérequis

- Docker 20.10+
- Docker Compose 2.0+

#### Build et Lancement

```bash
cd site-web

# Build l'image Docker
docker build -t ebook-scene-packer-site-web .

# Lancer avec Docker Compose
docker-compose up -d
```

Le site sera accessible sur `http://localhost:3000`

#### Variables d'Environnement Docker

Créer un fichier `.env.local` :

```bash
NEXT_PUBLIC_SITE_URL=http://localhost:3000
NODE_ENV=production
```

#### Health Check

Docker Compose inclut un health check automatique qui vérifie la disponibilité du site toutes les 30 secondes.

### 3. Déploiement Self-Hosted (Node.js)

#### Prérequis

- Node.js 20+
- npm ou yarn

#### Build et Lancement

```bash
cd site-web

# Installer dépendances
npm ci

# Build production
npm run build

# Lancer serveur production
npm start
```

Le site sera accessible sur `http://localhost:3000`

#### Utiliser PM2 pour Production

```bash
# Installer PM2
npm install -g pm2

# Lancer avec PM2
pm2 start npm --name "site-web" -- start

# Sauvegarder configuration PM2
pm2 save
pm2 startup
```

### 4. Docker Compose avec Nginx (Production)

Pour un déploiement production avec Nginx en reverse proxy :

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  site-web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ebook-scene-packer-site-web
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_SITE_URL=https://yourdomain.com
    restart: unless-stopped
    networks:
      - site-web-network

  nginx:
    image: nginx:alpine
    container_name: site-web-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - site-web
    restart: unless-stopped
    networks:
      - site-web-network

networks:
  site-web-network:
    driver: bridge
```

## 🔧 Configuration

### Variables d'Environnement

| Variable | Description | Requis | Exemple |
|----------|-------------|--------|---------|
| `NEXT_PUBLIC_SITE_URL` | URL publique du site | ✅ | `https://ebook-scene-packer.example.com` |
| `NEXT_PUBLIC_GA_ID` | Google Analytics ID | ❌ | `G-XXXXXXXXXX` |
| `NEXT_PUBLIC_SENTRY_DSN` | Sentry DSN | ❌ | `https://xxx@sentry.io/xxx` |
| `NODE_ENV` | Environnement | ✅ | `production` |

### Fichiers de Configuration

- `vercel.json` : Configuration Vercel
- `Dockerfile` : Configuration Docker
- `docker-compose.yml` : Configuration Docker Compose
- `.env.example` : Exemple de variables d'environnement

## 🧪 Tests avant Déploiement

### Tests Locaux

```bash
cd site-web

# Tests unitaires
npm run test

# Tests avec coverage
npm run test:coverage

# Tests d'accessibilité
npm run test:a11y

# Lint et format
npm run lint
npm run format:check

# Build de vérification
npm run build
```

### Tests CI/CD

Les tests sont exécutés automatiquement via GitHub Actions :
- Lint et format check
- TypeScript type check
- Tests unitaires
- Build production

## 📊 Monitoring

### Vercel Analytics

Vercel fournit des analytics intégrés si activés dans le dashboard.

### Health Check Endpoint

Pour Docker, un health check est configuré dans `docker-compose.yml`.

## 🔒 Sécurité

### Headers de Sécurité

Les headers de sécurité sont configurés automatiquement dans :
- `next.config.js` (headers HTTP)
- `vercel.json` (headers Vercel)

### Secrets

⚠️ **JAMAIS** commiter les fichiers `.env.local` ou `.env` avec des secrets.

Utiliser les variables d'environnement de la plateforme de déploiement.

## 🚨 Troubleshooting

### Erreur de Build

```bash
# Nettoyer le cache Next.js
rm -rf .next node_modules package-lock.json
npm install
npm run build
```

### Erreur Docker

```bash
# Rebuild sans cache
docker build --no-cache -t ebook-scene-packer-site-web .

# Vérifier les logs
docker-compose logs site-web
```

### Erreur Vercel

Vérifier les logs dans Vercel Dashboard → Deployments → Logs

## 📚 Ressources

- [Documentation Next.js Deployment](https://nextjs.org/docs/app/building-your-application/deploying)
- [Documentation Vercel](https://vercel.com/docs)
- [Documentation Docker](https://docs.docker.com/)

