#!/bin/bash

echo "🔍 Validation Complète de l'Application - eBook Scene Packer v2"
echo "=================================================================="
echo ""

BASE_URL="http://localhost:5001"
FRONTEND_URL="http://localhost:8082"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
TOTAL=0

test_endpoint() {
    local method=$1
    local endpoint=$2
    local expected_status=$3
    local description=$4
    local data=$5
    
    TOTAL=$((TOTAL + 1))
    
    if [ -z "$data" ]; then
        if [ "$method" = "GET" ]; then
            response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint" 2>&1)
        else
            response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint" 2>&1)
        fi
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" -H "Content-Type: application/json" -d "$data" "$BASE_URL$endpoint" 2>&1)
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "$expected_status" ]; then
        echo -e "${GREEN}✅ PASS${NC}: $description (HTTP $http_code)"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}: $description (Expected HTTP $expected_status, got $http_code)"
        echo "   Response: $body"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo "📊 PHASE 1 : Vérification des Services"
echo "----------------------------------------"

# Test 1: Health Check
echo ""
echo "1. Health Check Backend..."
test_endpoint "GET" "/api/health" "200" "Health check backend"

# Test 2: Database connection (via health)
echo ""
echo "2. Vérification Base de Données..."
if curl -s "$BASE_URL/api/health" | grep -q "healthy"; then
    echo -e "${GREEN}✅ PASS${NC}: Base de données accessible"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}❌ FAIL${NC}: Base de données non accessible"
    FAILED=$((FAILED + 1))
fi
TOTAL=$((TOTAL + 1))

echo ""
echo "📊 PHASE 2 : Test des Endpoints API (sans authentification)"
echo "------------------------------------------------------------"

# Test 3: Endpoints qui devraient retourner 401 (non authentifié)
echo ""
echo "3. Tests de sécurité (401 attendu pour endpoints protégés)..."

test_endpoint "GET" "/api/releases" "401" "Liste releases (401 - non authentifié)"
test_endpoint "GET" "/api/rules" "401" "Liste rules (401 - non authentifié)"
test_endpoint "GET" "/api/users" "401" "Liste users (401 - non authentifié)"
test_endpoint "GET" "/api/roles" "401" "Liste roles (401 - non authentifié)"
test_endpoint "GET" "/api/configurations" "401" "Liste configurations (401 - non authentifié)"
test_endpoint "GET" "/api/dashboard/stats" "401" "Dashboard stats (401 - non authentifié)"

echo ""
echo "📊 PHASE 3 : Test des Endpoints Publics"
echo "----------------------------------------"

# Test 4: Endpoints publics (si existent)
test_endpoint "GET" "/api/auth/login" "405" "Login endpoint existe (405 Method Not Allowed pour GET)" || true
test_endpoint "POST" "/api/auth/login" "400" "Login endpoint (400 - données manquantes)"

echo ""
echo "📊 PHASE 4 : Test de l'Interface Frontend"
echo "------------------------------------------"

# Test 5: Frontend accessible
echo ""
echo "5. Vérification Frontend..."
if curl -s "$FRONTEND_URL" > /dev/null 2>&1; then
    http_code=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL")
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ PASS${NC}: Frontend accessible (HTTP $http_code)"
        PASSED=$((PASSED + 1))
        
        # Vérifier que c'est bien du HTML React
        if curl -s "$FRONTEND_URL" | grep -q "root\|React\|<!DOCTYPE"; then
            echo -e "${GREEN}✅ PASS${NC}: Frontend contient du HTML valide"
            PASSED=$((PASSED + 1))
        else
            echo -e "${YELLOW}⚠️  WARN${NC}: Frontend réponse inattendue"
        fi
        TOTAL=$((TOTAL + 1))
    else
        echo -e "${RED}❌ FAIL${NC}: Frontend retourne HTTP $http_code"
        FAILED=$((FAILED + 1))
    fi
    TOTAL=$((TOTAL + 1))
else
    echo -e "${YELLOW}⚠️  WARN${NC}: Frontend non accessible (service non démarré ou port différent)"
    echo "   Frontend devrait être sur $FRONTEND_URL"
    echo "   Vérifiez: docker compose ps"
fi

echo ""
echo "📊 PHASE 5 : Résumé des Tests"
echo "------------------------------"
echo ""
echo "Tests passés   : $PASSED"
echo "Tests échoués  : $FAILED"
echo "Total          : $TOTAL"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ Tous les tests sont passés !${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Certains tests ont échoué${NC}"
    exit 1
fi

