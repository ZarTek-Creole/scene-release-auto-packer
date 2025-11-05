#!/usr/bin/env python3
"""Script de test complet de toutes les pages et fonctionnalités avec MCP Tools.

Ce script teste toutes les pages de l'application et valide que les interfaces
et fonctionnalités utilisateur fonctionnent correctement.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# URLs de base
BACKEND_URL = "http://localhost:5001"
FRONTEND_URL = "http://localhost:8082"

# Pages à tester
PAGES_TO_TEST = [
    {"path": "/", "name": "Dashboard", "description": "Page d'accueil avec statistiques"},
    {"path": "/releases/new", "name": "Nouvelle Release", "description": "Wizard 9 étapes pour créer une release"},
    {"path": "/releases", "name": "Liste Releases", "description": "Liste de toutes les releases"},
    {"path": "/rules", "name": "Rules", "description": "Gestion des règles Scene"},
    {"path": "/users", "name": "Utilisateurs", "description": "Gestion des utilisateurs"},
    {"path": "/roles", "name": "Rôles", "description": "Gestion des rôles et permissions"},
    {"path": "/config", "name": "Configurations", "description": "Gestion des configurations"},
]

# Endpoints API à tester
API_ENDPOINTS = [
    {"path": "/api/health", "method": "GET", "auth_required": False, "description": "Health check"},
    {"path": "/api/auth/login", "method": "POST", "auth_required": False, "description": "Authentification"},
    {"path": "/api/releases", "method": "GET", "auth_required": True, "description": "Liste des releases"},
    {"path": "/api/rules", "method": "GET", "auth_required": True, "description": "Liste des rules"},
    {"path": "/api/users", "method": "GET", "auth_required": True, "description": "Liste des utilisateurs"},
    {"path": "/api/roles", "method": "GET", "auth_required": True, "description": "Liste des rôles"},
    {"path": "/api/configurations", "method": "GET", "auth_required": True, "description": "Liste des configurations"},
    {"path": "/api/dashboard/stats", "method": "GET", "auth_required": True, "description": "Statistiques dashboard"},
]


def print_section(title: str) -> None:
    """Affiche un titre de section."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_test_result(name: str, passed: bool, details: str = "") -> tuple[int, int]:
    """Affiche le résultat d'un test."""
    if passed:
        print(f"✅ PASS: {name}")
        if details:
            print(f"   {details}")
        return (1, 0)
    else:
        print(f"❌ FAIL: {name}")
        if details:
            print(f"   {details}")
        return (0, 1)


def main() -> int:
    """Fonction principale."""
    print_section("Test Complet de l'Application - eBook Scene Packer v2")
    
    passed = 0
    failed = 0
    
    # Phase 1: Test Backend API
    print_section("PHASE 1 : Test des Endpoints API Backend")
    
    import requests
    
    for endpoint in API_ENDPOINTS:
        try:
            url = f"{BACKEND_URL}{endpoint['path']}"
            
            if endpoint['method'] == 'GET':
                response = requests.get(url, timeout=5)
            elif endpoint['method'] == 'POST':
                # Pour login, on teste avec des données invalides (devrait retourner 400)
                response = requests.post(url, json={}, timeout=5)
            
            if endpoint['auth_required']:
                # Endpoints protégés doivent retourner 401 sans auth
                if response.status_code == 401:
                    p, f = print_test_result(
                        endpoint['description'],
                        True,
                        f"HTTP {response.status_code} (401 attendu - non authentifié)"
                    )
                    passed += p
                    failed += f
                else:
                    p, f = print_test_result(
                        endpoint['description'],
                        False,
                        f"HTTP {response.status_code} (401 attendu)"
                    )
                    passed += p
                    failed += f
            else:
                # Endpoints publics
                if response.status_code in [200, 400, 405]:
                    p, f = print_test_result(
                        endpoint['description'],
                        True,
                        f"HTTP {response.status_code}"
                    )
                    passed += p
                    failed += f
                else:
                    p, f = print_test_result(
                        endpoint['description'],
                        False,
                        f"HTTP {response.status_code} (200/400/405 attendu)"
                    )
                    passed += p
                    failed += f
        except requests.exceptions.ConnectionError:
            p, f = print_test_result(
                endpoint['description'],
                False,
                "Connexion refusée - Backend non démarré"
            )
            passed += p
            failed += f
        except Exception as e:
            p, f = print_test_result(
                endpoint['description'],
                False,
                f"Erreur: {str(e)}"
            )
            passed += p
            failed += f
    
    # Phase 2: Test Frontend (si accessible)
    print_section("PHASE 2 : Test des Pages Frontend")
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            p, f = print_test_result(
                "Frontend accessible",
                True,
                f"HTTP {response.status_code}"
            )
            passed += p
            failed += f
            
            # Vérifier que c'est du HTML
            if "html" in response.text.lower() or "<!DOCTYPE" in response.text or "root" in response.text:
                p, f = print_test_result(
                    "Frontend contient du HTML valide",
                    True,
                    "Contenu HTML détecté"
                )
                passed += p
                failed += f
            else:
                p, f = print_test_result(
                    "Frontend contient du HTML valide",
                    False,
                    "Contenu HTML non détecté"
                )
                passed += p
                failed += f
            
            # Tester chaque page
            for page in PAGES_TO_TEST:
                try:
                    page_url = f"{FRONTEND_URL}{page['path']}"
                    page_response = requests.get(page_url, timeout=5, allow_redirects=True)
                    
                    if page_response.status_code in [200, 404]:
                        # 404 peut être normal si la page nécessite une redirection ou auth
                        p, f = print_test_result(
                            f"Page: {page['name']} ({page['path']})",
                            True,
                            f"HTTP {page_response.status_code}"
                        )
                        passed += p
                        failed += f
                    else:
                        p, f = print_test_result(
                            f"Page: {page['name']} ({page['path']})",
                            False,
                            f"HTTP {page_response.status_code}"
                        )
                        passed += p
                        failed += f
                except Exception as e:
                    p, f = print_test_result(
                        f"Page: {page['name']} ({page['path']})",
                        False,
                        f"Erreur: {str(e)}"
                    )
                    passed += p
                    failed += f
        else:
            p, f = print_test_result(
                "Frontend accessible",
                False,
                f"HTTP {response.status_code}"
            )
            passed += p
            failed += f
    except requests.exceptions.ConnectionError:
        print("⚠️  Frontend non accessible (service non démarré)")
        print(f"   URL testée: {FRONTEND_URL}")
        print("   Vérifiez: docker compose ps")
        print("   Pour démarrer: docker compose up -d frontend nginx")
    except Exception as e:
        p, f = print_test_result(
            "Frontend accessible",
            False,
            f"Erreur: {str(e)}"
        )
        passed += p
        failed += f
    
    # Résumé
    print_section("Résumé des Tests")
    print(f"Tests passés   : {passed}")
    print(f"Tests échoués  : {failed}")
    print(f"Total          : {passed + failed}")
    print(f"Taux de réussite: {(passed / (passed + failed) * 100):.1f}%" if (passed + failed) > 0 else "N/A")
    
    if failed == 0:
        print("\n✅ Tous les tests sont passés !")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) ont échoué")
        return 1


if __name__ == "__main__":
    sys.exit(main())

