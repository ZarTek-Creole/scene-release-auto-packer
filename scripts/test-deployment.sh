#!/bin/bash
# Script de test du déploiement - eBook Scene Packer v2

set -e

echo "🧪 Test de Déploiement - eBook Scene Packer v2"
echo "================================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher un succès
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Fonction pour afficher une erreur
error() {
    echo -e "${RED}❌ $1${NC}"
}

# Fonction pour afficher un avertissement
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Vérifier Docker
echo "1. Vérification de Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    success "Docker installé: $DOCKER_VERSION"
else
    error "Docker n'est pas installé"
    exit 1
fi

# Vérifier Docker Compose
echo ""
echo "2. Vérification de Docker Compose..."
if docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version)
    success "Docker Compose installé: $COMPOSE_VERSION"
    COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    success "Docker Compose installé: $COMPOSE_VERSION"
    COMPOSE_CMD="docker-compose"
else
    error "Docker Compose n'est pas installé"
    echo "   Installez Docker Compose ou utilisez 'docker compose' (v2)"
    exit 1
fi

# Vérifier fichiers nécessaires
echo ""
echo "3. Vérification des fichiers nécessaires..."

FILES=(
    "docker-compose.yml"
    "Dockerfile"
    "frontend/Dockerfile"
    "web/app.py"
    "frontend/package.json"
    "nginx/nginx.conf"
)

ALL_FILES_OK=true
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        success "Fichier trouvé: $file"
    else
        error "Fichier manquant: $file"
        ALL_FILES_OK=false
    fi
done

if [ "$ALL_FILES_OK" = false ]; then
    error "Certains fichiers sont manquants"
    exit 1
fi

# Vérifier .env
echo ""
echo "4. Vérification du fichier .env..."
if [ -f ".env" ]; then
    success "Fichier .env trouvé"
else
    warning "Fichier .env non trouvé"
    if [ -f ".env.example" ]; then
        echo "   Copiez .env.example vers .env et configurez-le"
        echo "   cp .env.example .env"
    else
        error "Fichier .env.example non trouvé"
    fi
fi

# Vérifier structure frontend
echo ""
echo "5. Vérification de la structure frontend..."
if [ -d "frontend/src" ]; then
    success "Dossier frontend/src existe"
else
    error "Dossier frontend/src manquant"
    exit 1
fi

if [ -f "frontend/package.json" ]; then
    success "frontend/package.json existe"
else
    error "frontend/package.json manquant"
    exit 1
fi

# Vérifier health check endpoint
echo ""
echo "6. Vérification du health check endpoint..."
if grep -q "/health" web/blueprints/health.py 2>/dev/null || grep -q "/api/health" web/app.py 2>/dev/null; then
    success "Health check endpoint trouvé"
else
    warning "Health check endpoint non trouvé (peut être dans un blueprint)"
fi

# Test de build Docker (optionnel)
echo ""
echo "7. Test de build Docker (optionnel)..."
read -p "Voulez-vous tester le build des images Docker? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "   Construction de l'image backend..."
    if docker build -t ebook-scene-packer-backend-test -f Dockerfile .; then
        success "Build backend réussi"
    else
        error "Build backend échoué"
        exit 1
    fi
    
    echo "   Construction de l'image frontend..."
    if docker build -t ebook-scene-packer-frontend-test -f frontend/Dockerfile .; then
        success "Build frontend réussi"
    else
        error "Build frontend échoué"
        exit 1
    fi
    
    # Nettoyer les images de test
    echo "   Nettoyage des images de test..."
    docker rmi ebook-scene-packer-backend-test ebook-scene-packer-frontend-test 2>/dev/null || true
fi

# Instructions pour démarrer
echo ""
echo "================================================"
echo "📋 Instructions pour démarrer le déploiement:"
echo ""
echo "1. Créez le fichier .env (si non présent):"
echo "   cp .env.example .env"
echo ""
echo "2. Configurez les variables dans .env"
echo ""
echo "3. Démarrez les services:"
echo "   $COMPOSE_CMD up -d --build"
echo ""
echo "4. Vérifiez les logs:"
echo "   $COMPOSE_CMD logs -f"
echo ""
echo "5. Vérifiez le statut:"
echo "   $COMPOSE_CMD ps"
echo ""
echo "6. Initialisez la base de données:"
echo "   $COMPOSE_CMD exec backend flask db upgrade"
echo ""
echo "7. Accédez à l'application:"
echo "   Frontend: http://localhost:80"
echo "   Backend API: http://localhost:5000"
echo "   Nginx: http://localhost:8080"
echo ""
echo "8. Arrêtez les services:"
echo "   $COMPOSE_CMD down"
echo ""

success "✅ Validation terminée avec succès!"
echo ""
echo "Pour plus de détails, voir:"
echo "  - docs/DEPLOYMENT_PLAN.md"
echo "  - docs/DEPLOYMENT.md"

