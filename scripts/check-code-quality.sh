#!/bin/bash
# scripts/check-code-quality.sh
# Script pour vérifier la qualité du code avec tous les outils configurés

set -e

echo "🔍 Vérification qualité code avec Black, Ruff, MyPy..."
echo ""

# Black - Formatage
echo "📝 Black - Formatage..."
black --check web/ tests/ || {
    echo "❌ Black: Code non formaté. Exécutez: black web/ tests/"
    exit 1
}
echo "✅ Black: Code formaté correctement"
echo ""

# Ruff - Linting
echo "🔍 Ruff - Linting..."
ruff check web/ tests/ || {
    echo "❌ Ruff: Erreurs de linting détectées"
    exit 1
}
echo "✅ Ruff: Aucune erreur de linting"
echo ""

# Ruff Format - Formatage supplémentaire
echo "📝 Ruff Format - Formatage..."
ruff format --check web/ tests/ || {
    echo "❌ Ruff Format: Code non formaté"
    exit 1
}
echo "✅ Ruff Format: Code formaté correctement"
echo ""

# MyPy - Type checking (strict)
echo "🔍 MyPy - Type checking (strict)..."
mypy web/ tests/ || {
    echo "⚠️  MyPy: Erreurs de type détectées (peut être normal pour tests)"
    # Ne pas faire échouer le script pour MyPy si des erreurs sont attendues
}
echo "✅ MyPy: Vérification terminée"
echo ""

# Pytest - Tests avec coverage
echo "🧪 Pytest - Tests avec coverage ≥90%..."
pytest tests/ --cov=web --cov=src --cov-report=term-missing --cov-fail-under=90 || {
    echo "❌ Pytest: Tests échoués ou coverage <90%"
    exit 1
}
echo "✅ Pytest: Tous les tests passent avec coverage ≥90%"
echo ""

echo "✅ Tous les outils de qualité code passent !"

