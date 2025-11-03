# 🎯 Intégration Scenerules.org - Documentation Critique

**Date** : 2025-11-01  
**Statut** : CRITIQUE ⚠️  
**Source** : [scenerules.org](https://scenerules.org/)

---

## ⚠️ EXIGENCE ABSOLUE

**Pour packager des EBOOK, il est IMPÉRATIF de prendre connaissance TOTALE et INTÉGRALE des règles disponibles sur [scenerules.org](https://scenerules.org/).**

Le processus de packaging EBOOK doit :
1. ✅ **Charger** la règle eBOOK complète depuis scenerules.org
2. ✅ **Comprendre** toutes les exigences de la règle
3. ✅ **Valider** que le packaging respecte TOUTES les contraintes
4. ✅ **Appliquer** strictement les formats, structures et nommages définis

---

## 📋 Règles eBOOK Disponibles sur scenerules.org

D'après [scenerules.org](https://scenerules.org/), les règles eBOOK disponibles sont :

### English Rules (Priorité)

#### Current English Rules
- **[2022] eBOOK** [p/t/n/d] ⭐ **VERSION ACTUELLE - PRIORITÉ ABSOLUE**
  - Règle la plus récente pour eBooks en anglais
  - Formats acceptés : EPUB, PDF, MOBI, AZW, AZW3, CBZ
  - Structure NFO standardisée
  - Contraintes de nommage strictes
  - **URL** : `https://scenerules.org/nfo/2022_eBOOK.nfo` (à vérifier exactement)

#### Ye Olde English Rules
- **[2012] eBOOK** [p/t/n/d]
  - Version précédente (référence historique)
  - Peut être utilisée pour compatibilité

### Autres Scènes

#### German
- **[2002] EBOOK** [p/t/n/d]
- **[2004] EBOOK3** [p/t/n/d]
- **[2009] EBOOK** [p/t/n/d]

#### Polish
- **[2006] EBOOK** [p/t/n/d]

**Note** : D'autres scènes peuvent avoir des règles EBOOK (French, Spanish, etc.) - voir [scenerules.org](https://scenerules.org/) pour liste complète.

---

## 🔍 Structure scenerules.org

### Organisation des Règles

Les règles sont organisées par :
1. **Scène** : English, German, French, Polish, Spanish, Swedish, Hungarian, Italian, Lithuanian, etc.
2. **Section** : eBOOK, TV-720p, TV-SD, X264, X265, FLAC, MP3, etc.
3. **Année** : Année de publication/mise à jour de la règle

### Format des Règles

Chaque règle est disponible en format **NFO** (.nfo) contenant :
- Spécifications complètes de nommage
- Formats de fichiers acceptés
- Structure du release packagé
- Template NFO standardisé
- Contraintes techniques (taille, qualité, etc.)
- Règles de validation

### Indicateurs Règles

Les règles ont des indicateurs :
- **[p/t/n/d]** : picture/text/numbered/download
- **[m/e]** : mirror/extras
- **[1-9]** : Statut spécial (Fake, Draft, Addendum, etc.)

---

## 🎯 Intégration dans le Processus de Packaging

### Étape Critique : Chargement et Analyse de la Règle

**Avant tout packaging EBOOK**, le système doit :

1. **Télécharger la règle eBOOK [2022]** depuis scenerules.org
   - URL à déterminer : `https://scenerules.org/nfo/2022_eBOOK.nfo` ou structure similaire
   - Format : Fichier NFO texte (ASCII)
   - Mise en cache locale après téléchargement

2. **Parser la règle complète**
   - Extraire tous les formats acceptés (EPUB, PDF, MOBI, etc.)
   - Extraire structure nommage complète
   - Extraire template NFO standardisé
   - Extraire toutes les contraintes (taille, structure, fichiers requis)
   - Extraire règles de validation

3. **Valider contre la règle à chaque étape**
   - **Étape 4** : Format fichier source conforme ?
   - **Étape 7** : Template NFO conforme ?
   - **Étape 8** : Structure release conforme ?
   - **Packaging** : Nommage conforme ?
   - **Final** : Toutes contraintes respectées ?

4. **Appliquer la règle strictement**
   - Générer NFO selon template de la règle
   - Créer structure release selon spécifications
   - Nommer fichiers selon règles strictes
   - Valider final contre toutes exigences

---

## 📝 Exigences Techniques

### Parser de Règle

**Service Critique** : `RuleParserService`

```python
class RuleParserService:
    """Parse et valide les règles scenerules.org."""
    
    def download_ebook_rule_2022(self) -> str:
        """Télécharge règle eBOOK [2022] depuis scenerules.org."""
        # Téléchargement depuis https://scenerules.org/
        # Mise en cache locale
        # Retourne contenu NFO brut
        pass
    
    def parse_ebook_rule_2022(self, content: str) -> EbookRuleSpec:
        """Parse règle eBOOK [2022] complète."""
        spec = EbookRuleSpec()
        
        # Extraction formats acceptés
        spec.accepted_formats = ['EPUB', 'PDF', 'MOBI', 'AZW', 'AZW3', 'CBZ']
        
        # Extraction template NFO
        spec.nfo_template = extract_template(content)
        
        # Extraction contraintes nommage
        spec.naming_pattern = extract_naming_pattern(content)
        
        # Extraction structure release
        spec.release_structure = extract_structure(content)
        
        # Extraction validations
        spec.validations = extract_validations(content)
        
        return spec
    
    def validate_against_rule(
        self, 
        release_data: dict, 
        rule_spec: EbookRuleSpec
    ) -> tuple[bool, list[str]]:
        """Valide release contre règle complète."""
        errors = []
        
        # Validation format fichier
        if release_data['file_format'] not in rule_spec.accepted_formats:
            errors.append(f"Format {release_data['file_format']} non accepté")
        
        # Validation nommage
        if not rule_spec.naming_pattern.match(release_data['release_name']):
            errors.append("Nommage non conforme à la règle")
        
        # Validation structure
        if not validate_structure(release_data, rule_spec.release_structure):
            errors.append("Structure release non conforme")
        
        # Validation NFO
        if not validate_nfo(release_data['nfo'], rule_spec.nfo_template):
            errors.append("NFO non conforme au template de la règle")
        
        return len(errors) == 0, errors
```

### Structure EbookRuleSpec

```python
@dataclass
class EbookRuleSpec:
    """Spécification complète règle eBOOK [2022]."""
    accepted_formats: list[str]  # EPUB, PDF, MOBI, etc.
    nfo_template: str  # Template NFO complet
    naming_pattern: re.Pattern  # Regex nommage
    release_structure: dict  # Structure fichiers requis
    validations: list[Callable]  # Fonctions validation
    constraints: dict  # Contraintes (taille, qualité, etc.)
```

### Validation Stricte

**Toutes validations basées sur la règle** :

1. **Format fichier source**
   - ✅ Format accepté selon règle ?
   - ✅ Extension conforme ?
   - ✅ Taille conforme (si spécifié dans règle) ?

2. **Nommage**
   - ✅ Format nom release conforme ?
   - ✅ Groupe conforme ?
   - ✅ Titre conforme ?
   - ✅ Pattern complet respecté ?

3. **Structure release**
   - ✅ Fichiers requis présents ?
   - ✅ Fichiers optionnels corrects ?
   - ✅ Structure arborescence conforme ?
   - ✅ Tous fichiers selon spécifications règle ?

4. **NFO**
   - ✅ Template respecté ?
   - ✅ Tous champs requis présents ?
   - ✅ Format ASCII conforme (largeur ≤ 80 colonnes) ?
   - ✅ Placeholders correctement remplacés ?

---

## 🔄 Processus Complet EBOOK

### 1. Étape 3 : Sélection Règle ⚠️ CRITIQUE
- **Obligatoire** : Règle eBOOK [2022] English (ou autre selon scène)
- **Source** : scenerules.org (téléchargement automatique si pas locale)
- **Validation** : Règle complète chargée et parsée
- **Stockage** : `EbookRuleSpec` complète stockée pour validations suivantes

### 2. Étape 4 : Sélection Fichier
- **Validation** : Format fichier conforme à règle eBOOK [2022]
- **Formats acceptés** : Selon règle (EPUB, PDF, MOBI, AZW, AZW3, CBZ)
- **Validation règle** : Vérification contre `rule_spec.accepted_formats`

### 3. Étape 7 : Templates NFO ⚠️ CRITIQUE
- **Template source** : Template de la règle eBOOK [2022]
- **Application** : Tous placeholders remplis selon métadonnées
- **Validation** : Format ASCII, largeur ≤ 80 colonnes (selon règle)
- **Conformité** : Template conforme à structure règle

### 4. Étape 8 : Options/Paramètres ⚠️ CRITIQUE
- **Validation** : Toutes options conformes à règle
- **Contraintes** : Taille, qualité, structure selon règle
- **Validation finale** : Release conforme à TOUTES exigences règle
- **Indicateur** : Badge "Conforme règle eBOOK [2022]" si OK

### 5. Packaging Final ⚠️ CRITIQUE
- **Validation finale** : Release conforme à TOUTES exigences règle
- **NFO généré** : Selon template règle (injecté métadonnées)
- **Structure** : Selon spécifications règle
- **Nommage** : Conforme règles strictes règle
- **Validation complète** : Toutes validations `RuleValidationService` passent

---

## 🚨 Points Critiques

### 1. Règle eBOOK [2022] Prioritaire
- ✅ **TOUJOURS** utiliser règle [2022] eBOOK pour packaging nouveau
- ✅ Règle [2012] seulement pour compatibilité historique
- ✅ Autres scènes (German, Polish) selon besoin utilisateur

### 2. Conformité Absolue
- ❌ **JAMAIS** packager sans règle chargée
- ❌ **JAMAIS** ignorer contraintes règle
- ❌ **JAMAIS** créer release non conforme
- ✅ **TOUJOURS** valider contre règle complète
- ✅ **TOUJOURS** utiliser template de la règle pour NFO

### 3. Mise à Jour Règles
- ✅ Synchronisation périodique scenerules.org
- ✅ Détection nouvelles versions règles
- ✅ Notification si règle obsolète
- ✅ Cache local avec vérification mise à jour

---

## 📚 Références

- **Site officiel** : [scenerules.org](https://scenerules.org/)
- **Règle eBOOK actuelle** : [2022] eBOOK (English) ⭐
- **Dernière mise à jour** : 2024-04-23 (selon scenerules.org)
- **Format** : NFO (.nfo) - ASCII, largeur ≤ 80 colonnes

---

## ✅ Checklist Intégration

### Avant Phase 3 (Wizard)
- [ ] Service `RuleParserService` créé
- [ ] Service `RuleValidationService` créé
- [ ] Service `ScenerulesDownloadService` créé
- [ ] Parser règle eBOOK [2022] implémenté
- [ ] Téléchargement scenerules.org fonctionnel
- [ ] Validation contre règle complète
- [ ] Tests avec règle réelle eBOOK [2022]
- [ ] Documentation intégration complète

### Avant Packaging EBOOK
- [ ] Règle eBOOK [2022] chargée et parsée
- [ ] Toutes contraintes règle extraites
- [ ] Template NFO de règle extrait
- [ ] Validation complète implémentée
- [ ] Structure `EbookRuleSpec` complète
- [ ] Tests validation contre règle réelle

### Pendant Développement
- [ ] Télécharger règle eBOOK [2022] depuis scenerules.org
- [ ] Analyser structure règle complète
- [ ] Identifier tous formats acceptés
- [ ] Identifier template NFO
- [ ] Identifier toutes contraintes
- [ ] Implémenter parser complet
- [ ] Implémenter validations complètes

---

## 🔧 Implémentation Recommandée

### 1. Phase 1 : Services Backend

**Créer en Phase 1.4 ou Phase 1.5** :

```python
# web/services/scenerules_download.py
class ScenerulesDownloadService:
    """Télécharge règles depuis scenerules.org."""
    BASE_URL = "https://scenerules.org"
    
    def download_ebook_2022(self) -> str:
        """Télécharge règle eBOOK [2022]."""
        # Implémentation scraping/fetch
        pass

# web/services/rule_parser.py
class RuleParserService:
    """Parse règles scenerules.org."""
    
    def parse_ebook_2022(self, content: str) -> EbookRuleSpec:
        """Parse règle eBOOK [2022] complète."""
        # Extraction formats, template, contraintes
        pass

# web/services/rule_validation.py
class RuleValidationService:
    """Valide releases contre règles."""
    
    def validate_ebook(self, release_data: dict, rule_spec: EbookRuleSpec) -> tuple[bool, list[str]]:
        """Valide release EBOOK contre règle."""
        # Validations complètes
        pass
```

### 2. Phase 3 : Intégration Wizard

**Étape 3** : Charger et parser règle eBOOK [2022]  
**Étape 7** : Utiliser template règle pour NFO  
**Étape 8** : Valider contre règle complète  
**Packaging** : Appliquer règle strictement

---

**CRITIQUE** : Ce document doit être consulté avant tout développement de packaging EBOOK.

**Rappel** : Connaissance TOTALE et INTÉGRALE des règles scenerules.org est OBLIGATOIRE pour packaging EBOOK conforme.

**Référence complète** : [scenerules.org](https://scenerules.org/)
