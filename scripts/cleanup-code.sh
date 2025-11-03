#!/bin/bash
# scripts/cleanup-code.sh
# Nettoyage automatique du code (imports non utilisés, code mort, etc.)

set -euo pipefail

echo "🧹 Nettoyage du code - eBook Scene Packer v2"
echo "============================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

CLEANED=0

# 1. Nettoyage Python
if [ -d "web" ] || [ -d "src" ]; then
    echo "1. Nettoyage Python..."
    echo "---------------------"
    
    # Vérifier si ruff est disponible
    if command -v ruff &> /dev/null; then
        echo "  → Suppression imports non utilisés..."
        ruff check --select F401 --fix web/ src/ 2>/dev/null && echo -e "${GREEN}    ✅ Imports nettoyés${NC}" || echo -e "${YELLOW}    ⚠️  Ruff non configuré ou pas d'erreurs${NC}"
        CLEANED=$((CLEANED + 1))
    else
        echo -e "${YELLOW}  ⚠️  Ruff non installé (optionnel)${NC}"
    fi
    
    # Détecter code mort (vulture)
    if command -v vulture &> /dev/null; then
        echo "  → Détection code mort..."
        DEAD_CODE=$(vulture web/ src/ --min-confidence 80 2>/dev/null || true)
        if [ -n "$DEAD_CODE" ]; then
            echo -e "${YELLOW}    ⚠️  Code mort potentiel détecté:${NC}"
            echo "$DEAD_CODE" | head -5
            echo "    → Vérifier manuellement avant suppression"
        else
            echo -e "${GREEN}    ✅ Aucun code mort détecté${NC}"
        fi
    else
        echo -e "${YELLOW}  ⚠️  Vulture non installé (optionnel)${NC}"
    fi
    echo ""
fi

# 2. Nettoyage TypeScript/JavaScript
if [ -d "frontend" ] || [ -d "web/static" ]; then
    echo "2. Nettoyage TypeScript/JavaScript..."
    echo "-----------------------------------"
    
    FRONTEND_DIR=""
    [ -d "frontend" ] && FRONTEND_DIR="frontend"
    [ -d "web/static" ] && FRONTEND_DIR="web/static"
    
    if [ -n "$FRONTEND_DIR" ]; then
        # Supprimer console.log (basique)
        echo "  → Recherche console.log de debug..."
        CONSOLE_LOGS=$(grep -r "console\.log" "$FRONTEND_DIR" --include="*.{ts,tsx,js,jsx}" 2>/dev/null | grep -v "node_modules\|dist" || true)
        if [ -n "$CONSOLE_LOGS" ]; then
            echo -e "${YELLOW}    ⚠️  Console.log trouvés (à supprimer manuellement):${NC}"
            echo "$CONSOLE_LOGS" | head -5
        else
            echo -e "${GREEN}    ✅ Aucun console.log trouvé${NC}"
        fi
        CLEANED=$((CLEANED + 1))
    fi
    echo ""
fi

# 3. Détection TODOs/FIXMEs
echo "3. Détection TODOs/FIXMEs..."
echo "----------------------------"
TODOS=$(grep -r "TODO\|FIXME" web/ src/ frontend/ 2>/dev/null --include="*.{py,ts,tsx,js,jsx}" | grep -v "node_modules\|venv\|__pycache__" || true)
if [ -n "$TODOS" ]; then
    COUNT=$(echo "$TODOS" | wc -l)
    echo -e "${YELLOW}  ⚠️  $COUNT TODO(s)/FIXME(s) trouvé(s):${NC}"
    echo "$TODOS" | head -10
    echo "  → Vérifier si pertinents ou à documenter avec issue/ticket"
else
    echo -e "${GREEN}  ✅ Aucun TODO/FIXME trouvé${NC}"
fi
echo ""

# 4. Résumé
echo "============================================="
echo "📊 Résumé du nettoyage"
echo "============================================="
echo -e "${GREEN}✅ Nettoyage terminé${NC}"
echo "Actions effectuées: $CLEANED"
echo ""
echo "⚠️  Note: Certaines actions nécessitent vérification manuelle"
echo ""

