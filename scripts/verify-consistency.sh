#!/bin/bash
# scripts/verify-consistency.sh
# Vérification de cohérence entre documentation et code

set -euo pipefail

echo "✅ Vérification de cohérence - Documentation ↔ Code"
echo "===================================================="
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0

# 1. Vérifier DEVBOOK ↔ Code
if [ -f "docs/DEVBOOK.md" ]; then
    echo "1. Vérification DEVBOOK ↔ Code..."
    echo "--------------------------------"
    
    # Vérifier Phase 1.1 (Setup Flask App Factory)
    if grep -q "Étape 1.1.*✅ Terminée\|Phase 1.*✅ Terminée" docs/DEVBOOK.md 2>/dev/null; then
        if [ ! -f "web/app.py" ]; then
            echo -e "${RED}❌ Incohérence: Phase 1.1 marquée terminée mais web/app.py n'existe pas${NC}"
            ERRORS=$((ERRORS + 1))
        else
            echo -e "${GREEN}  ✅ Phase 1.1: Code présent${NC}"
        fi
    fi
    
    # Vérifier autres phases selon besoin
    # (À étendre au fur et à mesure)
    echo ""
fi

# 2. Vérifier PRDs ↔ Fonctionnalités
echo "2. Vérification PRDs ↔ Fonctionnalités..."
echo "------------------------------------------"
if [ -d "docs/PRDs" ]; then
    # Vérifier PRD-002 (Wizard) → code wizard
    if [ -f "docs/PRDs/PRD-002-Nouvelle-Release.md" ]; then
        if grep -q "Statut.*Draft\|En cours" docs/PRDs/PRD-002-Nouvelle-Release.md 2>/dev/null; then
            # PRD en cours → code peut ne pas exister encore (OK)
            echo -e "${GREEN}  ✅ PRD-002: En cours (code peut ne pas exister)${NC}"
        elif grep -q "Statut.*Approved\|Terminée" docs/PRDs/PRD-002-Nouvelle-Release.md 2>/dev/null; then
            # PRD approuvé → code doit exister ou être en cours
            if [ ! -f "web/blueprints/wizard.py" ] && [ ! -d "frontend/src/components/wizard" ]; then
                echo -e "${YELLOW}  ⚠️  PRD-002 approuvé mais code wizard non trouvé (à vérifier)${NC}"
            else
                echo -e "${GREEN}  ✅ PRD-002: Code présent${NC}"
            fi
        fi
    fi
    echo ""
fi

# 3. Vérifier todolist ↔ DEVBOOK
echo "3. Vérification todolist ↔ DEVBOOK..."
echo "--------------------------------------"
if [ -f "docs/todolist.md" ] && [ -f "docs/DEVBOOK.md" ]; then
    # Extraire étapes terminées de DEVBOOK
    DEVBOOK_COMPLETED=$(grep -o "Étape.*✅ Terminée" docs/DEVBOOK.md 2>/dev/null || true)
    
    if [ -n "$DEVBOOK_COMPLETED" ]; then
        echo "$DEVBOOK_COMPLETED" | while read -r step; do
            STEP_ID=$(echo "$step" | grep -o "Étape [0-9]\.[0-9]" | head -1)
            if ! grep -q "$STEP_ID.*✅\|$STEP_ID.*terminée" docs/todolist.md 2>/dev/null; then
                echo -e "${YELLOW}  ⚠️  $STEP_ID terminée dans DEVBOOK mais pas dans todolist${NC}"
            fi
        done
    else
        echo -e "${GREEN}  ✅ Aucune étape terminée à vérifier${NC}"
    fi
    echo ""
fi

# 4. Résumé
echo "===================================================="
echo "📊 Résumé de la vérification"
echo "===================================================="
if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}❌ Erreurs de cohérence: $ERRORS${NC}"
    echo -e "${RED}🚨 Action requise!${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Cohérence vérifiée${NC}"
    exit 0
fi

