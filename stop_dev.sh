#!/bin/bash
# Script d'arrêt de Flask

cd "$(dirname "$0")"

echo "🛑 Arrêt des processus Flask..."

# Arrêter les processus Flask (méthode douce puis forcée)
pkill -f "flask run" 2>/dev/null
sleep 1

# Si toujours actifs, forcer l'arrêt
PIDS=$(pgrep -f "flask run" 2>/dev/null)
if [ -n "$PIDS" ]; then
    echo "⚠️  Forçage de l'arrêt des processus..."
    kill -9 $PIDS 2>/dev/null
fi

echo "✅ Processus Flask arrêtés" || echo "ℹ️  Aucun processus Flask trouvé"

# Arrêter les conteneurs Docker du projet
docker stop ebook_scene_packer_backend ebook_scene_packer_db 2>/dev/null && echo "✅ Conteneurs Docker arrêtés" || echo "ℹ️  Aucun conteneur à arrêter"

echo "✅ Arrêt terminé"

