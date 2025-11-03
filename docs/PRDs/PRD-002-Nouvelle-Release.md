# PRD-002 : Nouvelle Release Wizard

**ID** : PRD-002  
**Version** : 1.0.0  
**Date** : 2025-11-01  
**Statut** : Draft  
**Auteur** : Dev Team

---

## Vue d'Ensemble

Wizard interactif en 9 étapes permettant la création et le packaging d'une nouvelle release Scene (EBOOK, TV, DOCS, etc.) via un processus guidé avec validation à chaque étape, enrichissement automatique des métadonnées, prévisualisation en temps réel et sauvegarde de progression.

**Priorité MoSCoW** : Must Have

**Phase** : Phase 2 (après Infrastructure Core)

---

## User Stories

### US-002-001 : Étape 1 - Saisie Groupe
**En tant que** opérateur  
**Je veux** saisir le nom du groupe Scene  
**Afin de** identifier l'auteur de la release

**Critères d'acceptation** :
- Input texte avec autocomplete (suggestions groupes existants)
- Validation format Scene (regex)
- Stockage backend (Job avec statut draft)
- Message d'erreur si format invalide
- Bouton "Suivant" activé uniquement si valide

### US-002-002 : Étape 2 - Sélection Type Release
**En tant que** opérateur  
**Je veux** sélectionner le type de release (EBOOK en priorité)  
**Afin de** définir les formats de fichiers acceptés et la règle à appliquer

**Critères d'acceptation** :
- Types disponibles : EBOOK (priorité), TV, DOCS, AUDIOBOOK, GAME (après confirmation EBOOK)
- Format fichiers acceptés selon rules de scenerules.org
- Sélection unique (radio buttons ou cards)
- Affichage formats acceptés pour type sélectionné

### US-002-003 : Étape 3 - Sélection Règle
**En tant que** opérateur  
**Je veux** sélectionner la règle Scene à appliquer  
**Afin de** respecter les standards Scene pour le type de release

**⚠️ EXIGENCE ABSOLUE** : Pour packager des EBOOK, il est **IMPÉRATIF** de prendre connaissance **TOTALE et INTÉGRALE** des règles disponibles sur [scenerules.org](https://scenerules.org/). La règle **[2022] eBOOK** DOIT être analysée complètement avant packaging pour garantir conformité 100%.

**Critères d'acceptation** :
- Sources : Rules locales + scenerules.org + upload
- Format affichage : Liste ET arborescence (double vue avec toggle)
- Filtrage : Par scène, section, année, type release
- Recherche textuelle dans règles
- Prévisualisation règle avant sélection (NFO viewer)
- Upload de règle personnalisée possible
- **Pour EBOOK** : Règle [2022] eBOOK téléchargée et analysée intégralement
- **Pour EBOOK** : Spécifications extraites (formats, nommage, contraintes) et stockées dans `rule_specs`

### US-002-004 : Étape 4 - Sélection Fichier
**En tant que** opérateur  
**Je veux** sélectionner le fichier à packager (local ou distant)  
**Afin de** préparer le packaging

**Critères d'acceptation** :
- Upload local : Drag & drop, sélecteur de fichiers, navigation dans l'arborescence
- URL distante : HTTP/HTTPS uniquement (pas FTP direct)
- Taille maximale : 20GB
- Validation en temps réel : Format, taille, intégrité
- Affichage informations fichier (nom, taille, date)
- Barre de progression pour téléchargement distant

### US-002-005 : Étape 5 - Analyse Fichier
**En tant que** opérateur  
**Je veux** voir l'analyse complète du fichier  
**Afin de** vérifier les métadonnées extraites avant packaging

**Critères d'acceptation** :
- Extraction métadonnées : Maximum possibles (titre, auteur, ISBN, etc.)
- MediaInfo : Pour tous types (pas seulement TV)
- Temps traitement estimé affiché avec barre de progression
- Affichage résultats structurés (onglets ou sections)
- Possibilité de relancer l'analyse si erreur

### US-002-006 : Étape 6 - Enrichissement Métadonnées
**En tant que** opérateur  
**Je veux** enrichir les métadonnées avec des APIs externes  
**Afin de** compléter automatiquement les informations manquantes

**Critères d'acceptation** :
- APIs recherchées sur internet selon Type Release
- Ordre de priorité configurable par utilisateur
- Affichage résultats toutes sources (avec source identifiée)
- Validation manuelle obligatoire avec prévisualisation
- Possibilité d'accepter/refuser chaque enrichissement
- Édition manuelle complète possible

### US-002-007 : Étape 7 - Templates NFO
**En tant que** opérateur  
**Je veux** sélectionner et éditer un template NFO  
**Afin de** personnaliser le fichier NFO généré

**Critères d'acceptation** :
- Stockage templates : Disque OU base de données (choix configurable)
- Édition inline avec visualisation "NFO viewer" monospace, UTF-8
- Prévisualisation temps réel avec "NFO viewer" monospace, UTF-8
- Placeholders : `{{variable}}`, conditionnelles `{% if %}`, fonctions `{{format_date(date)}}`
- Injection automatique métadonnées dans template
- Validation template avant sauvegarde

### US-002-008 : Étape 8 - Options et Paramètres
**En tant que** opérateur  
**Je veux** configurer les options de packaging  
**Afin de** personnaliser le processus de packaging

**Critères d'acceptation** :
- Paramètres affichés : Tout ce qui peut être utile
- Configuration packaging (ZIP, RAR, volumes, taille volumes, etc.)
- Options commandes affichées et éditables
- Validation avant exécution obligatoire
- Bouton "Valider et Packager"
- Logs en temps réel pendant packaging
- Barre de progression packaging

### US-002-009 : Étape 9 - Destination
**En tant que** opérateur  
**Je veux** choisir la destination de la release packagée  
**Afin de** stocker ou transférer la release finalisée

**Critères d'acceptation** :
- Formats destination : Directory local (avec backup fichier source)
- Test connexion avant upload (pour FTP/SSH)
- Progress bar upload visible
- Confirmation succès/échec upload
- Affichage chemin/nom fichier destination

### US-002-010 : Navigation Wizard
**En tant que** opérateur  
**Je veux** naviguer entre les étapes du wizard  
**Afin de** corriger ou modifier mes choix précédents

**Critères d'acceptation** :
- Boutons "Précédent" / "Suivant" sur chaque étape
- Indicateur progression (Étape X/9)
- Validation étape avant passage suivante
- Sauvegarde automatique progression (backend draft + localStorage)
- Possibilité quitter et reprendre plus tard
- Affichage étapes complétées/incomplètes

---

## Détails Fonctionnels

### Architecture Wizard

**Gestion État** :
- **Frontend** : Context API React (`WizardContext`)
- **Backend** : Job avec statut `draft` (sauvegarde progression)
- **Persistance** : Hybride (localStorage pour UX rapide + backend pour persistance)

**Composants React** :
- `WizardContainer` : Container principal avec state global
- `WizardNavigation` : Boutons Previous/Next
- `WizardProgress` : Indicateur progression (1/9, 2/9, etc.)
- `StepGroup` : Étape 1
- `StepReleaseType` : Étape 2
- `StepRules` : Étape 3
- `StepFileSelection` : Étape 4
- `StepAnalysis` : Étape 5
- `StepEnrichment` : Étape 6
- `StepTemplates` : Étape 7
- `StepOptions` : Étape 8
- `StepDestination` : Étape 9

---

### Étape 1 : Groupe Scene

**Objectif** : Saisir le nom du groupe Scene

**UI** :
- Input texte avec autocomplete
- Suggestions basées sur groupes existants en base de données
- Validation en temps réel (regex format Scene)
- Message d'erreur sous l'input si invalide
- Bouton "Suivant" disabled si invalide

**Validation** :
- Format Scene : Regex à définir (ex: `^[A-Z0-9]+$`, min 2 chars, max 100)
- Non vide
- Caractères autorisés uniquement (pas de caractères spéciaux)

**Stockage** :
- Sauvegarde immédiate dans Job backend (statut `draft`)
- Stockage aussi dans localStorage pour UX rapide
- Clé : `wizard.group`

**Backend** :
- Endpoint : `POST /api/wizard/step/1/validate`
- Endpoint : `POST /api/wizard/step/1/save`
- Création Job si première sauvegarde

**Exemple validation** :
```python
def validate_group(group: str) -> tuple[bool, list[str]]:
    """Valide format groupe Scene."""
    errors = []
    if not group or len(group.strip()) == 0:
        errors.append("Le nom du groupe est requis")
    elif len(group) < 2:
        errors.append("Le nom du groupe doit contenir au moins 2 caractères")
    elif len(group) > 100:
        errors.append("Le nom du groupe ne peut pas dépasser 100 caractères")
    elif not re.match(r'^[A-Z0-9]+$', group):
        errors.append("Le nom du groupe doit contenir uniquement lettres majuscules et chiffres")
    return len(errors) == 0, errors
```

---

### Étape 2 : Type Release

**Objectif** : Sélectionner le type de release

**UI** :
- Cards ou radio buttons pour chaque type
- Types disponibles :
  - **EBOOK** (priorité) - Formats : EPUB, PDF, MOBI, AZW, AZW3, CBZ
  - TV (après EBOOK) - Formats : MKV, MP4, AVI, etc.
  - DOCS (après EBOOK) - Formats : DOCX, PDF, TXT, etc.
  - AUDIOBOOK (après EBOOK) - Formats : MP3, FLAC, etc.
  - GAME (après EBOOK) - Formats : ISO, etc.
- Affichage formats acceptés pour type sélectionné
- Information : "Types supplémentaires disponibles après confirmation EBOOK"

**Validation** :
- Type valide selon règles Scene
- **Pour EBOOK** : Vérification formats acceptés selon règle eBOOK [2022] scenerules.org
  - **Formats acceptés** (Section 2.6) : **PDF, EPUB, CBZ, AZW, KF8, PRC, MOBI**
  - ✅ Formats exacts extraits de règle eBOOK [2022] : Documentée dans `docs/EBOOK_RULES_2022_COMPLETE.md`
  - Validation contre `EbookRuleSpec.accepted_formats` (chargé depuis règle complète)

**Stockage** :
- Clé : `wizard.release_type`
- Impact sur étapes suivantes (filtrage règles, formats fichiers)

**Dépendances** :
- Étape 3 : Filtrage règles par type
- Étape 4 : Validation formats fichiers par type

---

### Étape 3 : Règle Scene ⚠️ CRITIQUE

**Objectif** : Sélectionner la règle Scene à appliquer

**⚠️ EXIGENCE ABSOLUE** : Pour packaging EBOOK, connaissance TOTALE et INTÉGRALE des règles scenerules.org obligatoire.  
**Voir** : 
- `docs/SCENERULES_INTEGRATION.md` : Intégration générale scenerules.org
- `docs/EBOOK_RULES_2022_COMPLETE.md` : **Règle eBOOK [2022] COMPLÈTE parsée** ⭐
- `docs/PACKAGING_EBOOK_SPEC.md` : Spécification packaging conforme règle [2022]

**Règle eBOOK Prioritaire** :
- **[2022] eBOOK** (English) ⭐ **OBLIGATOIRE pour packaging EBOOK conforme**
- **Source** : [scenerules.org](https://scenerules.org/)
- **URL** : `https://scenerules.org/html/2022_EBOOK.html` ✅ **Récupérée et documentée**
- **Format** : HTML/NFO avec 8 sections complètes :
  1. Introduction & Notes
  2. Technical Details (scans, retail, hybrid, DRM, NFO/DIZ, formats)
  3. Packaging (global rules, ZIP archives, tailles autorisées)
  4. NFO-File (informations mandataires/optionnelles)
  5. Dirnaming (magazines, comics, manga, books, newspapers, XXX)
  6. Dupes/Proper
  7. Miscellaneous
  8. Sign
- **Contenu complet** : Toutes spécifications documentées dans `docs/EBOOK_RULES_2022_COMPLETE.md`

**UI** :
- **Double vue** :
  - Vue Liste : Liste plate avec recherche
  - Vue Arborescence : Arborescence par scène/section/année
  - Toggle entre les deux vues
- **Filtres** :
  - Par scène (English, French, German, etc.)
  - Par section (eBOOK, TV-720p, X264, etc.)
  - Par année
  - Par type release (auto-filtré selon étape 2)
- **Recherche** : Recherche textuelle dans nom/contenu règle
- **Prévisualisation** : NFO viewer pour prévisualiser règle avant sélection
- **Upload** : Possibilité uploader règle personnalisée
- **Indicateur** : Règle eBOOK [2022] marquée comme "Recommandée" pour EBOOK

**Sources** :
- **scenerules.org** : ⭐ PRIORITÉ - Téléchargement automatique si pas locale
  - **URL HTML** : `https://scenerules.org/html/2022_EBOOK.html` ✅ **Récupérée et parsée**
  - **URL NFO** : `https://scenerules.org/nfo/2022_EBOOK.nfo` (format ASCII)
  - Téléchargement et parsing automatique
  - Mise en cache locale
  - **Règle complète** : 8 sections documentées dans `docs/EBOOK_RULES_2022_COMPLETE.md`
- **Rules locales** : Stockées en base de données (téléchargées depuis scenerules.org)
- **Upload** : Upload fichier NFO local (pour règles personnalisées)

**Sélection** :
- Sélection unique (radio ou highlight)
- **Pour EBOOK** : Suggestion automatique règle eBOOK [2022] English
- Affichage informations règle (nom, scène, section, année, date mise à jour)
- Bouton "Voir détails" → NFO viewer complet
- **Validation** : Règle complète chargée et parsée avant validation étape

**Stockage** :
- Clé : `wizard.rule_id` (si locale) ou `wizard.rule_url` (si scenerules.org)
- **Contenu règle complet** : Chargé, parsé et stocké pour validation toutes étapes
- **Specification règle** : Formats acceptés, template NFO, contraintes extraites
- **Structure** : `EbookRuleSpec` complète stockée

**Backend** :
- Endpoint : `GET /api/rules?type=EBOOK&scene=English&section=eBOOK&year=2022`
- Endpoint : `GET /api/rules/scenerules?type=EBOOK&year=2022` (téléchargement scenerules.org)
- Endpoint : `POST /api/rules/download` (téléchargement depuis scenerules.org)
- Endpoint : `POST /api/rules/upload` (upload règle personnalisée)
- Endpoint : `GET /api/rules/:id/preview` (prévisualisation NFO viewer)
- Endpoint : `GET /api/rules/:id/spec` (spécification parsée : formats, template, contraintes)

**Validation Critique** :
- ✅ Règle eBOOK [2022] chargée complètement
- ✅ Tous formats acceptés extraits
- ✅ Template NFO extrait
- ✅ Toutes contraintes parsées
- ✅ Règle valide et complète avant validation étape

---

### Étape 4 : Sélection Fichier

**Objectif** : Sélectionner le fichier à packager

**UI - Upload Local** :
- **Drag & Drop** : Zone drop zone visible
- **Sélecteur** : Bouton "Choisir fichier" → file input
- **Navigation arborescence** : Explorer fichiers serveur (si configuré)
- Affichage informations fichier sélectionné (nom, taille, date, chemin)

**UI - URL Distante** :
- Input URL (HTTP/HTTPS uniquement)
- Bouton "Télécharger"
- Barre progression téléchargement
- Validation URL format
- Taille fichier affichée après téléchargement

**Validation** :
- **Format** : Selon type release sélectionné (étape 2)
- **Taille** : Maximum 20GB
- **Intégrité** : Vérification checksum si disponible
- **Temps réel** : Validation immédiate après sélection

**Stockage** :
- **Local** : Chemin fichier stocké
- **Distant** : Fichier téléchargé temporairement, chemin stocké
- Clé : `wizard.file_path`
- Clé : `wizard.file_source` ("local" ou "remote")

**Backend** :
- Endpoint : `POST /api/wizard/step/4/validate`
- Endpoint : `POST /api/wizard/step/4/upload` (upload fichier)
- Endpoint : `POST /api/wizard/step/4/download` (téléchargement URL)

**Limites** :
- Taille max : 20GB
- Formats acceptés selon type :
  - EBOOK : `.epub`, `.pdf`, `.mobi`, `.azw`, `.azw3`, `.cbz`
  - TV : `.mkv`, `.mp4`, `.avi`, `.mov`, etc.
  - DOCS : `.docx`, `.pdf`, `.txt`, `.odt`, etc.

---

### Étape 5 : Analyse Fichier

**Objectif** : Analyser le fichier et extraire métadonnées

**UI** :
- Barre progression "Analyse en cours..."
- Temps traitement estimé affiché
- Résultats affichés structurés :
  - Onglet "Métadonnées" : Titre, auteur, ISBN, année, etc.
  - Onglet "MediaInfo" : Informations techniques (tous types)
  - Onglet "Structure" : Arborescence interne (EPUB, PDF)
  - Onglet "Résumé" : Vue d'ensemble

**Extraction Métadonnées** :
- **EBOOK** : Titre, auteur, ISBN, année, éditeur, langue, description
- **TV** : Titre, saison, épisode, qualité, codec, résolution, durée
- **DOCS** : Titre, auteur, date création, nombre pages
- **Maximum possible** : Toutes métadonnées extractibles

**MediaInfo** :
- **Tous types** : Extraction MediaInfo pour informations techniques
- Affichage format structuré (JSON ou tree view)
- Informations : Codec, bitrate, résolution, durée, etc.

**Stockage** :
- Résultats sauvegardés dans Job (JSON)
- Clé : `wizard.analysis.metadata`
- Clé : `wizard.analysis.mediainfo`
- Clé : `wizard.analysis.structure`

**Backend** :
- Endpoint : `POST /api/wizard/step/5/analyze`
- Traitement asynchrone (Job) si fichier volumineux
- WebSocket ou polling pour mise à jour progression
- Endpoint : `GET /api/wizard/jobs/:job_id/analysis` (récupérer résultats)

**Performance** :
- Petit fichier (< 100MB) : < 30s
- Gros fichier (< 20GB) : < 5min
- Barre progression mise à jour en temps réel

---

### Étape 6 : Enrichissement Métadonnées

**Objectif** : Enrichir métadonnées avec APIs externes

**UI** :
- Résumé métadonnées actuelles affiché
- Liste APIs disponibles selon Type Release :
  - **EBOOK** : OpenLibrary, Google Books, Goodreads API
  - **TV** : OMDb, TVDB, TMDb
  - **DOCS** : APIs documentaires si disponibles
- Configuration ordre priorité (drag & drop ou liste ordonnée)
- Bouton "Enrichir" → Appels APIs séquentiels
- Résultats affichés avec source identifiée
- Validation manuelle obligatoire : Case à cocher pour chaque enrichissement
- Prévisualisation complète avant validation
- Édition manuelle complète possible

**APIs Recherchées** :
- Recherche automatique APIs selon Type Release sur internet
- Configuration APIs dans PRD-007 (Configurations)
- Ordre priorité configurable par utilisateur (préférences)

**Enrichissement** :
- Appels APIs séquentiels selon ordre priorité
- Fusion intelligente résultats (pas de doublons)
- Métadonnées complétées affichées avec source
- Possibilité accepter/refuser chaque enrichissement

**Validation** :
- Validation manuelle obligatoire
- Prévisualisation complète métadonnées finales
- Édition manuelle possible avant validation
- Bouton "Valider métadonnées"

**Stockage** :
- Métadonnées enrichies sauvegardées
- Clé : `wizard.metadata.enriched`
- Clé : `wizard.metadata.sources` (traçabilité sources)

**Backend** :
- Endpoint : `POST /api/wizard/step/6/enrich`
- Endpoint : `GET /api/wizard/step/6/apis?type=EBOOK` (liste APIs disponibles)
- Endpoint : `PUT /api/wizard/step/6/metadata` (édition manuelle)
- Endpoint : `POST /api/wizard/step/6/validate` (validation finale)

---

### Étape 7 : Templates NFO ⚠️ CRITIQUE

**Objectif** : Sélectionner et éditer template NFO

**⚠️ EXIGENCE ABSOLUE** : Template NFO doit être basé sur template de la règle eBOOK [2022] scenerules.org.

**Template Source** :
- **Priorité** : Template extrait de règle eBOOK [2022] chargée (Étape 3)
- **Fallback** : Templates locaux (si règle ne contient pas template)
- **Validation** : Template conforme à format règle (ASCII ≤ 80 colonnes)

**UI** :
- **Template par défaut** : Template de règle eBOOK [2022] pré-rempli
- Liste templates disponibles (disque ou base de données)
- **Suggestion** : "Utiliser template règle eBOOK [2022]" (bouton)
- Sélection template
- **Édition inline** avec :
  - Zone édition (textarea ou éditeur monospace)
  - **NFO Viewer** monospace UTF-8 à côté (prévisualisation temps réel)
  - Synchronisation automatique édition → prévisualisation
- Placeholders affichés avec tooltip/valeurs
- Injection automatique métadonnées dans template
- **Indicateur conformité** : Badge "Template conforme règle eBOOK [2022]"

**Format Templates** :
- **Format règle** : Template NFO ASCII ≤ 80 colonnes (selon règle eBOOK [2022])
- Placeholders : `{{variable}}` (ex: `{{title}}`, `{{author}}`)
- Conditionnelles : `{% if condition %}...{% endif %}`
- Fonctions : `{{format_date(date)}}`, `{{uppercase(text)}}`, etc.
- Ajout Placeholders progressif selon outputs métadonnées/mediainfo (au fur et à mesure tests)

**Stockage Templates** :
- **Option 1** : Disque (fichiers `.nfo` ou `.template`)
- **Option 2** : Base de données (table `templates`)
- **Choix configurable** : Paramètre système (PRD-007)
- **Template règle** : Stocké automatiquement lors chargement règle (Étape 3)

**Prévisualisation** :
- NFO Viewer monospace UTF-8
- Mise à jour temps réel (défilement < 100ms)
- **Validation format ASCII** : ≤ 80 colonnes (selon règle Scene)
- **Validation UTF-8** : Support UTF-8 mais ASCII préféré selon règle

**Édition** :
- Édition inline (pas de popup)
- **Validation largeur** : Avertissement si ligne > 80 colonnes
- Validation template avant sauvegarde
- Messages d'erreur si placeholders invalides
- **Conformité règle** : Validation que template respecte structure règle eBOOK [2022]

**Stockage** :
- Template sélectionné : Clé `wizard.template_id`
- Template édité : Clé `wizard.template_content`
- Métadonnées injectées : Clé `wizard.template_preview`

**Backend** :
- Endpoint : `GET /api/templates?storage=disk|db`
- Endpoint : `GET /api/templates/:id`
- Endpoint : `POST /api/wizard/step/7/render` (rendu prévisualisation)
- Endpoint : `POST /api/wizard/step/7/validate` (validation template)

---

### Étape 8 : Options et Paramètres ⚠️ CRITIQUE

**Objectif** : Configurer options packaging et valider

**⚠️ EXIGENCE ABSOLUE** : Packaging EBOOK doit respecter STRICTEMENT la règle eBOOK [2022] scenerules.org.  
**Voir** : `docs/SCENERULES_INTEGRATION.md` pour connaissance totale et intégrale des règles.

**Validation contre Règle** :
- ✅ **Règle eBOOK [2022] chargée et parsée complètement**
- ✅ **Validation structure release** : Conforme à spécifications règle
- ✅ **Validation nommage** : Format nom release conforme règle
- ✅ **Validation fichiers** : Tous fichiers requis présents selon règle
- ✅ **Validation NFO** : Template respecté, format ASCII ≤ 80 colonnes
- ✅ **Validation contraintes** : Toutes contraintes règle respectées
- ❌ **JAMAIS** packager si validation règle échoue

**UI** :
- **Avertissement visible** : "Packaging conforme à règle eBOOK [2022] obligatoire"
- Paramètres affichés :
  - **Packaging** :
    - Format : ZIP, RAR, ou les deux (selon règle)
    - Taille volumes (ZIP/RAR) (selon contraintes règle)
    - Compression level (selon règle)
    - Nombre volumes max (selon règle)
  - **Fichiers générés** :
    - NFO : Oui/Non (OBLIGATOIRE selon règle)
    - DIZ : Oui/Non (selon règle)
    - SFV : Oui/Non (selon règle)
    - **Validation** : Fichiers requis selon règle eBOOK [2022]
  - **Commandes** :
    - Options commandes affichées (éditables mais validées contre règle)
    - Paramètres avancés (section collapse)
- **Indicateur conformité** : Badge "Conforme règle eBOOK [2022]" si toutes validations OK
- **Messages erreurs** : Affichage détails si validation règle échoue
- Édition manuelle possible (mais validation règle maintenue)
- Validation avant exécution obligatoire
- Bouton "Valider et Packager" (disabled si validation règle échoue)
- Zone logs en temps réel (pendant packaging)
- Barre progression packaging

**Validation** :
- **Validation règle complète** : TOUTES exigences règle eBOOK [2022] vérifiées
- Vérification tous paramètres valides
- Validation avant exécution obligatoire
- Message confirmation avant packaging (avec résumé validations règle)

**Packaging** :
- **Application règle** : Structure release selon spécifications règle eBOOK [2022]
- **NFO généré** : Selon template de la règle (injecté métadonnées)
- **Nommage** : Format strict selon contraintes règle
- Exécution commandes packaging (Job asynchrone)
- Logs en temps réel (WebSocket ou polling)
- Barre progression mise à jour
- Affichage fichiers générés (arborescence conforme règle)

**Stockage** :
- Options sauvegardées : Clé `wizard.options`
- Job créé avec statut `running`
- Logs stockés : Clé `wizard.logs`

**Backend** :
- Endpoint : `POST /api/wizard/step/8/validate`
- Endpoint : `POST /api/wizard/pack` (lancement packaging)
- Endpoint : `GET /api/wizard/jobs/:job_id/logs` (logs temps réel)
- Endpoint : `GET /api/wizard/jobs/:job_id/status` (statut packaging)

**Performance** :
- Packaging petit fichier : < 30s
- Packaging gros fichier : < 5min
- Logs mis à jour toutes les 500ms

---

### Étape 9 : Destination

**Objectif** : Choisir destination release packagée

**UI** :
- **Directory Local** :
  - Sélection répertoire local
  - Affichage chemin destination
  - Option backup fichier source (checkbox)
- **FTP/SFTP** (si configuré) :
  - Liste destinations FTP/SFTP disponibles
  - Sélection destination
  - Test connexion avant upload (bouton "Tester")
  - Affichage résultat test
- **Progress bar upload** visible
- Confirmation succès/échec upload

**Destination Directory Local** :
- Sélection répertoire (explorer ou saisie chemin)
- Backup fichier source automatique (option activable)
- Affichage chemin complet destination

**Destination FTP/SFTP** :
- Liste destinations depuis PRD-007 (Configurations)
- Test connexion avant upload obligatoire
- Affichage résultat test (succès/échec + message)
- Bouton "Test connexion" visible

**Upload** :
- Progress bar upload visible
- Affichage vitesse upload, temps restant
- Possibilité annuler upload
- Confirmation succès/échec avec message

**Stockage** :
- Destination sauvegardée : Clé `wizard.destination`
- Backup fichier source : Clé `wizard.backup_source`
- Statut upload : Clé `wizard.upload_status`

**Backend** :
- Endpoint : `POST /api/wizard/step/9/destination`
- Endpoint : `POST /api/destinations/:id/test` (test connexion FTP/SSH)
- Endpoint : `POST /api/wizard/jobs/:job_id/upload` (upload release)
- Endpoint : `GET /api/wizard/jobs/:job_id/upload/progress` (progression upload)

---

## Navigation et Persistance

### Navigation Wizard

**Composants** :
- `WizardNavigation` : Boutons "Précédent" / "Suivant"
- `WizardProgress` : Indicateur "Étape X/9" avec étapes complétées/incomplètes
- Navigation possible uniquement si étape validée

**Validation Étapes** :
- Validation avant passage étape suivante
- Message erreur si étape invalide
- Bouton "Suivant" disabled si étape invalide

**Sauvegarde Progression** :
- **Hybride** :
  - localStorage : Sauvegarde immédiate pour UX rapide
  - Backend : Job avec statut `draft` pour persistance
- Sauvegarde automatique après chaque étape validée
- Possibilité quitter et reprendre plus tard :
  - Restauration depuis Job draft
  - Restauration depuis localStorage si Job non disponible

**Reprise Wizard** :
- Liste Jobs drafts dans dashboard
- Bouton "Reprendre" sur Job draft
- Restauration étape où l'utilisateur s'était arrêté

---

## Contraintes Techniques

### Frontend

**Technologies** :
- React 18+ avec TypeScript
- Context API pour état wizard (`WizardContext`)
- React Router v6 pour navigation
- Bootstrap 5 pour UI (grid, utilities, base)
- Bootstrap Icons pour icônes (2 000+ icônes)
- Axios pour appels API

**Design System** :
- **Voir** : `docs/DESIGN_SYSTEM_UI_UX.md` ⭐ pour spécifications complètes
- Système de couleurs (jour/nuit) avec variables CSS
- Typographie (polices système, hiérarchie)
- Bordures élégantes et espacements cohérents
- Icônes : Bootstrap Icons (tailles standardisées)
- Thème jour/nuit avec transition fluide
- Accessibilité WCAG 2.2 AA

**Composants** :
- Structure modulaire (voir PRD-001)
- Composants réutilisables selon Design System :
  - `Button` (variantes, tailles, états, icônes)
  - `Input` (validation, erreurs, icônes)
  - `Card` (bordures, ombres, header/footer)
  - `Tabs` (navigation claire, icônes, états actifs)
  - `ProgressBar` (packaging, uploads)
  - `Alert` (succès, erreur, warning, info)
  - `NFO Viewer` : Composant monospace UTF-8 (ASCII ≤ 80 colonnes)

**Performance** :
- Chargement étape : < 500ms
- Validation temps réel : < 100ms
- Prévisualisation template : < 100ms

### Backend

**Endpoints API** :
- `POST /api/wizard/step/:step/validate` : Validation étape
- `POST /api/wizard/step/:step/save` : Sauvegarde progression
- `GET /api/wizard/step/:step/data` : Récupération données étape
- `POST /api/wizard/pack` : Lancement packaging
- `GET /api/wizard/jobs/:job_id/status` : Statut Job
- `GET /api/wizard/jobs/:job_id/logs` : Logs temps réel
- `GET /api/wizard/jobs/:job_id/analysis` : Résultats analyse
- **Endpoints Rules scenerules.org** :
  - `GET /api/rules?type=:type&scene=:scene&section=:section` : Liste règles
  - `GET /api/rules/scenerules?type=EBOOK&year=2022` : Téléchargement règle eBOOK [2022]
  - `GET /api/rules/:id/spec` : Spécification parsée (formats, template, contraintes)
  - `POST /api/rules/download` : Téléchargement depuis scenerules.org
- Endpoint : `GET /api/templates?storage=:storage` : Liste templates
- Endpoint : `POST /api/templates/:id/render` : Rendu prévisualisation
- Endpoint : `POST /api/destinations/:id/test` : Test connexion

**Services Backend Critiques** :

**⚠️ CRITIQUE - RuleParserService** :
- **OBLIGATOIRE** : Parse règle eBOOK [2022] complète depuis scenerules.org
- **Connaissance TOTALE et INTÉGRALE** : Analyse complète du fichier .nfo
- **Méthode principale** : `parse_ebook_rule_2022(content: str) -> EbookRuleSpec`
- **Extraction complète** :
  - Formats fichiers acceptés (.epub, .pdf, .mobi, .azw3, .cbz)
  - Structure nommage exacte (format, composants, séparateurs, contraintes)
  - Fichiers requis (ZIP, RAR, NFO, DIZ, SFV)
  - Template NFO standardisé (ASCII ≤ 80 colonnes)
  - Contraintes validation (taille, intégrité, métadonnées)
  - Règles packaging (compression, structure, checksums)
- **Stockage** : Spécifications parsées dans table `rule_specs` (JSON structuré)
- **⚠️ SANS parsing complet, packaging ne sera PAS conforme**

**⚠️ CRITIQUE - RuleValidationService** :
- Valide release contre règle complète parsée
- Méthode : `validate_against_rule(release_data: dict, rule_spec: EbookRuleSpec) -> tuple[bool, list[str]]`
- Validation complète :
  - Format fichier conforme à `rule_spec.file_formats.accepted`
  - Nommage conforme à `rule_spec.naming.format` (format exact)
  - Structure fichiers conforme à `rule_spec.required_files`
  - NFO conforme à template de `rule_spec.template`
  - Toutes contraintes respectées
- **⚠️ JAMais packager si validation échoue**

**⚠️ CRITIQUE - ScenerulesDownloadService** :
- Télécharge règles depuis https://scenerules.org/
- Méthode : `download_ebook_rule_2022() -> str`
- Téléchargement règle [2022] eBOOK (format .nfo texte complet)
- Cache local pour éviter re-téléchargements
- Parsing automatique après téléchargement
- Stockage dans table `rules` avec `source='scenerules.org'`

**Voir** :
- `docs/SCENERULES_INTEGRATION_REQUIREMENT.md` ⭐ pour exigence critique
- `docs/SCENE_RULES_EBOOK_ANALYSIS.md` pour analyse détaillée
- `docs/PREREQUISITES_PHASE3_WIZARD.md` pour prérequis avant Phase 3
- `docs/SCENERULES_INTEGRATION.md` pour implémentation complète

**Base de Données** :
- Table `jobs` : Jobs de packaging avec statut `draft`/`running`/`completed`/`failed`
- Table `releases` : Releases créées
- Table `rules` : Rules Scene locales (⚠️ DOIT contenir règle [2022] eBOOK complète)
- Table `rule_specs` : **NOUVELLE** - Spécifications parsées des règles (⚠️ CRITIQUE pour EBOOK)
- Table `templates` : Templates NFO (si stockage DB)

**Sécurité** :
- Protection JWT sur tous endpoints
- Validation stricte inputs (Marshmallow schemas)
- Limite taille fichier : 20GB
- Validation formats fichiers stricts

**Performance** :
- Temps réponse API : < 200ms (p95)
- Packaging petit fichier : < 30s
- Packaging gros fichier : < 5min

---

## Tests (TDD)

### Tests Unitaires Frontend

```typescript
describe('StepGroup', () => {
  it('should validate group format', () => {
    // Test validation regex format Scene
  });
  
  it('should show autocomplete suggestions', () => {
    // Test autocomplete groupes existants
  });
  
  it('should disable Next if invalid', () => {
    // Test bouton Next disabled
  });
});

describe('StepReleaseType', () => {
  it('should display EBOOK as priority', () => {
    // Test affichage EBOOK en priorité
  });
  
  it('should show accepted formats for type', () => {
    // Test affichage formats selon type
  });
});

describe('StepRules', () => {
  it('should toggle between list and tree view', () => {
    // Test toggle vue liste/arborescence
  });
  
  it('should filter rules by scene/section/year', () => {
    // Test filtrage règles
  });
  
  it('should preview rule in NFO viewer', () => {
    // Test prévisualisation règle
  });
});

describe('StepFileSelection', () => {
  it('should validate file format', () => {
    // Test validation format fichier
  });
  
  it('should validate file size (max 20GB)', () => {
    // Test validation taille max
  });
  
  it('should show progress for remote download', () => {
    // Test barre progression téléchargement
  });
});

describe('StepAnalysis', () => {
  it('should display extraction progress', () => {
    // Test barre progression analyse
  });
  
  it('should display all extracted metadata', () => {
    // Test affichage métadonnées
  });
  
  it('should display MediaInfo for all types', () => {
    // Test MediaInfo tous types
  });
});

describe('StepEnrichment', () => {
  it('should fetch APIs according to release type', () => {
    // Test appels APIs selon type
  });
  
  it('should require manual validation', () => {
    // Test validation manuelle obligatoire
  });
  
  it('should allow editing metadata', () => {
    // Test édition manuelle
  });
});

describe('StepTemplates', () => {
  it('should render template with placeholders', () => {
    // Test rendu template avec placeholders
  });
  
  it('should update NFO viewer in real-time', () => {
    // Test prévisualisation temps réel
  });
  
  it('should validate template format', () => {
    // Test validation template
  });
});

describe('StepOptions', () => {
  it('should validate all parameters', () => {
    // Test validation paramètres
  });
  
  it('should show real-time logs during packaging', () => {
    // Test logs temps réel
  });
});

describe('StepDestination', () => {
  it('should test FTP connection before upload', () => {
    // Test connexion FTP
  });
  
  it('should show upload progress', () => {
    // Test barre progression upload
  });
});

describe('WizardNavigation', () => {
  it('should navigate between steps', () => {
    // Test navigation Previous/Next
  });
  
  it('should save progress on step change', () => {
    // Test sauvegarde progression
  });
  
  it('should restore draft job', () => {
    // Test reprise wizard draft
  });
});
```

### Tests Backend

```python
def test_wizard_step_1_validate():
    """Test validation étape 1 (groupe)."""
    response = client.post('/api/wizard/step/1/validate',
                          json={'group': 'TESTGROUP'},
                          headers=auth_headers)
    assert response.status_code == 200
    assert response.json['valid'] is True

def test_wizard_step_1_validate_invalid():
    """Test validation étape 1 avec groupe invalide."""
    response = client.post('/api/wizard/step/1/validate',
                          json={'group': 'invalid-group!'},
                          headers=auth_headers)
    assert response.status_code == 200
    assert response.json['valid'] is False
    assert 'errors' in response.json

def test_wizard_step_4_upload():
    """Test upload fichier étape 4."""
    # Test upload fichier local
    # Test téléchargement URL distante
    # Test validation format/taille

def test_wizard_step_5_analyze():
    """Test analyse fichier étape 5."""
    # Test extraction métadonnées
    # Test extraction MediaInfo
    # Test barre progression

def test_wizard_step_6_enrich():
    """Test enrichissement métadonnées étape 6."""
    # Test appels APIs
    # Test fusion résultats
    # Test validation manuelle

def test_wizard_step_7_render():
    """Test rendu template étape 7."""
    # Test injection placeholders
    # Test prévisualisation NFO

def test_wizard_step_8_pack():
    """Test packaging étape 8."""
    # Test lancement packaging
    # Test logs temps réel
    # Test barre progression

def test_wizard_step_9_destination():
    """Test destination étape 9."""
    # Test sélection directory local
    # Test test connexion FTP
    # Test upload avec progression
```

### Tests E2E (Playwright MCP)

**⚠️ OBLIGATOIRE** : Utiliser Playwright MCP Tools pour tous les tests E2E.

```python
def test_wizard_complete_flow_ebook():
    """Test wizard complet flow EBOOK avec Playwright MCP."""
    # 1. Login
    mcp_playwright_browser_navigate(url="http://localhost:5000/login")
    mcp_playwright_browser_type(element="username", text="operator")
    mcp_playwright_browser_type(element="password", text="password")
    mcp_playwright_browser_click(element="login button")
    
    # 2. Naviguer vers wizard
    mcp_playwright_browser_navigate(url="http://localhost:5000/releases/new")
    mcp_playwright_browser_snapshot()
    
    # 3. Étape 1 : Groupe
    mcp_playwright_browser_type(element="group input", text="TESTGROUP")
    mcp_playwright_browser_wait_for(text="Valid")
    mcp_playwright_browser_click(element="Next button")
    
    # 4. Étape 2 : Type
    mcp_playwright_browser_click(element="EBOOK card")
    mcp_playwright_browser_click(element="Next button")
    
    # 5. Étape 3 : Règle
    # ... sélection règle ...
    mcp_playwright_browser_click(element="Next button")
    
    # 6. Étape 4 : Fichier
    # ... upload fichier ...
    mcp_playwright_browser_click(element="Next button")
    
    # 7. Étape 5 : Analyse
    mcp_playwright_browser_wait_for(text="Analysis complete")
    mcp_playwright_browser_click(element="Next button")
    
    # 8. Étape 6 : Enrichissement
    # ... validation métadonnées ...
    mcp_playwright_browser_click(element="Next button")
    
    # 9. Étape 7 : Templates
    # ... sélection template ...
    mcp_playwright_browser_click(element="Next button")
    
    # 10. Étape 8 : Options
    # ... configuration options ...
    mcp_playwright_browser_click(element="Pack button")
    mcp_playwright_browser_wait_for(text="Packaging complete")
    
    # 11. Étape 9 : Destination
    # ... sélection destination ...
    mcp_playwright_browser_click(element="Upload button")
    mcp_playwright_browser_wait_for(text="Upload complete")
    
    # 12. Validation completion
    mcp_playwright_browser_snapshot()
    mcp_playwright_browser_take_screenshot(filename="wizard-complete.png")
```

**Scénarios E2E** :
- Flow complet normal EBOOK
- Navigation backward/forward entre étapes
- Validation chaque étape (erreurs affichées)
- Sauvegarde/reprise wizard (draft)
- Gestion erreurs (fichier invalide, API échec, etc.)
- Upload distant avec progression
- Packaging avec logs temps réel

---

## Critères de Réussite

### Fonctionnels

- ✅ Wizard 9 étapes fonctionnel et complet
- ✅ Navigation Previous/Next fonctionnelle
- ✅ Validation chaque étape fonctionnelle
- ✅ Sauvegarde progression (localStorage + backend)
- ✅ Reprise wizard draft fonctionnelle
- ✅ EBOOK priorité : Fonctionnel à 100%
- ✅ Autres types : Disponibles après confirmation EBOOK
- ✅ Prévisualisation temps réel (NFO viewer)
- ✅ Logs temps réel pendant packaging
- ✅ Upload avec progression fonctionnelle

### Performance

- Chargement étape : < 500ms
- Validation temps réel : < 100ms
- Prévisualisation template : < 100ms
- Analyse petit fichier (< 100MB) : < 30s
- Analyse gros fichier (< 20GB) : < 5min
- Packaging petit fichier : < 30s
- Packaging gros fichier : < 5min

### Qualité

- Accessibilité WCAG 2.2 AA
- Responsive design (mobile/tablette/desktop)
- Tests couverture 100%
- Gestion erreurs complète (messages clairs)
- UX fluide et intuitive

---

## Dépendances

- **Phase 1** : Infrastructure Core (JWT, DB, Models)
- **PRD-001** : Interface Administration (navigation)
- **PRD-003** : Liste des Releases (affichage releases créées)
- **PRD-004** : Rules Management (gestion règles)
- **PRD-007** : Configurations (APIs, destinations FTP/SSH)
- **Phase 2** : Frontend React setup (Vite + TypeScript + Context API)

---

## Notes Techniques

### Gestion État Wizard

**Architecture** :
- **Frontend** : Context API React (`WizardContext`)
- **Backend** : Job avec statut `draft` pour persistance
- **Hybride** : localStorage (UX rapide) + backend (persistance)

**Structure Données** :
```typescript
interface WizardState {
  currentStep: number;
  completedSteps: number[];
  data: {
    group?: string;
    releaseType?: 'EBOOK' | 'TV' | 'DOCS' | 'AUDIOBOOK' | 'GAME';
    ruleId?: number;
    ruleUrl?: string;
    filePath?: string;
    fileSource?: 'local' | 'remote';
    analysis?: {
      metadata: Record<string, any>;
      mediainfo: Record<string, any>;
      structure: any;
    };
    metadata?: Record<string, any>;
    templateId?: number;
    templateContent?: string;
    options?: Record<string, any>;
    destination?: string;
  };
  jobId?: number; // Job draft backend
}
```

### Placeholders Templates NFO

**Format** :
- Variables : `{{variable}}` (ex: `{{title}}`, `{{author}}`)
- Conditionnelles : `{% if condition %}...{% endif %}`
- Fonctions : `{{format_date(date)}}`, `{{uppercase(text)}}`

**Placeholders disponibles** (ajout progressif selon tests) :
- Métadonnées : `{{title}}`, `{{author}}`, `{{isbn}}`, `{{year}}`, `{{publisher}}`, etc.
- MediaInfo : `{{mediainfo.codec}}`, `{{mediainfo.resolution}}`, `{{mediainfo.duration}}`, etc.
- Release : `{{group}}`, `{{release_type}}`, `{{date}}`, etc.

**Ajout progressif** : Placeholders ajoutés au fur et à mesure des tests selon besoins réels outputs métadonnées/mediainfo.

---

**Liens** :
- [Backlog Agile](../BACKLOG_AGILE.md)
- [Test Plan](../TEST_PLAN.md)
- [DEVBOOK](../DEVBOOK.md)
- [CDC](../cdc.md)
- [PROJECT_ANALYSIS_QUESTIONS](../PROJECT_ANALYSIS_QUESTIONS.md)

