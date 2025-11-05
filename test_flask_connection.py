#!/usr/bin/env python3
"""Test rapide de connexion Flask et MySQL."""

import sys
from pathlib import Path

# Ajouter le projet au path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from web.app import create_app
from web.extensions import db

print("🔍 Test de connexion Flask et MySQL...")
print()

app = create_app('development')

with app.app_context():
    try:
        print("✅ Application Flask créée")
        print(f"✅ Configuration: {app.config.get('SQLALCHEMY_DATABASE_URI', 'N/A')[:50]}...")
        
        # Test de connexion simple
        print("\n🔍 Test de connexion à la base de données...")
        result = db.session.execute(db.text("SELECT 1")).scalar()
        print(f"✅ Connexion MySQL réussie: {result}")
        
        # Test de la route health
        print("\n🔍 Test de la route /api/health...")
        with app.test_client() as client:
            response = client.get('/api/health')
            print(f"✅ Health check: {response.status_code} - {response.get_json()}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

print("\n✅ Tous les tests réussis !")

