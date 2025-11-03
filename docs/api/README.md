# 📡 API Documentation - OpenAPI/Swagger

**Date** : 2025-11-01  
**Version** : 1.0.0

---

## 📄 Fichiers Disponibles

- **`openapi.yaml`** : Spécification OpenAPI 3.0.3 (YAML) - **2 585 lignes**
- **`API_REFERENCE.md`** : Documentation texte complète (référence)

---

## 🚀 Utilisation

### Visualiser la Documentation Interactive

#### Option 1 : Swagger UI (Recommandé)

1. **Installer Swagger UI** :
```bash
npm install -g swagger-ui-serve
# OU
docker run -p 8080:8080 -e SWAGGER_JSON=/api/openapi.yaml -v $(pwd)/docs/api:/api swaggerapi/swagger-ui
```

2. **Servir la documentation** :
```bash
# Depuis le répertoire docs/api/
swagger-ui-serve openapi.yaml
# OU via Docker
docker run -p 8080:8080 \
  -e SWAGGER_JSON=/api/openapi.yaml \
  -v $(pwd)/docs/api:/api \
  swaggerapi/swagger-ui
```

3. **Accéder** : http://localhost:8080

#### Option 2 : Redoc

1. **Installer Redoc** :
```bash
npm install -g redoc-cli
```

2. **Servir la documentation** :
```bash
redoc-cli serve docs/api/openapi.yaml
```

3. **Accéder** : http://localhost:8080

#### Option 3 : Swagger Editor (En ligne)

1. Aller sur https://editor.swagger.io/
2. Coller le contenu de `openapi.yaml`
3. Documentation interactive disponible

---

## 🔧 Génération Code

### Client API (TypeScript/JavaScript)

**Avec openapi-generator** :
```bash
# Installer openapi-generator
npm install -g @openapitools/openapi-generator-cli

# Générer client TypeScript
openapi-generator-cli generate \
  -i docs/api/openapi.yaml \
  -g typescript-axios \
  -o frontend/src/api/generated

# Générer client JavaScript
openapi-generator-cli generate \
  -i docs/api/openapi.yaml \
  -g javascript \
  -o frontend/src/api/generated
```

### Client API (Python)

```bash
# Générer client Python
openapi-generator-cli generate \
  -i docs/api/openapi.yaml \
  -g python \
  -o python-client
```

---

## ✅ Validation

### Valider le Fichier OpenAPI

**Avec Swagger Validator** :
```bash
# En ligne
curl -X POST "https://validator.swagger.io/validator/debug" \
  -H "Content-Type: application/yaml" \
  --data-binary @docs/api/openapi.yaml
```

**Avec redoc-cli** :
```bash
redoc-cli lint docs/api/openapi.yaml
```

---

## 📊 Statistiques

- **Endpoints documentés** : ~64
- **Schémas définis** : 6 (User, Release, Job, Rule, Role, Error, Pagination)
- **Tags** : 8 (Authentication, Dashboard, Wizard, Releases, Rules, Users, Roles, Configurations)
- **Format** : OpenAPI 3.0.3

---

## 🔄 Mise à Jour

**Quand mettre à jour** :
1. Nouvel endpoint ajouté
2. Modification endpoint existant
3. Ajout/modification schéma
4. Changement authentification

**Processus** :
1. Modifier `openapi.yaml`
2. Valider avec `redoc-cli lint`
3. Tester dans Swagger UI
4. Mettre à jour `API_REFERENCE.md` si nécessaire
5. Générer nouveau client si nécessaire

---

## 🔗 Liens

- **API Reference** : [API_REFERENCE.md](../API_REFERENCE.md)
- **PRDs** : [PRDs](../PRDs/)
- **Database ERD** : [DATABASE_ERD.md](../DATABASE_ERD.md)
- **DEVBOOK** : [DEVBOOK.md](../DEVBOOK.md)

---

## 📝 Notes

- **Authentification** : Tous endpoints (sauf `/auth/login`) requièrent JWT Bearer Token
- **Permissions** : Vérification READ/WRITE/MOD/DELETE selon ressource
- **Rate Limiting** : Limites documentées dans `API_REFERENCE.md`
- **Versioning** : Format `/api/v1/...` (futur)

---

**Dernière mise à jour** : 2025-11-01

