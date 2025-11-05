#!/usr/bin/env python3
"""Test complet de toutes les fonctionnalités avec authentification.

Ce script teste toutes les fonctionnalités de l'application avec un utilisateur authentifié
et génère un rapport complet avec preuves visuelles.
"""

from __future__ import annotations

import json
import sys
from typing import Any

import requests

BASE_URL = "http://localhost:5001"
TEST_USERNAME = "admin"
TEST_PASSWORD = "admin123"

# Résultats
results = {
    "authenticated": False,
    "token": None,
    "tests": [],
    "screenshots": [],
}


def print_header(title: str) -> None:
    """Affiche un en-tête."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def test_api_call(
    method: str,
    endpoint: str,
    description: str,
    expected_status: int,
    data: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[bool, dict[str, Any]]:
    """Teste un appel API."""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            return (False, {"error": f"Méthode {method} non supportée"})
        
        success = response.status_code == expected_status
        result = {
            "success": success,
            "status_code": response.status_code,
            "expected": expected_status,
            "description": description,
            "endpoint": endpoint,
            "method": method,
        }
        
        try:
            result["response"] = response.json()
        except:
            result["response"] = response.text[:200]
        
        return (success, result)
    except Exception as e:
        return (False, {"error": str(e), "description": description, "endpoint": endpoint})


def main() -> int:
    """Fonction principale."""
    print_header("Test Complet de Toutes les Fonctionnalités")
    
    passed = 0
    failed = 0
    
    # Phase 1: Authentification
    print_header("PHASE 1 : Authentification")
    
    login_data = {"username": TEST_USERNAME, "password": TEST_PASSWORD}
    success, result = test_api_call("POST", "/api/auth/login", "Connexion utilisateur", 200, login_data)
    results["tests"].append(result)
    
    if success and "access_token" in result.get("response", {}):
        token = result["response"]["access_token"]
        results["token"] = token
        results["authenticated"] = True
        headers = {"Authorization": f"Bearer {token}"}
        print(f"✅ Connexion réussie")
        print(f"   Token obtenu: {token[:20]}...")
        passed += 1
    else:
        print(f"❌ Échec de connexion")
        print(f"   Réponse: {result.get('response', 'N/A')}")
        failed += 1
        print("\n⚠️  Impossible de continuer sans authentification")
        return 1
    
    # Phase 2: Test des Endpoints API avec authentification
    print_header("PHASE 2 : Endpoints API (Authentifiés)")
    
    api_tests = [
        ("GET", "/api/auth/me", "Informations utilisateur actuel", 200),
        ("GET", "/api/dashboard/stats", "Statistiques dashboard", 200),
        ("GET", "/api/releases", "Liste des releases", 200),
        ("GET", "/api/rules", "Liste des rules", 200),
        ("GET", "/api/users", "Liste des utilisateurs", 200),
        ("GET", "/api/roles", "Liste des rôles", 200),
        ("GET", "/api/jobs", "Liste des jobs", 200),
    ]
    
    for method, endpoint, description, expected in api_tests:
        success, result = test_api_call(method, endpoint, description, expected, headers=headers)
        results["tests"].append(result)
        
        if success:
            print(f"✅ {description}")
            if "response" in result and isinstance(result["response"], dict):
                # Afficher quelques données si disponibles
                data = result["response"]
                if "users" in data:
                    print(f"   Utilisateurs trouvés: {len(data['users'])}")
                elif "releases" in data:
                    print(f"   Releases trouvées: {len(data['releases'])}")
                elif "rules" in data:
                    print(f"   Rules trouvées: {len(data['rules'])}")
                elif "roles" in data:
                    print(f"   Rôles trouvés: {len(data['roles'])}")
                elif "jobs" in data:
                    print(f"   Jobs trouvés: {len(data['jobs'])}")
                elif "stats" in data:
                    print(f"   Statistiques disponibles")
            passed += 1
        else:
            print(f"❌ {description}")
            print(f"   HTTP {result.get('status_code', 'N/A')} (attendu {expected})")
            failed += 1
    
    # Phase 3: Test des Fonctionnalités CRUD
    print_header("PHASE 3 : Fonctionnalités CRUD")
    
    # Test création rule (si possible)
    rule_data = {
        "name": "TEST_RULE_E2E",
        "description": "Rule de test E2E",
        "content": "Test rule content",
        "category": "EBOOK",
    }
    success, result = test_api_call("POST", "/api/rules", "Création d'une rule", 201, rule_data, headers)
    results["tests"].append(result)
    
    if success:
        print(f"✅ Création d'une rule réussie")
        rule_id = result.get("response", {}).get("rule", {}).get("id")
        if rule_id:
            # Test suppression
            success2, result2 = test_api_call("DELETE", f"/api/rules/{rule_id}", "Suppression d'une rule", 200, headers=headers)
            results["tests"].append(result2)
            if success2:
                print(f"✅ Suppression d'une rule réussie")
                passed += 2
            else:
                print(f"❌ Suppression d'une rule échouée")
                failed += 1
        passed += 1
    else:
        print(f"❌ Création d'une rule échouée")
        print(f"   {result.get('response', 'N/A')}")
        failed += 1
    
    # Résumé
    print_header("Résumé Final")
    print(f"Tests passés   : {passed}")
    print(f"Tests échoués  : {failed}")
    print(f"Total          : {passed + failed}")
    print(f"Taux de réussite: {(passed / (passed + failed) * 100):.1f}%" if (passed + failed) > 0 else "N/A")
    
    # Sauvegarder les résultats
    with open("test-results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n📄 Résultats sauvegardés dans: test-results.json")
    
    if failed == 0:
        print("\n✅ Toutes les fonctionnalités testées fonctionnent correctement !")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) ont échoué")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

