/**
 * Instructions pour générer et optimiser les screenshots.
 *
 * Ce fichier documente le processus de création des screenshots
 * pour le site web public.
 */

# Instructions pour Screenshots

## 📸 Screenshots Requis

Les screenshots suivants doivent être créés et optimisés :

### 1. Dashboard (`/screenshots/dashboard.png`)
- **Contenu** : Vue d'ensemble du dashboard avec statistiques
- **Taille recommandée** : 1920x1080px
- **Format** : PNG (sera converti en WebP)

### 2. Wizard (`/screenshots/wizard.png`)
- **Contenu** : Vue du wizard 9 étapes en cours
- **Taille recommandée** : 1920x1080px
- **Format** : PNG (sera converti en WebP)

### 3. Releases (`/screenshots/releases.png`)
- **Contenu** : Liste des releases avec filtres
- **Taille recommandée** : 1920x1080px
- **Format** : PNG (sera converti en WebP)

### 4. Rules Management (`/screenshots/rules.png`)
- **Contenu** : Gestion des règles Scene
- **Taille recommandée** : 1920x1080px
- **Format** : PNG (sera converti en WebP)

## 🛠️ Processus de Création

### Étape 1 : Prendre les Screenshots
1. Démarrer l'application en mode développement
2. Se connecter avec un compte admin
3. Naviguer vers chaque page
4. Prendre un screenshot avec :
   - **Chrome DevTools** : Cmd+Shift+P > "Capture screenshot"
   - **Firefox** : DevTools > Settings > Screenshots
   - **Outils tiers** : Shutter, Spectacle, etc.

### Étape 2 : Optimisation des Images
```bash
# Installer sharp (si nécessaire)
npm install -g sharp-cli

# Convertir en WebP avec compression
sharp-cli --input screenshots/dashboard.png \
  --output screenshots/dashboard.webp \
  --quality 85 \
  --format webp

# Redimensionner si nécessaire
sharp-cli --input screenshots/dashboard.png \
  --output screenshots/dashboard-1920.webp \
  --width 1920 \
  --quality 85 \
  --format webp
```

### Étape 3 : Placeholder Images
En attendant les vrais screenshots, utiliser des placeholders SVG optimisés :

```svg
<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#f8f9fa"/>
  <text x="50%" y="50%" text-anchor="middle" font-family="Arial" font-size="48" fill="#6c757d">
    Screenshot à venir
  </text>
</svg>
```

## 📁 Structure Finale

```
site-web/public/screenshots/
├── dashboard.png      (original)
├── dashboard.webp     (optimisé)
├── wizard.png
├── wizard.webp
├── releases.png
├── releases.webp
└── rules.png
└── rules.webp
```

## ⚡ Optimisations Recommandées

- **Format WebP** : Meilleure compression que PNG/JPG
- **Qualité** : 85% (bon compromis taille/qualité)
- **Lazy Loading** : Utiliser `next/image` avec `loading="lazy"`
- **Responsive** : Créer plusieurs tailles (1920px, 1280px, 768px)

## 🔗 Références

- [Next.js Image Optimization](https://nextjs.org/docs/app/api-reference/components/image)
- [WebP Guide](https://developers.google.com/speed/webp)
- [Image Optimization Best Practices](https://web.dev/fast/#optimize-your-images)

