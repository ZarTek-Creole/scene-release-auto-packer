# ⚠️ Risks Register - eBook Scene Packer v2

**Date de création** : 2025-11-01  
**Mise à jour** : Dynamique à chaque itération

---

## 📊 Vue d'Ensemble

Registre complet des risques identifiés avec analyses SWOT, probabilité, impact et plans de mitigation.

---

## 🎯 Légende

### Probabilité
- **🔴 Haute** : > 70%
- **🟡 Moyenne** : 30-70%
- **🟢 Faible** : < 30%

### Impact
- **🔴 Critique** : Bloque projet ou fonctionnalité majeure
- **🟡 Important** : Impact significatif sur délais/qualité
- **🟢 Mineur** : Impact limité, gérable

### Statut
- **⏳ Identifié** : Risque identifié, mitigation à planifier
- **🔄 En mitigation** : Plan en cours d'exécution
- **✅ Mitigé** : Risque contrôlé
- **❌ Accepté** : Risque accepté, monitoring

---

## 📋 Registre des Risques

### RISK-001 : Complexité Wizard Multi-étapes

**Description** : Le wizard 9 étapes peut devenir complexe à maintenir et tester.

**Probabilité** : 🟡 Moyenne (50%)  
**Impact** : 🟡 Important  
**Statut** : ⏳ Identifié

**SWOT** :
- **Forces** : Architecture modulaire (React), composants réutilisables
- **Faiblesses** : Nombreuses étapes, état complexe
- **Opportunités** : Design pattern wizard éprouvé, librairies React
- **Menaces** : Régressions possibles, tests E2E complexes

**Plan de Mitigation** :
1. Découper wizard en composants modulaires
2. State management clair (Context API ou Redux)
3. Tests unitaires par étape
4. Tests E2E complets du flux
5. Documentation claire du flux

**Responsable** : Équipe Frontend  
**Date révision** : À chaque étape wizard complétée

---

### RISK-002 : Intégration APIs Externes

**Description** : Dépendance aux APIs externes (OpenLibrary, Google Books, OMDb, etc.) peut causer des pannes ou limitations.

**Probabilité** : 🟡 Moyenne (40%)  
**Impact** : 🟡 Important  
**Statut** : ⏳ Identifié

**SWOT** :
- **Forces** : APIs documentées, fallback possible
- **Faiblesses** : Pas de contrôle externe, rate limits
- **Opportunités** : Caching, retry logic
- **Menaces** : Changements APIs, downtime externe

**Plan de Mitigation** :
1. Implémenter caching robuste
2. Retry logic avec backoff exponentiel
3. Fallback si API indisponible
4. Monitoring des APIs
5. Tests avec mocks pour isolation

**Responsable** : Équipe Backend  
**Date révision** : Avant Phase 3

---

### RISK-003 : Performance Base de Données

**Description** : Nombreuses requêtes DB peuvent impacter performance.

**Probabilité** : 🟡 Moyenne (45%)  
**Impact** : 🟡 Important  
**Statut** : ⏳ Identifié

**SWOT** :
- **Forces** : SQLAlchemy ORM optimisé, indexes possibles
- **Faiblesses** : Requêtes N+1 possibles, pas encore optimisé
- **Opportunités** : Caching, pagination, indexes
- **Menaces** : Volume données croissant

**Plan de Mitigation** :
1. Indexes sur colonnes fréquemment requêtées
2. Eager loading (joinedload, subqueryload)
3. Caching Flask-Caching
4. Pagination systématique
5. Monitoring requêtes lentes

**Responsable** : Équipe Backend  
**Date révision** : Phase 1, Phase 8

---

### RISK-004 : Sécurité JWT et Credentials

**Description** : Risques de sécurité avec JWT, chiffrement credentials, gestion tokens.

**Probabilité** : 🟢 Faible (20%)  
**Impact** : 🔴 Critique  
**Statut** : ⏳ Identifié

**SWOT** :
- **Forces** : Bibliothèques éprouvées (Flask-JWT-Extended), best practices
- **Faiblesses** : Implémentation custom nécessaire
- **Opportunités** : Audit sécurité, tests pénétration
- **Menaces** : Vulnérabilités connues, attaques

**Plan de Mitigation** :
1. Audit sécurité régulier
2. Rotation secrets régulière
3. Expiration tokens courte
4. Révocation tokens fonctionnelle
5. Tests sécurité automatisés
6. Chiffrement credentials robuste (Fernet/AES-GCM)

**Responsable** : Équipe Sécurité/Backend  
**Date révision** : Phase 1, Phase 8

---

### RISK-005 : Complexité Tests E2E

**Description** : Tests E2E du wizard complet peuvent être fragiles et longs.

**Probabilité** : 🟡 Moyenne (55%)  
**Impact** : 🟡 Important  
**Statut** : ⏳ Identifié

**SWOT** :
- **Forces** : Playwright robuste, tests isolés possibles
- **Faiblesses** : Temps exécution, flaky tests possibles
- **Opportunités** : Parallélisation, CI/CD
- **Menaces** : Maintenance coûteuse, faux positifs

**Plan de Mitigation** :
1. Tests E2E critiques seulement
2. Tests unitaires/integration en priorité
3. Fixtures robustes
4. Retry logic pour tests flaky
5. Parallélisation CI/CD
6. Monitoring temps exécution

**Responsable** : Équipe QA  
**Date révision** : Phase 8

---

### RISK-006 : Dépendance scenerules.org

**Description** : Scraping scenerules.org peut échouer si structure change.

**Probabilité** : 🟡 Moyenne (50%)  
**Impact** : 🟡 Important  
**Statut** : ⏳ Identifié

**SWOT** :
- **Forces** : Caching rules locales, fallback
- **Faiblesses** : Pas de contrôle externe, structure peut changer
- **Opportunités** : API officielle future, scraping robuste
- **Menaces** : Blocage IP, changements structure

**Plan de Mitigation** :
1. Caching agressif rules téléchargées
2. Scraping robuste avec retry
3. Tests scraping isolés
4. Fallback vers rules locales si échec
5. Monitoring changements structure

**Responsable** : Équipe Backend  
**Date révision** : Phase 5

---

### RISK-007 : Retards Délais

**Description** : Délais estimés peuvent être sous-estimés, causant retards.

**Probabilité** : 🟡 Moyenne (60%)  
**Impact** : 🟡 Important  
**Statut** : ⏳ Identifié

**SWOT** :
- **Forces** : Estimation basée sur v1, méthodologie Agile
- **Faiblesses** : Complexité sous-estimée possible, imprévus
- **Opportunités** : Priorisation MoSCoW, itérations courtes
- **Menaces** : Scope creep, dépendances bloquantes

**Plan de Mitigation** :
1. Buffer 20% sur estimations
2. Priorisation MoSCoW stricte
3. Sprints courts (2 semaines)
4. Révision estimations régulière
5. Focus Must Have en priorité
6. Monitoring progression hebdomadaire

**Responsable** : Équipe Project Management  
**Date révision** : Chaque sprint

---

### RISK-008 : Maintenance Code v2

**Description** : Code v2 doit rester maintenable malgré complexité.

**Probabilité** : 🟢 Faible (30%)  
**Impact** : 🟡 Important  
**Statut** : ⏳ Identifié

**SWOT** :
- **Forces** : Architecture modulaire, TDD, documentation
- **Faiblesses** : Complexité croissante, équipe réduite possible
- **Opportunités** : Code reviews, refactoring régulier
- **Menaces** : Dette technique, turnover équipe

**Plan de Mitigation** :
1. Code reviews obligatoires
2. Refactoring régulier
3. Documentation à jour
4. Tests comme documentation
5. Patterns clairs et documentés

**Responsable** : Équipe Développement  
**Date révision** : Continu

---

## 📊 Matrice Risques

| Risque | Probabilité | Impact | Priorité | Statut |
|--------|-------------|--------|----------|--------|
| RISK-001 | Moyenne | Important | 🟡 | Identifié |
| RISK-002 | Moyenne | Important | 🟡 | Identifié |
| RISK-003 | Moyenne | Important | 🟡 | Identifié |
| RISK-004 | Faible | Critique | 🔴 | Identifié |
| RISK-005 | Moyenne | Important | 🟡 | Identifié |
| RISK-006 | Moyenne | Important | 🟡 | Identifié |
| RISK-007 | Moyenne | Important | 🟡 | Identifié |
| RISK-008 | Faible | Important | 🟢 | Identifié |

---

## 🔄 Processus de Suivi

### Révision Hebdomadaire
- Identifier nouveaux risques
- Mettre à jour statuts
- Ajuster plans mitigation
- Communiquer changements

### Mise à Jour Dynamique
- À chaque itération/sprint
- À chaque phase complétée
- Après incidents
- Après changements majeurs

---

## 🔗 Liens

- **CDC** : `docs/cdc.md`
- **DEVBOOK** : `docs/DEVBOOK.md`
- **Test Plan** : `docs/TEST_PLAN.md`

---

**Dernière mise à jour** : 2025-11-01  
**Prochaine révision** : 2025-11-08 (hebdomadaire)

