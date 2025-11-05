# Images et Assets

## 📁 Structure

```
public/images/
├── logo.svg          # Logo principal (à créer)
├── logo.png          # Logo PNG fallback
├── og-image.png      # Image Open Graph (1200x630px)
└── og-image.webp     # Version WebP optimisée
```

## 🎨 Logo

### Spécifications
- **Format principal** : SVG (vectoriel, scalable)
- **Format fallback** : PNG (256x256px)
- **Couleurs** : Utiliser les variables CSS du Design System
- **Style** : Moderne, professionnel, identifiable

### Génération
```bash
# Créer logo SVG avec Inkscape/Illustrator
# Exporter en PNG 256x256px pour fallback
# Optimiser avec SVGO pour SVG
npx svgo logo.svg -o logo-optimized.svg
```

## 🖼️ Open Graph Image

### Spécifications
- **Taille** : 1200x630px (ratio 1.91:1)
- **Format** : PNG (original) + WebP (optimisé)
- **Contenu** : Logo + titre + description courte
- **Style** : Cohérent avec le design du site

### Génération
```bash
# Créer avec outils graphiques (Figma, Photoshop, etc.)
# Optimiser avec sharp
sharp-cli --input og-image.png \
  --output og-image.webp \
  --quality 90 \
  --format webp
```

## 📝 Instructions

1. **Logo** : Créer/modifier le logo selon les spécifications
2. **OG Image** : Créer l'image Open Graph pour les réseaux sociaux
3. **Optimisation** : Convertir en WebP pour meilleures performances
4. **Mise à jour** : Mettre à jour les références dans layout.tsx et page.tsx

