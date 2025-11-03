#!/bin/bash
# scripts/audit-documentation.sh
# Audit de la documentation pour détecter fichiers obsolètes, liens brisés, etc.

set -euo pipefail

echo "🔍 Audit de la documentation - eBook Scene Packer v2"
echo "=================================================="
echo ""

# Couleurs pour output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# 1. Vérifier sections "À compléter" ou "TODO"
echo "1. Vérification des sections incomplètes..."
echo "-------------------------------------------"
INCOMPLETE=$(grep -r "À compléter\|TODO\|FIXME" docs/ --include="*.md" 2>/dev/null | grep -v "node_modules\|venv" || true)
if [ -n "$INCOMPLETE" ]; then
    echo -e "${YELLOW}⚠️  Sections incomplètes trouvées:${NC}"
    echo "$INCOMPLETE" | while read -r line; do
        echo "  - $line"
    done
    WARNINGS=$((WARNINGS + $(echo "$INCOMPLETE" | wc -l)))
else
    echo -e "${GREEN}✅ Aucune section incomplète${NC}"
fi
echo ""

# 2. Détecter PRDs obsolètes (statut "Deprecated")
echo "2. Vérification des PRDs obsolètes..."
echo "-------------------------------------"
# Chercher seulement les PRDs avec "Statut.*Deprecated" (pas README qui mentionne deprecated dans texte)
DEPRECATED_PRD=$(find docs/PRDs/ -name "PRD-*.md" -exec grep -l "^\\*\\*Statut\\*\\*.*Deprecated\|Statut.*Deprecated" {} \; 2>/dev/null || true)
if [ -n "$DEPRECATED_PRD" ]; then
    echo -e "${YELLOW}⚠️  PRDs deprecated trouvés:${NC}"
    echo "$DEPRECATED_PRD" | while read -r file; do
        # Vérifier date de dernière modification
        LAST_MOD=$(stat -c %y "$file" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
        echo "  - $file (dernière mod: $LAST_MOD)"
        echo "    → À supprimer ou archiver si > 1 mois"
    done
    WARNINGS=$((WARNINGS + $(echo "$DEPRECATED_PRD" | wc -l)))
else
    echo -e "${GREEN}✅ Aucun PRD deprecated${NC}"
fi
echo ""

# 3. Vérifier fichiers de documentation très anciens (> 6 mois)
echo "3. Vérification des fichiers très anciens (> 6 mois)..."
echo "-------------------------------------------------------"
OLD_FILES=$(find docs/ -name "*.md" -type f -mtime +180 2>/dev/null | grep -v "node_modules\|venv\|archive" || true)
if [ -n "$OLD_FILES" ]; then
    echo -e "${YELLOW}⚠️  Fichiers anciens trouvés (à vérifier):${NC}"
    echo "$OLD_FILES" | while read -r file; do
        LAST_MOD=$(stat -c %y "$file" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
        # Vérifier si fichier référencé comme actif
        if grep -q "Statut.*En cours\|⏳\|🟡" "$file" 2>/dev/null; then
            echo -e "${RED}  ❌ $file (modifié: $LAST_MOD) - Marqué actif mais très ancien!${NC}"
            ERRORS=$((ERRORS + 1))
        else
            echo "  - $file (modifié: $LAST_MOD) - À vérifier si toujours pertinent"
            WARNINGS=$((WARNINGS + 1))
        fi
    done
else
    echo -e "${GREEN}✅ Aucun fichier très ancien${NC}"
fi
echo ""

# 4. Vérifier cohérence DEVBOOK ↔ Code (basique)
echo "4. Vérification de cohérence DEVBOOK ↔ Code (basique)..."
echo "---------------------------------------------------------"
if [ -f "docs/DEVBOOK.md" ]; then
    # Vérifier si Phase 1.1 terminée mais web/app.py n'existe pas
    if grep -q "Phase 1.*✅ Terminée\|Étape 1.1.*✅ Terminée" docs/DEVBOOK.md 2>/dev/null; then
        if [ ! -f "web/app.py" ]; then
            echo -e "${RED}❌ Incohérence: Phase 1 marquée terminée mais web/app.py n'existe pas${NC}"
            ERRORS=$((ERRORS + 1))
        else
            echo -e "${GREEN}✅ Cohérence Phase 1 vérifiée${NC}"
        fi
    fi
else
    echo -e "${YELLOW}⚠️  DEVBOOK.md non trouvé${NC}"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# 5. Vérifier liens relatifs (basique - recherche de patterns)
echo "5. Vérification des liens Markdown (patterns)..."
echo "------------------------------------------------"
# Rechercher liens relatifs potentiellement brisés
LINK_FILES=$(find docs/ -name "*.md" -type f 2>/dev/null | grep -v "node_modules\|venv\|archive" || true)
BROKEN_LINKS=0
for file in $LINK_FILES; do
    # Extraire liens relatifs du fichier
    LINKS=$(grep -oE '\[.*\]\((\.\/|\.\.\/)[^)]+\)' "$file" 2>/dev/null || true)
    if [ -n "$LINKS" ]; then
        echo "$LINKS" | while read -r link; do
            # Extraire le chemin du lien
            LINK_PATH=$(echo "$link" | sed -n 's/.*(\(.*\))/\1/p')
            # Résoudre le chemin relatif
            LINK_DIR=$(dirname "$file")
            ABS_LINK_PATH=$(realpath -m "$LINK_DIR/$LINK_PATH" 2>/dev/null || echo "")
            if [ -n "$ABS_LINK_PATH" ] && [ ! -f "$ABS_LINK_PATH" ] && [ ! -d "$ABS_LINK_PATH" ]; then
                echo -e "${YELLOW}  ⚠️  Lien potentiellement brisé dans $file: $link${NC}"
                BROKEN_LINKS=$((BROKEN_LINKS + 1))
            fi
        done
    fi
done
if [ "$BROKEN_LINKS" -eq 0 ]; then
    echo -e "${GREEN}✅ Aucun lien brisé détecté (vérification basique)${NC}"
else
    WARNINGS=$((WARNINGS + BROKEN_LINKS))
fi
echo ""

# 6. Résumé
echo "=================================================="
echo "📊 Résumé de l'audit"
echo "=================================================="
echo -e "${GREEN}✅ Vérifications terminées${NC}"
echo -e "${RED}❌ Erreurs: $ERRORS${NC}"
echo -e "${YELLOW}⚠️  Avertissements: $WARNINGS${NC}"
echo ""

if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}🚨 Des erreurs critiques ont été détectées. Action requise!${NC}"
    exit 1
elif [ "$WARNINGS" -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Des avertissements ont été détectés. Vérification recommandée.${NC}"
    exit 0
else
    echo -e "${GREEN}✨ Documentation propre! Aucun problème détecté.${NC}"
    exit 0
fi

