#!/bin/bash

echo "Création d'un utilisateur de test admin..."

docker compose exec -T backend flask shell <<EOF
from web.models import User, Role, db

# Créer rôle admin si n'existe pas
admin_role = Role.query.filter_by(name='admin').first()
if not admin_role:
    admin_role = Role(name='admin', description='Administrator')
    db.session.add(admin_role)
    db.session.commit()
    print("✅ Rôle admin créé")

# Créer utilisateur admin si n'existe pas
admin_user = User.query.filter_by(username='admin').first()
if not admin_user:
    admin_user = User(username='admin', email='admin@test.com', active=True)
    admin_user.set_password('admin123')
    admin_user.roles.append(admin_role)
    db.session.add(admin_user)
    db.session.commit()
    print("✅ Utilisateur admin créé (username: admin, password: admin123)")
else:
    print("ℹ️  Utilisateur admin existe déjà")
    # Réinitialiser le mot de passe
    admin_user.set_password('admin123')
    admin_user.active = True
    db.session.commit()
    print("✅ Mot de passe réinitialisé: admin123")
EOF

echo ""
echo "Utilisateur de test créé :"
echo "  Username: admin"
echo "  Password: admin123"

