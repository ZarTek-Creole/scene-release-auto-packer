#!/bin/bash
# Script de démarrage Flask en mode développement

cd "$(dirname "$0")"

# Activer l'environnement virtuel
source venv/bin/activate

# Variables d'environnement
export FLASK_ENV=development
export FLASK_APP=wsgi.py
export FLASK_DEBUG=1

# Arrêter les conteneurs Docker backend si nécessaire (mais garder MySQL)
docker stop ebook_scene_packer_backend 2>/dev/null || true

# Démarrer MySQL si nécessaire
if ! docker ps | grep -q ebook_scene_packer_db; then
    echo "🔧 Démarrage de MySQL..."
    docker start ebook_scene_packer_db 2>/dev/null || docker compose up -d db 2>/dev/null || true
    echo "⏳ Attente du démarrage de MySQL..."
    sleep 5
    # Attendre que MySQL soit prêt
    for i in {1..30}; do
        if docker exec ebook_scene_packer_db mysqladmin ping -h localhost 2>/dev/null | grep -q "mysqld is alive"; then
            echo "✅ MySQL prêt"
            break
        fi
        sleep 1
    done
fi

# Vérifier si le port 5000 est utilisé et arrêter les processus Flask
if lsof -i :5000 >/dev/null 2>&1 || ss -tulpn 2>/dev/null | grep -q ":5000"; then
    echo "⚠️  Port 5000 déjà utilisé. Arrêt des processus Flask existants..."
    pkill -f "flask run" 2>/dev/null
    pkill -f "gunicorn.*5000" 2>/dev/null
    sleep 2
    # Forcer l'arrêt si nécessaire
    PIDS=$(pgrep -f "flask run" 2>/dev/null)
    if [ -n "$PIDS" ]; then
        kill -9 $PIDS 2>/dev/null
        sleep 1
    fi
    # Vérifier à nouveau
    if lsof -i :5000 >/dev/null 2>&1; then
        echo "❌ Impossible de libérer le port 5000. Utilisation du port 5001..."
        PORT=5001
    else
        PORT=5000
    fi
else
    PORT=5000
fi

# Démarrer Flask en mode développement
echo "🚀 Démarrage de l'application Flask en mode développement..."
echo "📡 URL: http://localhost:$PORT"
echo "🔍 Mode debug: activé"
echo ""
echo "Endpoints disponibles:"
echo "  - Health: http://localhost:$PORT/api/health"
echo "  - API: http://localhost:$PORT/api/"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter"
echo ""

flask run --host=0.0.0.0 --port=$PORT --debug --no-reload

