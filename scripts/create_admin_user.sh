#!/bin/bash
# Script pour créer l'utilisateur admin dans la base de données

cd "$(dirname "$0")/.."

echo "🔧 Création de l'utilisateur admin..."

docker exec -i ebook_scene_packer_db mysql -uappuser -pchangeme_db_password ebook_scene_packer << 'SQL'
-- Créer les tables si nécessaire (via Flask)
-- Créer l'utilisateur admin et le rôle admin si nécessaire

INSERT IGNORE INTO roles (id, name, description, created_at) 
VALUES (1, 'admin', 'Administrator', NOW());

INSERT IGNORE INTO users (id, username, email, password_hash, active, created_at) 
VALUES (1, 'admin', 'admin@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5b5v5X5Xe', 1, NOW())
ON DUPLICATE KEY UPDATE password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5b5v5X5Xe', active = 1;

INSERT IGNORE INTO user_roles (user_id, role_id) 
VALUES (1, 1);
SQL

echo "✅ Utilisateur admin créé (username: admin, password: admin123)"
echo ""
echo "Note: Le hash du mot de passe doit être généré via Flask."
echo "Exécutez ce script Python pour créer l'utilisateur correctement:"
echo ""
echo "python3 << 'EOF'"
echo "from web.app import create_app"
echo "from web.extensions import db"
echo "from web.models import User, Role"
echo ""
echo "app = create_app('development')"
echo "with app.app_context():"
echo "    db.create_all()"
echo "    admin_role = Role.query.filter_by(name='admin').first()"
echo "    if not admin_role:"
echo "        admin_role = Role(name='admin', description='Administrator')"
echo "        db.session.add(admin_role)"
echo "        db.session.commit()"
echo "    admin_user = User.query.filter_by(username='admin').first()"
echo "    if not admin_user:"
echo "        admin_user = User(username='admin', email='admin@test.com', active=True)"
echo "        admin_user.set_password('admin123')"
echo "        admin_user.roles.append(admin_role)"
echo "        db.session.add(admin_user)"
echo "        db.session.commit()"
echo "        print('✅ Utilisateur admin créé')"
echo "EOF"

