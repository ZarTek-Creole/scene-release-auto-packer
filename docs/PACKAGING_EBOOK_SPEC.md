# 📦 Spécification Packaging EBOOK - Conformité Règle [2022]

**Date** : 2025-11-01  
**Source** : Règle eBOOK [2022] de [scenerules.org](https://scenerules.org/)  
**Référence** : `docs/EBOOK_RULES_2022_COMPLETE.md`

---

## ⚠️ RÈGLE ABSOLUE

**Le packaging EBOOK DOIT respecter STRICTEMENT la règle eBOOK [2022] complète.**

Toutes les étapes du processus DOIVENT valider contre cette règle.

---

## 📋 Processus de Packaging EBOOK - Conformité Règle

### Étape Préalable : Chargement Règle

**AVANT toute étape packaging** :

1. **Télécharger règle eBOOK [2022]**
   - URL : `https://scenerules.org/html/2022_EBOOK.html`
   - Format : HTML (ou NFO si disponible)
   - Cache : Stockage local avec vérification mise à jour

2. **Parser règle complète**
   - Extraire Section 2.6 : Formats acceptés
   - Extraire Section 3 : Packaging rules
   - Extraire Section 4 : NFO requirements
   - Extraire Section 5 : Dirnaming rules
   - Créer `EbookRuleSpec` complète

3. **Valider règle chargée**
   - Vérifier toutes sections présentes
   - Vérifier formats acceptés extraits
   - Vérifier contraintes packaging extraites

---

### Étape 4 : Validation Fichier Source

**Selon Section 2.6 (OTHER)** :

✅ **Formats acceptés** :
- PDF
- EPUB
- CBZ
- AZW (Kindle)
- KF8 (Kindle)
- PRC (MOBIPOCKET)
- MOBI (MOBIPOCKET)

❌ **Formats INTERDITS** :
- Conversions (epub→pdf, etc.)
- Free from web (sauf internal)
- Formats non listés

**Validation** :
```python
def validate_ebook_file(file_path: Path, rule_spec: EbookRuleSpec) -> tuple[bool, list[str]]:
    """Valide fichier source contre règle eBOOK [2022]."""
    errors = []
    
    # Vérifier extension
    ext = file_path.suffix.upper().lstrip('.')
    if ext not in rule_spec.accepted_formats:
        errors.append(f"Format {ext} non accepté. Formats acceptés: {', '.join(rule_spec.accepted_formats)}")
    
    # Détecter DRM/Watermark (Section 2.4)
    if detect_drm(file_path):
        errors.append("Fichier protégé DRM détecté. DRM doit être retiré avant packaging.")
    
    if detect_watermark(file_path):
        errors.append("Watermark détecté. Watermark doit être retiré avant packaging.")
    
    return len(errors) == 0, errors
```

---

### Étape 5 : Analyse et Extraction Métadonnées

**Selon Section 4.1 (NFO-FILE)** :

**Métadonnées MANDATOIRES à extraire** :
1. ✅ **Release Date** : Format ISO YYYY-MM-DD
2. ✅ **Publish Date** : Format ISO YYYY-MM-DD ou YYYY
3. ✅ **Language** : (German/Swedish/French/...)
4. ✅ **Release Type** : RETAiL/SCAN/HYBRiD
5. ✅ **Author/Publisher** : Au moins un des deux
6. ✅ **Issue/Volume** : Si applicable
7. ✅ **Source link** : Si RETAiL (proof URL retailer)

**Métadonnées OPTIONNELLES (fortement recommandées)** :
- Disks (nombre et taille)
- Size (taille totale release)
- ISBN/ISSN
- Genre
- Store date
- URL/Shop link

**Extraction** :
```python
def extract_mandatory_metadata(file_path: Path, rule_spec: EbookRuleSpec) -> dict:
    """Extrait métadonnées mandataires pour NFO."""
    metadata = {}
    
    # Extraction depuis fichier
    metadata['release_date'] = extract_release_date(file_path)  # ISO YYYY-MM-DD
    metadata['publish_date'] = extract_publish_date(file_path)  # ISO YYYY-MM-DD ou YYYY
    metadata['language'] = extract_language(file_path)
    metadata['release_type'] = determine_release_type(file_path)  # SCAN/HYBRiD/RETAiL
    metadata['author'] = extract_author(file_path)
    metadata['publisher'] = extract_publisher(file_path)
    metadata['issue_or_volume'] = extract_issue_volume(file_path)
    
    # Si RETAiL : Source link obligatoire
    if metadata['release_type'] == 'RETAiL':
        metadata['source_link'] = extract_proof_url(file_path)  # OBLIGATOIRE
    
    return metadata
```

---

### Étape 7 : Génération Templates NFO/DIZ

**Selon Section 4.1 (NFO-FILE) et Section 2.5 (NFO & DiZ)** :

**NFO Requirements** :
- ✅ Largeur maximale : **80 caractères**
- ✅ Toutes informations mandataires présentes
- ✅ Release names peuvent être split pour respecter 80 chars
- ✅ Proof URL peut être split (ou utiliser URL principale shop)

**DIZ Requirements** :
- ✅ **Fichier .diz OBLIGATOIRE**
- ✅ Nombre de disques : `DISK: [xx/??]`
- ✅ Largeur maximale : **44 caractères**
- ✅ Hauteur maximale : **30 lignes**

**Génération** :
```python
def generate_nfo_file(metadata: dict, rule_spec: EbookRuleSpec) -> str:
    """Génère fichier NFO conforme Section 4.1."""
    nfo_lines = []
    
    # Header ASCII art (optionnel mais standard)
    nfo_lines.append("─" * 80)
    nfo_lines.append(f"{'Release Info':^80}")
    nfo_lines.append("─" * 80)
    
    # Informations mandataires (Section 4.1)
    for field in rule_spec.nfo_mandatory_fields:
        value = metadata.get(field)
        if value:
            # Format : "Field: Value" (max 80 chars)
            line = f"{field}: {value}"
            if len(line) > 80:
                # Split si nécessaire (Section 2.5)
                line = split_line_80_chars(line)
            nfo_lines.append(line)
    
    # Informations optionnelles
    for field in rule_spec.nfo_optional_fields:
        value = metadata.get(field)
        if value:
            line = f"{field}: {value}"
            if len(line) > 80:
                line = split_line_80_chars(line)
            nfo_lines.append(line)
    
    # Validation largeur
    for line in nfo_lines:
        assert len(line) <= 80, f"NFO line exceeds 80 chars: {line[:50]}..."
    
    return "\n".join(nfo_lines)

def generate_diz_file(disk_count: int, total_size_mb: float) -> str:
    """Génère fichier DIZ conforme Section 2.5."""
    diz_lines = []
    
    # DISK: [xx/??] format
    diz_lines.append(f"DISK: [{disk_count:02d}/??]")
    diz_lines.append("")
    diz_lines.append(f"Size: {total_size_mb:.2f} MB")
    
    # Validation dimensions
    assert all(len(line) <= 44 for line in diz_lines), "DIZ width exceeds 44 chars"
    assert len(diz_lines) <= 30, "DIZ height exceeds 30 lines"
    
    return "\n".join(diz_lines)
```

---

### Étape 8 : Options Packaging

**Selon Section 3 (PACKAGiNG)** :

**Validation ZIP Size** :
```python
def validate_zip_size(size_bytes: int, rule_spec: EbookRuleSpec) -> tuple[bool, str]:
    """Valide taille ZIP contre Section 3.1."""
    allowed_sizes = rule_spec.zip_allowed_sizes
    if size_bytes not in allowed_sizes:
        return False, f"Taille ZIP {size_bytes} non autorisée. Tailles autorisées: {', '.join(map(str, allowed_sizes))}"
    return True, ""
```

**Contraintes Packaging** :
- ✅ ZIP+DIZ structure
- ✅ .nfo dans ZIP archives
- ✅ ZIP filename unique (pas de dupes dans l'année)
- ✅ ZIP volume filenames max **8.3 caractères**
- ⚠️ NFO exempt de règle 8.3
- ✅ RAR archives **à l'intérieur** ZIP volumes
- ❌ Espaces interdits dans filenames (rar/zip/diz/nfo)
- ✅ Dirname max **243 caractères**
- ✅ Archive filename max **140 caractères**
- ❌ Nombre fichiers max **99**

---

### Packaging Final : Génération Release

**Selon Section 5 (DiRNAMiNG)** :

**Structure Dirnaming selon Type** :

#### Magazines (Section 5.1)
```
{Name}.{Issue}.{Year}.{Language}.{Source}.MAGAZiNE.eBOOK-{GROUP}
```

#### Comics (Section 5.2)
```
{Name}.Vol.{Volume}.No.{Issue}.{Date}.{Language}.{Source}.COMiC.eBOOK-{GROUP}
```

#### Manga (Section 5.3)
```
{Name}.Vol.{Volume}.{Language}.{Source}.MANGA.eBOOK-{GROUP}
```

#### Books Fictional (Section 5.4)
```
{Author}.{Title}.{Edition}.{Year}.{Language}.{Source}.eBOOK-{GROUP}
```

#### Books Technical (Section 5.5)
```
{Publisher}.{Title}.{Year}.{Language}.{Source}.eBOOK-{GROUP}
```

#### Newspapers (Section 5.6)
```
{Name}.{Date}.{Year}.{Language}.{Source}.eBOOK-{GROUP}
```

#### XXX Books (Section 5.7)
```
{Title}.{Year}.{Source}.XXX.eBOOK-{GROUP}
```

**Règles Globales Dirnaming** :
- ✅ Grouptag obligatoire
- ✅ Year tag obligatoire
- ⚠️ Language tag : Uniquement si non-English
- ✅ Source tag obligatoire (SCAN/HYBRiD/RETAiL)
- ⚠️ Format tag si non-PDF : ePUB, CBZ, KF8, AZW, MOBI, PRC
- ✅ Dirname max 243 caractères (raccourcir si nécessaire, titre complet dans .nfo)

**Génération Dirname** :
```python
def generate_ebook_dirname(
    metadata: dict,
    release_type: str,  # 'magazine', 'comic', 'manga', 'book_fictional', 'book_technical', 'newspaper', 'xxx'
    group: str,
    rule_spec: EbookRuleSpec
) -> str:
    """Génère dirname conforme Section 5."""
    parts = []
    
    if release_type == 'magazine':
        # Section 5.1
        parts.append(metadata['name'])
        parts.append(metadata.get('issue', ''))  # No.1, NR03, etc.
        parts.append(metadata['year'])
        if metadata['language'] != 'English':
            parts.append(metadata['language'])
        parts.append(metadata['source'])  # RETAiL/SCAN/HYBRiD
        parts.append('MAGAZiNE')
        if metadata['format'] != 'PDF':
            parts.append(metadata['format'])  # ePUB, CBZ, etc.
        parts.append('eBOOK')
    # ... autres types ...
    
    dirname = '.'.join(parts) + f"-{group}"
    
    # Validation longueur
    if len(dirname) > 243:
        # Raccourcir intelligemment, titre complet dans .nfo
        dirname = shorten_dirname(dirname, 243)
    
    return dirname
```

---

## 🔧 Services Backend Requis

### ScenerulesDownloadService

```python
class ScenerulesDownloadService:
    """Télécharge règles depuis scenerules.org."""
    
    BASE_URL = "https://scenerules.org"
    CACHE_DIR = Path("rules_cache")
    
    def download_ebook_2022(self) -> str:
        """Télécharge règle eBOOK [2022] HTML."""
        url = f"{self.BASE_URL}/html/2022_EBOOK.html"
        # Téléchargement avec cache
        # Retourne contenu HTML complet
        pass
    
    def download_ebook_2022_nfo(self) -> str:
        """Télécharge règle eBOOK [2022] NFO."""
        url = f"{self.BASE_URL}/nfo/2022_EBOOK.nfo"
        # Téléchargement avec cache
        # Retourne contenu NFO ASCII
        pass
```

### RuleParserService

```python
class RuleParserService:
    """Parse règles scenerules.org complètes."""
    
    def parse_ebook_2022(self, html_content: str) -> EbookRuleSpec:
        """Parse règle eBOOK [2022] complète."""
        spec = EbookRuleSpec()
        
        # Section 2.6 : Formats acceptés
        spec.accepted_formats = ['PDF', 'EPUB', 'CBZ', 'AZW', 'KF8', 'PRC', 'MOBI']
        
        # Section 3.1 : Tailles ZIP autorisées
        spec.zip_allowed_sizes = [
            5_000_000, 10_000_000, 50_000_000, 100_000_000,
            150_000_000, 200_000_000, 250_000_000
        ]
        
        # Section 3.0 : Packaging rules
        spec.packaging = {
            'use_zip_diz': True,
            'nfo_required': True,
            'zip_filename_unique': True,
            'zip_volume_max_83_chars': True,
            'nfo_exempt_83_rule': True,
            'rar_inside_zip': True,
            'no_spaces_filenames': True,
            'dirname_max_chars': 243,
            'archive_filename_max_chars': 140,
            'max_files_per_zip': 99
        }
        
        # Section 4.1 : NFO mandatory fields
        spec.nfo_mandatory = [
            'release_date', 'publish_date', 'language',
            'release_type', 'author_or_publisher', 'issue_or_volume',
            'source_link'  # Si retail
        ]
        
        # Section 5 : Dirnaming rules
        spec.dirnaming = {
            'grouptag_required': True,
            'year_tag_required': True,
            'language_tag_non_english_only': True,
            'source_tag_required': True,
            'format_tag_if_not_pdf': True
        }
        
        # Sections complètes stockées
        spec.full_rule_sections = {
            'section_2': extract_section_2(html_content),
            'section_3': extract_section_3(html_content),
            'section_4': extract_section_4(html_content),
            'section_5': extract_section_5(html_content),
            'section_6': extract_section_6(html_content),
            'section_7': extract_section_7(html_content),
        }
        
        return spec
```

### RuleValidationService

```python
class RuleValidationService:
    """Valide releases contre règles eBOOK [2022]."""
    
    def validate_ebook_format(
        self, 
        file_path: Path, 
        rule_spec: EbookRuleSpec
    ) -> tuple[bool, list[str]]:
        """Valide format fichier contre Section 2.6."""
        errors = []
        ext = file_path.suffix.upper().lstrip('.')
        
        if ext not in rule_spec.accepted_formats:
            errors.append(
                f"Format {ext} non accepté. "
                f"Formats acceptés: {', '.join(rule_spec.accepted_formats)}"
            )
        
        return len(errors) == 0, errors
    
    def validate_ebook_packaging(
        self,
        zip_structure: dict,
        rule_spec: EbookRuleSpec
    ) -> tuple[bool, list[str]]:
        """Valide structure packaging contre Section 3."""
        errors = []
        
        # Vérifier taille ZIP
        if zip_structure['size'] not in rule_spec.zip_allowed_sizes:
            errors.append(
                f"Taille ZIP {zip_structure['size']} non autorisée. "
                f"Tailles autorisées: {rule_spec.zip_allowed_sizes}"
            )
        
        # Vérifier nombre fichiers
        if zip_structure['file_count'] > rule_spec.packaging['max_files_per_zip']:
            errors.append(
                f"Nombre fichiers {zip_structure['file_count']} > "
                f"{rule_spec.packaging['max_files_per_zip']}"
            )
        
        # Vérifier .nfo présent
        if not zip_structure.get('has_nfo'):
            errors.append(".nfo file obligatoire dans ZIP (Section 3.0)")
        
        # Vérifier .diz présent
        if not zip_structure.get('has_diz'):
            errors.append(".diz file obligatoire (Section 2.5)")
        
        # Vérifier SFV absent
        if zip_structure.get('has_sfv'):
            errors.append("SFV interdit dans ZIP archive (Section 3.1)")
        
        return len(errors) == 0, errors
    
    def validate_ebook_nfo(
        self,
        nfo_content: str,
        rule_spec: EbookRuleSpec
    ) -> tuple[bool, list[str]]:
        """Valide NFO contre Section 4.1."""
        errors = []
        
        # Vérifier largeur ≤ 80
        lines = nfo_content.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 80:
                errors.append(f"Ligne {i} NFO dépasse 80 caractères: {len(line)} chars")
        
        # Vérifier informations mandataires
        for field in rule_spec.nfo_mandatory:
            if field not in nfo_content.lower():
                errors.append(f"Information mandataire manquante: {field}")
        
        return len(errors) == 0, errors
    
    def validate_ebook_dirname(
        self,
        dirname: str,
        release_type: str,
        rule_spec: EbookRuleSpec
    ) -> tuple[bool, list[str]]:
        """Valide dirname contre Section 5."""
        errors = []
        
        # Vérifier longueur max
        if len(dirname) > rule_spec.dirnaming['dirname_max_chars']:
            errors.append(
                f"Dirname {len(dirname)} chars > "
                f"{rule_spec.dirnaming['dirname_max_chars']} max"
            )
        
        # Vérifier grouptag présent
        if not re.search(r'-[A-Z0-9]+$', dirname):
            errors.append("Grouptag obligatoire dans dirname (Section 5.0)")
        
        # Vérifier year tag
        if not re.search(r'\.\d{4}\.', dirname):
            errors.append("Year tag obligatoire dans dirname (Section 5.0)")
        
        # Vérifier source tag
        if not re.search(r'\.(SCAN|HYBRiD|RETAiL)\.', dirname):
            errors.append("Source tag obligatoire (SCAN/HYBRiD/RETAiL) (Section 5.0)")
        
        return len(errors) == 0, errors
```

---

## ✅ Checklist Validation Complète

### Avant Packaging

- [ ] Règle eBOOK [2022] téléchargée depuis scenerules.org
- [ ] Règle parsée complètement (`EbookRuleSpec` complète)
- [ ] Toutes sections extraites (2, 3, 4, 5, 6, 7)

### Étape 4 : Fichier

- [ ] Format fichier dans `accepted_formats` (PDF, EPUB, CBZ, AZW, KF8, PRC, MOBI)
- [ ] DRM détecté → ERREUR (Section 2.4)
- [ ] Watermark détecté → ERREUR (Section 2.4)
- [ ] Pas de conversion (epub→pdf, etc.) → ERREUR si détecté

### Étape 7 : Templates

- [ ] NFO contient toutes informations mandataires (Section 4.1)
- [ ] NFO width ≤ 80 caractères toutes lignes
- [ ] DIZ file généré (DISK: [xx/??], max 44x30)
- [ ] Proof URL si RETAiL (Section 2.2)

### Étape 8 : Packaging

- [ ] ZIP size dans liste autorisée (7 tailles seulement)
- [ ] Nombre fichiers ≤ 99
- [ ] .nfo dans ZIP archives
- [ ] .diz dans ZIP archives
- [ ] Pas de SFV dans ZIP
- [ ] Structure ZIP+DIZ respectée
- [ ] Filenames conformes (8.3 pour volumes, max 140 pour archive)
- [ ] Pas d'espaces dans filenames (rar/zip/diz/nfo)

### Packaging Final

- [ ] Dirname conforme Section 5 (selon type)
- [ ] Grouptag présent
- [ ] Year tag présent
- [ ] Source tag présent (SCAN/HYBRiD/RETAiL)
- [ ] Format tag si non-PDF
- [ ] Dirname ≤ 243 caractères
- [ ] Validation finale complète passée

---

## 📚 Références

- **Règle complète** : `docs/EBOOK_RULES_2022_COMPLETE.md`
- **Intégration scenerules.org** : `docs/SCENERULES_INTEGRATION.md`
- **Source** : [scenerules.org](https://scenerules.org/)
- **URL règle** : `https://scenerules.org/html/2022_EBOOK.html`

---

**Document créé le** : 2025-11-01  
**Statut** : ✅ **COMPLET - PRÊT POUR IMPLÉMENTATION**

