# ADR-008 : Choix Framework Site Web Public

**Date** : 2025-11-03  
**Statut** : ✅ **APPROUVÉ**  
**Décision** : Next.js 15 avec App Router

---

## Contexte

Le projet eBook Scene Packer v2 nécessite un site web public pour présenter l'application, la documentation, et les guides. Plusieurs options de framework sont disponibles.

---

## Options Considérées

### Option 1 : Next.js 15 (Recommandé) ✅

**Avantages** :
- ✅ React 19 compatible (cohérence avec frontend)
- ✅ SSR/SSG pour performance et SEO
- ✅ TypeScript support natif
- ✅ App Router moderne (Next.js 15)
- ✅ Déploiement facile sur Vercel
- ✅ Excellent pour SEO et performance
- ✅ API Routes si nécessaire
- ✅ Image optimization intégrée

**Inconvénients** :
- ⚠️ Légèrement plus complexe que VitePress
- ⚠️ Plus de configuration initiale

**Score** : **9/10**

---

### Option 2 : VitePress

**Avantages** :
- ✅ Très léger et rapide
- ✅ Markdown-first (idéal pour docs)
- ✅ Basé sur Vite (cohérence avec frontend)
- ✅ Configuration minimale

**Inconvénients** :
- ❌ Moins flexible pour pages custom
- ❌ Pas de React Components natifs
- ❌ Moins adapté pour landing page complexe

**Score** : **6/10**

---

### Option 3 : Astro

**Avantages** :
- ✅ Performance maximale (Islands architecture)
- ✅ SEO optimisé
- ✅ Multi-framework support

**Inconvénients** :
- ❌ Courbe d'apprentissage
- ❌ Moins de ressources/documentation
- ❌ Overkill pour site simple

**Score** : **7/10**

---

## Décision

**Choix** : **Next.js 15 avec App Router**

**Raisons** :
1. ✅ **Cohérence** : React 19 utilisé dans le projet principal
2. ✅ **Performance** : SSR/SSG optimisé pour SEO
3. ✅ **Flexibilité** : Supporte landing page complexe ET documentation
4. ✅ **Écosystème** : Large communauté et documentation
5. ✅ **Déploiement** : Vercel intégré (gratuit pour projets open-source)
6. ✅ **TypeScript** : Support natif strict
7. ✅ **Future-proof** : Framework maintenu activement

---

## Conséquences

### Positives
- Site web moderne et performant
- SEO optimisé automatiquement
- Cohérence avec le projet principal
- Déploiement facile sur Vercel

### Négatives
- Configuration initiale plus importante
- Nécessite connaissance Next.js (mais équipe compétente)

### Mitigation
- Utiliser Next.js App Router (plus simple que Pages Router)
- Documentation Next.js complète disponible
- Template Next.js pour démarrer rapidement

---

## Implémentation

**Version** : Next.js 15.1.8 (dernière stable)  
**TypeScript** : Strict mode  
**Styling** : Bootstrap 5 (cohérence avec app)  
**Icônes** : Bootstrap Icons  

**Structure** :
```
site-web/
├── app/              # App Router (Next.js 15)
├── components/      # Composants React
├── public/          # Assets statiques
└── package.json
```

---

## Validation

- [x] Options analysées
- [x] Décision documentée
- [x] Implémentation planifiée
- [x] Cohérence avec projet vérifiée

---

**Dernière mise à jour** : 2025-11-03  
**Auteur** : Lead Dev  
**Version** : 1.0.0

