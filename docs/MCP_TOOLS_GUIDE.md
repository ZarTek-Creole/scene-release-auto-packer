# 🛠️ Guide MCP Tools - eBook Scene Packer v2

**Date de création** : 2025-11-01  
**Version** : 1.0.0

---

## 🎯 Vue d'Ensemble

Ce guide documente tous les **MCP (Model Context Protocol) Tools** disponibles pour le projet v2, leur utilisation et quand les utiliser.

Les MCP Tools sont des outils puissants permettant d'étendre les capacités de l'assistant IA pour analyser le code, tester l'application, rechercher de la documentation, etc.

---

## 📚 Catégories de MCP Tools

### 1. Repomix MCP - Analyse et Packaging Codebase

**Objectif** : Analyser et packager une base de code complète pour analyse AI.

#### Outils Disponibles

##### `mcp_repomix_pack_codebase`
Packager un répertoire local en un fichier consolidé pour analyse AI.

**Quand l'utiliser** :
- 📦 Analyse complète de la codebase
- 📊 Génération de métriques et statistiques
- 🔍 Recherche dans tout le code
- 📝 Génération de documentation automatique

**Paramètres** :
- `directory` : Répertoire à packager (chemin absolu)
- `style` : Format de sortie (xml, markdown, json, plain)
- `compress` : Compression Tree-sitter (optionnel)
- `includePatterns` : Patterns de fichiers à inclure
- `ignorePatterns` : Patterns de fichiers à exclure

**Exemple** :
```python
# Packager toute la codebase pour analyse
mcp_repomix_pack_codebase(
    directory="/home/deffice/projects/ebook.scene.packer",
    style="markdown",
    compress=False
)
```

##### `mcp_repomix_pack_remote_repository`
Packager un dépôt GitHub distant.

**Quand l'utiliser** :
- 📥 Analyser une dépendance externe
- 🔍 Comparer avec d'autres projets
- 📚 Analyser des exemples de code

**Exemple** :
```python
mcp_repomix_pack_remote_repository(
    remote="flask/flask",
    style="markdown"
)
```

##### `mcp_repomix_grep_repomix_output`
Rechercher des patterns dans un output Repomix.

**Quand l'utiliser** :
- 🔍 Recherche de code spécifique dans codebase packagé
- 📝 Analyse de patterns de code
- 🐛 Recherche de bugs potentiels

---

### 2. Docs MCP Server - Documentation Bibliothèques

**Objectif** : Scraper, indexer et rechercher la documentation de bibliothèques.

#### Outils Disponibles

##### `mcp_docs-mcp-server_scrape_docs`
Scraper et indexer la documentation d'une bibliothèque.

**Quand l'utiliser** :
- 📚 Indexer documentation React, Flask, Bootstrap, etc.
- 🔄 Mettre à jour documentation d'une nouvelle version
- 📖 Préparer documentation pour référence rapide

**Paramètres** :
- `url` : URL racine de la documentation
- `library` : Nom de la bibliothèque
- `version` : Version (optionnel)
- `maxPages` : Nombre max de pages (défaut 1000)
- `maxDepth` : Profondeur navigation (défaut 3)

**Exemple** :
```python
# Indexer documentation React
mcp_docs-mcp-server_scrape_docs(
    url="https://react.dev",
    library="react",
    version="18.0.0"
)
```

##### `mcp_docs-mcp-server_search_docs`
Rechercher dans la documentation indexée.

**Quand l'utiliser** :
- 🔍 Rechercher des exemples d'utilisation
- 📖 Trouver des patterns de code
- ❓ Résoudre des questions techniques

**Exemple** :
```python
# Rechercher documentation React Hooks
mcp_docs-mcp-server_search_docs(
    library="react",
    query="hooks lifecycle useEffect",
    limit=5
)
```

##### `mcp_docs-mcp-server_list_libraries`
Lister toutes les bibliothèques indexées.

**Quand l'utiliser** :
- 📋 Vérifier quelles bibliothèques sont disponibles
- ✅ Valider indexation documentation

---

### 3. Playwright Browser MCP - Tests E2E et Validation UI

**Objectif** : Automatiser le navigateur pour tests E2E et validation interface utilisateur.

#### Outils Disponibles

##### Navigation
- `mcp_playwright_browser_navigate` : Naviguer vers une URL
- `mcp_playwright_browser_navigate_back` : Retour page précédente
- `mcp_playwright_browser_wait_for` : Attendre texte/temps

**Quand utiliser** :
- 🧪 Tests E2E complets
- ✅ Validation fonctionnalités UI
- 🔍 Vérification flux utilisateur
- 📱 Tests responsive design

##### Interaction
- `mcp_playwright_browser_click` : Cliquer sur élément
- `mcp_playwright_browser_type` : Saisir texte
- `mcp_playwright_browser_fill_form` : Remplir formulaire
- `mcp_playwright_browser_select_option` : Sélectionner option

**Quand utiliser** :
- 📝 Tests formulaires
- 🖱️ Tests interactions utilisateur
- ✅ Validation workflow complet

##### Capture
- `mcp_playwright_browser_snapshot` : Capturer snapshot accessibilité
- `mcp_playwright_browser_take_screenshot` : Prendre screenshot

**Quand utiliser** :
- 📸 Documentation visuelle
- 🐛 Debug problèmes UI
- 📋 Validation accessibilité
- 📊 Reporting tests

##### Exemple Workflow Complet
```python
# Test login E2E
1. mcp_playwright_browser_navigate(url="http://localhost:5000")
2. mcp_playwright_browser_snapshot()  # Vérifier page chargée
3. mcp_playwright_browser_type(element="username input", text="admin")
4. mcp_playwright_browser_type(element="password input", text="password")
5. mcp_playwright_browser_click(element="login button")
6. mcp_playwright_browser_wait_for(text="Dashboard")
7. mcp_playwright_browser_snapshot()  # Valider dashboard
```

---

### 4. Context7 MCP - Documentation Bibliothèques Structurée

**Objectif** : Accéder à la documentation structurée de bibliothèques via Context7.

#### Outils Disponibles

##### `mcp_context7_resolve-library-id`
Résoudre un nom de package vers un ID Context7.

**Quand l'utiliser** :
- 🔍 Identifier bibliothèque à documenter
- ✅ Valider disponibilité documentation

##### `mcp_context7_get-library-docs`
Récupérer documentation d'une bibliothèque.

**Quand l'utiliser** :
- 📚 Documentation React, Flask, etc.
- 🔍 Recherche d'exemples de code
- ❓ Questions techniques spécifiques

**Exemple** :
```python
# Récupérer documentation Flask
mcp_context7_get-library-docs(
    context7CompatibleLibraryID="/pallets/flask",
    topic="blueprints",
    tokens=5000
)
```

---

### 5. Memory MCP - Knowledge Graph et Entités

**Objectif** : Créer et gérer un graphe de connaissances pour le projet.

#### Outils Disponibles

##### `mcp_memory_create_entities`
Créer des entités dans le graphe de connaissances.

**Quand l'utiliser** :
- 🧠 Modéliser architecture projet
- 📝 Documenter décisions techniques
- 🔗 Créer relations entre concepts

##### `mcp_memory_search_nodes`
Rechercher dans le graphe de connaissances.

**Quand l'utiliser** :
- 🔍 Recherche informations projet
- 📊 Analyse relations architecture
- 🧠 Requêtes sémantiques

**Exemple** :
```python
# Créer entités architecture
mcp_memory_create_entities(
    entities=[{
        "name": "Flask App Factory",
        "entityType": "Pattern",
        "observations": ["Used in web/app.py", "Enables testing"]
    }]
)
```

---

### 6. Sequential Thinking MCP - Résolution Problèmes Complexes

**Objectif** : Pensée séquentielle pour problèmes complexes.

#### Outils Disponibles

##### `mcp_sequential-thinking_sequentialthinking`
Pensée séquentielle dynamique et réflexive.

**Quand l'utiliser** :
- 🤔 Problèmes complexes multi-étapes
- 📋 Planification et design
- 🔍 Analyse approfondie
- 🎯 Décomposition problèmes

**Exemple** :
```python
# Analyser problème architecture
mcp_sequential-thinking_sequentialthinking(
    thought="Le wizard 9 étapes devient complexe à maintenir...",
    thoughtNumber=1,
    totalThoughts=5,
    nextThoughtNeeded=True
)
```

---

## 📋 Guide d'Utilisation par Scénario

### Scénario 1 : Analyse Codebase Complète

**Quand** : Début projet, refactoring majeur, audit code

**Tools à utiliser** :
1. `mcp_repomix_pack_codebase` - Packager codebase
2. `mcp_repomix_grep_repomix_output` - Rechercher patterns
3. `mcp_memory_create_entities` - Modéliser architecture

**Workflow** :
```python
# 1. Packager codebase
output = mcp_repomix_pack_codebase(
    directory="/home/deffice/projects/ebook.scene.packer",
    style="markdown"
)

# 2. Rechercher patterns spécifiques
mcp_repomix_grep_repomix_output(
    outputId=output.id,
    pattern="def.*test_",
    contextLines=5
)

# 3. Créer entités architecture
mcp_memory_create_entities(...)
```

---

### Scénario 2 : Recherche Documentation Bibliothèque

**Quand** : Implémentation nouvelle fonctionnalité, résolution problème technique

**Tools à utiliser** :
1. `mcp_docs-mcp-server_search_docs` - Rechercher documentation
2. `mcp_context7_get-library-docs` - Documentation structurée

**Workflow** :
```python
# 1. Rechercher documentation React
results = mcp_docs-mcp-server_search_docs(
    library="react",
    query="useState hook examples",
    limit=5
)

# 2. Si besoin, documentation plus détaillée
docs = mcp_context7_get-library-docs(
    context7CompatibleLibraryID="/facebook/react",
    topic="hooks"
)
```

---

### Scénario 3 : Tests E2E Complets

**Quand** : Validation fonctionnalités, tests régression, validation UI

**Tools à utiliser** :
1. `mcp_playwright_browser_navigate` - Navigation
2. `mcp_playwright_browser_snapshot` - Capture état
3. `mcp_playwright_browser_click/type` - Interactions
4. `mcp_playwright_browser_take_screenshot` - Documentation

**Workflow** :
```python
# 1. Naviguer vers application
mcp_playwright_browser_navigate(url="http://localhost:5000")

# 2. Capturer état initial
mcp_playwright_browser_snapshot()

# 3. Interagir avec interface
mcp_playwright_browser_type(element="input", text="value")
mcp_playwright_browser_click(element="button")

# 4. Valider résultat
mcp_playwright_browser_wait_for(text="Success")
mcp_playwright_browser_snapshot()

# 5. Screenshot pour documentation
mcp_playwright_browser_take_screenshot(filename="test-result.png")
```

---

### Scénario 4 : Résolution Problème Complexe

**Quand** : Bug complexe, décision architecture, optimisation

**Tools à utiliser** :
1. `mcp_sequential-thinking_sequentialthinking` - Pensée séquentielle
2. `mcp_repomix_pack_codebase` - Analyser code
3. `mcp_memory_search_nodes` - Rechercher connaissances

**Workflow** :
```python
# 1. Pensée séquentielle pour analyser problème
mcp_sequential-thinking_sequentialthinking(
    thought="Le problème est...",
    thoughtNumber=1,
    totalThoughts=5
)

# 2. Analyser code pertinent
mcp_repomix_grep_repomix_output(...)

# 3. Rechercher dans connaissances
mcp_memory_search_nodes(query="problem context")
```

---

## ✅ Checklist Utilisation MCP Tools

### Avant d'Utiliser un MCP Tool

- [ ] Identifier clairement l'objectif
- [ ] Vérifier que le tool est approprié pour la tâche
- [ ] Préparer paramètres nécessaires
- [ ] Vérifier pré-requis (serveur démarré, etc.)

### Pendant l'Utilisation

- [ ] Utiliser tool de manière isolée si possible
- [ ] Capturer résultats pour documentation
- [ ] Vérifier que résultats sont cohérents
- [ ] Documenter workflow si réutilisable

### Après Utilisation

- [ ] Analyser résultats
- [ ] Intégrer résultats dans code/documentation
- [ ] Mettre à jour mémoire (Memory MCP) si pertinent
- [ ] Documenter learnings

---

## 🚫 Anti-Patterns

### ❌ Surutilisation
```python
# ❌ Mauvais : Packager codebase à chaque petite modification
mcp_repomix_pack_codebase(...)  # Inutile pour changement mineur

# ✅ Bon : Utiliser seulement pour analyse majeure
# Pour petits changements, utiliser grep directement
```

### ❌ Tests E2E Non Optimisés
```python
# ❌ Mauvais : Prendre screenshot à chaque étape
for step in steps:
    do_step()
    mcp_playwright_browser_take_screenshot()  # Trop de screenshots

# ✅ Bon : Screenshot seulement aux points critiques
mcp_playwright_browser_take_screenshot(filename="final-state.png")
```

### ❌ Documentation Redondante
```python
# ❌ Mauvais : Indexer même bibliothèque plusieurs fois
mcp_docs-mcp-server_scrape_docs(library="react")  # Déjà indexé
mcp_docs-mcp-server_scrape_docs(library="react")  # Redondant

# ✅ Bon : Vérifier d'abord avec list_libraries
libraries = mcp_docs-mcp-server_list_libraries()
if "react" not in libraries:
    mcp_docs-mcp-server_scrape_docs(...)
```

---

## 🔗 Intégration avec TDD

### Workflow TDD avec MCP Tools

1. **Red** : Écrire test
   - Utiliser `mcp_playwright_browser_snapshot` pour valider état initial
   
2. **Green** : Implémenter code minimal
   - Utiliser `mcp_docs-mcp-server_search_docs` pour recherche documentation
   - Utiliser `mcp_repomix_grep_repomix_output` pour trouver patterns similaires
   
3. **Refactor** : Améliorer code
   - Utiliser `mcp_sequential-thinking_sequentialthinking` pour analyser améliorations
   - Utiliser `mcp_playwright_browser_*` pour valider pas de régression

4. **Validation** : Tests passent
   - Utiliser `mcp_playwright_browser_take_screenshot` pour documentation
   - Utiliser `mcp_memory_create_entities` pour documenter décisions

---

## 📊 Tableau Récapitulatif

| MCP Tool | Catégorie | Quand Utiliser | Fréquence |
|----------|-----------|----------------|-----------|
| `repomix_pack_codebase` | Analyse | Analyse majeure, audit | Occasionnel |
| `docs_search_docs` | Documentation | Recherche patterns, exemples | Fréquent |
| `playwright_browser_*` | Tests E2E | Validation UI, tests régression | Très fréquent |
| `context7_get-library-docs` | Documentation | Documentation structurée | Modéré |
| `memory_create_entities` | Connaissance | Modélisation architecture | Occasionnel |
| `sequential-thinking` | Analyse | Problèmes complexes | Modéré |

---

## 🔗 Liens

- **TDD Methodology** : `.cursor/rules/tdd-methodology.mdc`
- **Test Plan** : `docs/TEST_PLAN.md`
- **DEVBOOK** : `docs/DEVBOOK.md`

---

**Dernière mise à jour** : 2025-11-01  
**Version** : 1.0.0

