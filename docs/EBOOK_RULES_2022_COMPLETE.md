# 📚 Règle eBOOK [2022] - Document Complet et Intégration

**Date** : 2025-11-01  
**Source** : [scenerules.org](https://scenerules.org/)  
**Règle** : [2022] eBOOK (English) - **VERSION ACTUELLE** ⭐  
**URL** : `https://scenerules.org/html/2022_EBOOK.html`  
**Format NFO** : `https://scenerules.org/nfo/2022_EBOOK.nfo`

---

## ⚠️ EXIGENCE ABSOLUE

**Pour packager des EBOOK, connaissance TOTALE et INTÉGRALE de cette règle est OBLIGATOIRE.**

Cette règle DOIT être :
1. ✅ **Chargée** depuis scenerules.org avant tout packaging
2. ✅ **Parsée** complètement (toutes sections extraites)
3. ✅ **Validée** à chaque étape du packaging
4. ✅ **Appliquée** strictement (aucune exception)

---

## 📋 Règle eBOOK [2022] - Contenu Complet

### Structure de la Règle

La règle eBOOK [2022] contient **8 sections principales** :

1. **INTRODUCTiON & NOTES**
2. **TECHNiCAL DETAiLS** (7 sous-sections)
3. **PACKAGiNG** (2 sous-sections)
4. **NFO-FiLE** (1 sous-section)
5. **DiRNAMiNG** (8 sous-sections)
6. **DUPES/PROPER** (2 sous-sections)
7. **MiSCELLANEOUS** (2 sous-sections)
8. **SiGN** (2 sous-sections)

---

## 🎯 Section 2 : TECHNiCAL DETAiLS - Spécifications Critiques

### 2.1 SCANS

**Contraintes** :
- ✅ Résolution minimum : **96dpi** (mais doit être lisible)
- ❌ Pages endommagées/sales : **INTERDITES**
- ✅ Recadrage : Autorisé si nécessaire
- ✅ Contenu complet : **Tout le magazine/livre** doit être scanné
- ⚠️ Publicités : Optionnelles (peuvent être retirées)
  - Si retirées : Remplacer par pages blanches/noires pour maintenir ordre
- ✅ Downscaling : Autorisé (minimum résolution = **1600x***)
- ❌ Upscaling : **INTERDIT**
- ✅ Photographies qualité : Autorisées comme scans
- ✅ Format : **.PDF obligatoire**

### 2.2 RETAiL

**Contraintes** :
- ✅ **PROOF URL OBLIGATOIRE** : Au moins une URL de preuve d'un retailer
  - URL doit prouver que l'item est disponible en format released
  - Utilisation d'une preuve URL différente de la source réelle autorisée
- ⚠️ Modifications : Retail files ne doivent **PAS être modifiés** (sauf absolument nécessaire)
  - Exceptions : Retrait watermarks/métadonnées identifiants
- ✅ PDF pages fusionnées : Autorisé si source fournit pages séparées

### 2.3 HYBRiD

**Définition** : Toute source autre que retail ou scan
- Virtual printers
- Screen captures
- Fichiers extraits formats DRM-protégés
- Fichiers dumpés depuis attaques réseau
- etc.

### 2.4 DRM/Watermark

**Règles strictes** :
- ❌ Documents protégés DRM/Watermark : **INTERDITS** (doivent être retirés)
- ❌ Watermarking groupe : **INTERDIT**

### 2.5 NFO & DiZ

**NFO** :
- ✅ Largeur maximale : **80 caractères**
- ✅ Release names : Peuvent être split pour respecter 80 chars
- ✅ Proof URL : Peut être split (ou utiliser URL principale du shop)

**DiZ** :
- ✅ **Fichier .diz OBLIGATOIRE**
- ✅ Nombre de disques : `DISK: [xx/??]`
- ✅ Largeur maximale : **44 caractères**
- ✅ Hauteur maximale : **30 lignes**

**Note importante** : Les dimensions diz/nfo sont des recommandations historiques, mais ne pas les respecter ne doit pas être grounds for nuke.

### 2.6 OTHER

**Formats acceptés** : ⭐ **CRITIQUE**
- ✅ **PDF**
- ✅ **EPUB**
- ✅ **CBZ**
- ✅ **Kindle** : `.azw`, `.kf8`
- ✅ **MOBIPOCKET** : `.prc`, `.mobi`

**Règles strictes** :
- ❌ Free from web : **INTERDIT** (sauf internal releases pour préserver contenu free qui n'est plus disponible)
- ❌ Conversions : **INTERDITES** (ex: epub → pdf interdit)
- ✅ Extras encouragés : Archives séparées (e.g. `book.pdf + bonus.zip`)
  - ⚠️ Attention : Ne pas inclure dupes extras (ex: musique déjà released en MP3/FLAC)

---

## 📦 Section 3 : PACKAGiNG - Règles Critiques

### 3.0 GLOBAL PACKAGiNG RULES

**Règles absolues** :
- ✅ **ZIP+DIZ obligatoire**
- ✅ **.nfo file obligatoire** dans tous les cas
- ✅ ZIP filename : **Unique** (pas de dupes dans l'année)
- ✅ ZIP volume filenames : **Max 8.3 caractères**
- ⚠️ 8.3 rule : **N'APPLIQUE PAS** au .nfo
- ✅ RAR archives : **À l'intérieur ZIP volumes**
- ❌ Espaces : **INTERDITS** dans filenames (rar/zip/diz/nfo)
  - ✅ Extras dans leur propre archive : Espaces autorisés
- ✅ Dirname maximum : **243 caractères**
- ✅ Ebook/extras archive filename max : **140 caractères**

### 3.1 ZiP ARCHiVES

**Tailles autorisées** : ⭐ **CRITIQUE**
- ✅ **5.000.000 bytes** (5MB)
- ✅ **10.000.000 bytes** (10MB)
- ✅ **50.000.000 bytes** (50MB)
- ✅ **100.000.000 bytes** (100MB)
- ✅ **150.000.000 bytes** (150MB)
- ✅ **200.000.000 bytes** (200MB)
- ✅ **250.000.000 bytes** (250MB)

**Règles** :
- ✅ Compression RAR : Autorisée et optionnelle
- ❌ Nombre de fichiers : **Maximum 99 fichiers**
- ✅ .nfo et .diz : **DOIVENT être dans ZIP archives**
- ❌ SFV : **INTERDIT dans ZIP archive**

---

## 📄 Section 4 : NFO-FiLE - Contenu Obligatoire

### 4.1 CONTENT

**Informations MANDATOIRES** (doivent être dans .nfo) :
- ✅ **Release Date** : Format ISO YYYY-MM-DD
- ✅ **Publish Date** : Format ISO YYYY-MM-DD ou au moins YYYY
  - ⚠️ Note : Dates dans .nfo sont purement informatives (ne pas nuker si incorrectes)
- ✅ **Language** : (German/Swedish/French/...)
- ✅ **Release Type** : (RETAiL/SCAN/HYBRiD)
- ✅ **Author/Publisher** : Au moins un des deux
- ✅ **Issue/Volume** : Numéro d'issue Magazine ou mois édition
- ✅ **Source link** : Pour prouver disponibilité retail d'une release retail dans le format released

**Exception** : Si l'information est dans le dirname de la release, elle peut être omise du .nfo.

**Informations OPTIONNELLES** (fortement recommandées) :
- ⚠️ **Disks** : Nombre et taille (e.g. "20 x 5mb")
- ⚠️ **Size** : Taille totale release en megabytes
- ⚠️ **ISBN/ISSN** : Si disponible
- ⚠️ **Genre** : (Science-Fiction/Music/Sports/Comic/Manga/...)
  - ⚠️ Note : Genres appropriés aident à trier releases
- ⚠️ **Store date** : Date disponibilité release en format ISO YYYY-MM-DD
- ⚠️ **URL/Shop link** : URL vers site où information disponible
  - ⚠️ Note : Proof URL retail reste obligatoire pour releases retail

---

## 🏷️ Section 5 : DiRNAMiNG - Règles de Nommage

### 5.0 GLOBAL DiRNAMiNG RULES

**Règles absolues** :
- ✅ **Grouptag obligatoire** : Toujours ajouter votre grouptag
- ⚠️ Titre > 243 chars : Raccourcir au mieux, titre complet dans .nfo
- ✅ **Year tag obligatoire** : Utiliser meilleur jugement (copyright/publish/print year)
- ⚠️ Language tag : **Uniquement pour releases non-English**
- ✅ **Source tag obligatoire** : (SCAN/HYBRiD/RETAiL)
- ⚠️ Issue numbers : Recommandé format `No2/No.2/N02/N.02/NR02/NR.02`
- ✅ **Tags additionnels** : READNFO, NFOFiX, DiRFiX, iNTERNAL, PROPER entre source et format
- ✅ **Author et year** : Tag selon édition
  - ⚠️ **SCAN** : Toujours tagged avec année publication originale et publisher
  - ⚠️ **Digital editions** : Toujours tagged avec année publication ebook et publisher ebook
  - Exemple : 
    - `J.R.R.Tolkien.The.Lord.of.The.Rings.1955.SCAN.eBOOK-GRP` (scan)
    - `J.R.R.Tolkien.The.Lord.of.The.Rings.2010.RETAiL.eBOOK-GRP` (digital)
- ⚠️ **Format tag** : Si fichier n'est pas PDF, ajouter tag correct (ePUB, CBZ, KF8, AZW, MOBI, PRC)
  - Exemple : `Himmel.Over.London.2010.SWEDiSH.RETAiL.ePUB.eBOOK-COOLGROUPTAG`

### 5.1 MAGAZiNES

**Structure** :
- Nom du Magazine
- Issue et Year (e.g. `Cool.Magazine.No.1.2012.Ebook-CoolGRP`)
- Si issue number non disponible : Utiliser month/week/timestamp (intelligent)
- Source et Language (e.g. `RETAiL/SCAN` et `SWEDiSH/FRENCH/etc`)
- **MAGAZiNE tag obligatoire** dans dirname (sauf si "magazine" est mot exact du titre)
- Newspapers bonus content : Pas requis tag .MAGAZiNE
- Newspapers périodiques (weekly/monthly) : Sont magazines → tag .MAGAZiNE requis
- Exemple : `PC.Magazine.NR03.2008.FRENCH.RETAiL.MAGAZiNE.eBOOk-GRP`

### 5.2 COMiCS

**Structure** :
- Nom du comic
- Volume et Issue
- Source et Language
- **COMiC tag obligatoire** dans dirname
  - Exception : Si "Comic" est partie du titre, tag COMiC non requis
- Exemple : `Batman.Vol.23.No.22.Dec.2007.SWEDiSH.SCAN.COMiC.eBOOk-COOLGRP`

### 5.3 MANGA

**Règles** :
- Tag **MANGA** : Alternative à COMiC tag pour comics/graphic novels origine Japan
- Peut s'appliquer autres situations (foreign mangakas, manhwa, manfra...)
- **Interchangeabilité** :
  - MANGA tagged as COMiC : Ne doit PAS être nuké
  - COMiC tagged as MANGA : Ne doit PAS être nuké
  - ⚠️ DiRFiXes bienvenus si ça arrive
- **Structure** :
  - Nom du manga
  - Volume et Issue
  - Source et Language
  - **MANGA tag obligatoire** dans dirname
    - Exception : Si "Manga" est partie du titre, tag MANGA non requis
- Exemple : `One.Piece.Vol.23.JAPANESE.SCAN.MANGA.eBOOk-COOLGRP`

### 5.4 BOOKS (E.G. FiCTiONAL LiTERATURE)

**Structure** :
- Auteur ou Publisher
- Nom du livre
- Issue number si existe (e.g. "3rd.Edition")
- Year de release livre
- Source et Language
- Exemple : `Ken.Follet.Pillars.6th.Edition.2007.FRENCH.RETAiL.eBOOk-GRP`

### 5.5 BOOKS (E.G. TECHNiCAL LiTERATURE)

**Structure** :
- Publisher ou Author
- Titre du livre
- Issue/version/edition et année publication si disponible
- Year release livre
- Source et Language
- Exemple : `Wileys.Books.Tools.and.Computing.2008.GERMAN.RETAiL.eBOOk-GRP`

### 5.6 NEWSPAPERS

**Structure** :
- Nom du newspaper
- Date du paper (e.g. `23.December`, `23.Dec.`, `23.12` etc)
- Language et Source
- Exemple : `Your.Daily.News.23.December.2012.iTALiAN.RETAiL.eBOOK-GRP`

### 5.7 XXX BOOKS

**Règles** :
- ⚠️ **Uniquement** hardcore XXX books/magazines (pas softcore comme Playboy Magazine)
- Global dirnaming rules appliquées
- **XXX tag** ajouté au dirname
- Exemple : `Nikky.Cuffed.Fuck.Me.2011.RETAiL.XXX.eBOOK-GRP`

---

## 🔄 Section 6 : DUPES/PROPER

### 6.1 DUPES

**Ordre de priorité** : `RETAiL > HYBRiD > SCAN` (`>` signifie supersède)

**Règles** :
- ⚠️ Quand retail est out : Aucune autre source autorisée pour même format sans tag `.iNTERNAL.`
- ✅ Releases meilleure qualité : Toujours bienvenues, de n'importe quelle source, utiliser tag `.iNTERNAL.` avec explication dans .nfo

### 6.2 PROPER

**Règles** :
- ✅ Proper valide si release original ne respectait pas requirements règles ci-dessus
- ❌ Packing related propers : **INTERDITS** d'autres groups dans les **premiers 24 heures** après pre
- ✅ Raison proper obligatoire : Dans .nfo, avec preuve pour flaws techniques
- ⚠️ Si release PROPER/REPACK/FIX : **Dirname du release problématique** DOIT être listé dans votre .nfo file

---

## 📝 Section 7 : MiSCELLANEOUS

### 7.1 HOMEMADE

- ❌ Releases homemade : **INTERDITS**

### 7.2 COVERS

- ❌ Covers séparés : **INTERDITS**

---

## ✅ Section 8 : SiGN

### 8.1 ORGANiZATiONAL STUFF

- Compliance avec cette règle : **Optionnelle** depuis 2020-04-02
- Compliance : **MANDATORY** depuis **2020-04-19 00:00:00 UTC**

### 8.2 SiGNED BY

Groupes signataires :
- 13 AEROHOLICS BitBook DiSTRiBUTiON DiVER FMR iDiB INKED LiBRiCiDE LORENZ PAPERCLiPS PRiNTER TONER dbOOk

---

## 🔧 Intégration dans le Processus de Packaging

### Étape Critique : Chargement Règle

**AVANT toute étape de packaging EBOOK** :

1. **Téléchargement automatique** :
   ```python
   # Service à créer
   def download_ebook_rule_2022() -> str:
       """Télécharge règle depuis scenerules.org."""
       url = "https://scenerules.org/html/2022_EBOOK.html"
       # Téléchargement et parsing HTML → texte
       return content
   ```

2. **Parsing complet** :
   ```python
   def parse_ebook_rule_2022(content: str) -> EbookRuleSpec:
       """Parse règle complète et extrait toutes contraintes."""
       spec = EbookRuleSpec()
       
       # Section 2.6 : Formats acceptés
       spec.accepted_formats = [
           'PDF', 'EPUB', 'CBZ', 
           'AZW', 'KF8',  # Kindle
           'PRC', 'MOBI'  # MOBIPOCKET
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
           'archive_filename_max_chars': 140
       }
       
       # Section 3.1 : ZIP sizes autorisés
       spec.zip_sizes = [
           5_000_000,    # 5MB
           10_000_000,   # 10MB
           50_000_000,   # 50MB
           100_000_000,  # 100MB
           150_000_000,  # 150MB
           200_000_000,  # 200MB
           250_000_000   # 250MB
       ]
       
       # Section 4.1 : NFO mandatory info
       spec.nfo_mandatory = [
           'release_date',      # ISO YYYY-MM-DD
           'publish_date',      # ISO YYYY-MM-DD ou YYYY
           'language',
           'release_type',      # RETAiL/SCAN/HYBRiD
           'author_or_publisher',  # Au moins un
           'issue_or_volume',
           'source_link'        # Si retail
       ]
       
       # Section 5 : Dirnaming rules
       spec.dirnaming = {
           'grouptag_required': True,
           'year_tag_required': True,
           'language_tag_non_english_only': True,
           'source_tag_required': True,  # SCAN/HYBRiD/RETAiL
           'format_tag_if_not_pdf': True  # ePUB, CBZ, KF8, AZW, MOBI, PRC
       }
       
       return spec
   ```

### Validation à Chaque Étape

**Étape 2 : Type Release** :
- ✅ Format fichier source conforme formats acceptés (Section 2.6)

**Étape 4 : Fichier** :
- ✅ Format fichier dans liste formats acceptés
- ✅ Taille fichier vérifiée
- ✅ DRM/Watermark détecté → ERREUR (Section 2.4)

**Étape 7 : Templates** :
- ✅ NFO template conforme Section 4.1 (informations mandataires)
- ✅ NFO width ≤ 80 caractères
- ✅ DIZ file généré (DISK: [xx/??], max 44x30)

**Étape 8 : Options/Paramètres** :
- ✅ ZIP size dans liste tailles autorisées (Section 3.1)
- ✅ Nombre fichiers ≤ 99
- ✅ Structure ZIP+DIZ respectée
- ✅ Filenames conformes (8.3 pour volumes, max 140 pour archive)

**Packaging Final** :
- ✅ Dirnaming conforme Section 5 (selon type : magazine, comic, manga, book, newspaper, XXX)
- ✅ Grouptag présent
- ✅ Source tag présent (SCAN/HYBRiD/RETAiL)
- ✅ Year tag présent
- ✅ Format tag si non-PDF
- ✅ Dirname ≤ 243 caractères

---

## 📊 Structure EbookRuleSpec Complète

```python
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class EbookRuleSpec:
    """Spécification complète règle eBOOK [2022]."""
    
    # Section 2.6 : Formats acceptés
    accepted_formats: List[str] = None
    
    # Section 2.1-2.5 : Technical details
    scan_rules: Dict = None
    retail_rules: Dict = None
    hybrid_definition: str = None
    drm_watermark_rules: Dict = None
    nfo_diz_rules: Dict = None
    
    # Section 3 : Packaging
    packaging_rules: Dict = None
    zip_allowed_sizes: List[int] = None
    max_files_per_zip: int = 99
    
    # Section 4 : NFO
    nfo_mandatory_fields: List[str] = None
    nfo_optional_fields: List[str] = None
    nfo_max_width: int = 80
    diz_max_width: int = 44
    diz_max_height: int = 30
    
    # Section 5 : Dirnaming
    dirnaming_rules: Dict = None
    dirname_max_chars: int = 243
    archive_filename_max_chars: int = 140
    
    # Section 6 : Dupes/Proper
    dupe_order: List[str] = None  # ['RETAiL', 'HYBRiD', 'SCAN']
    proper_rules: Dict = None
    
    # Section 7 : Miscellaneous
    homemade_allowed: bool = False
    separate_covers_allowed: bool = False
```

---

## ✅ Checklist Implémentation

### Services Backend à Créer

- [ ] **ScenerulesDownloadService** : Téléchargement règles scenerules.org
  - Méthode `download_ebook_2022() -> str`
  - Méthode `download_all_ebook_rules() -> List[str]`
  - Cache local avec vérification mise à jour

- [ ] **RuleParserService** : Parsing règles complètes
  - Méthode `parse_ebook_2022(content: str) -> EbookRuleSpec`
  - Extraction toutes sections (2, 3, 4, 5, 6, 7, 8)
  - Structure `EbookRuleSpec` complète

- [ ] **RuleValidationService** : Validation contre règle
  - Méthode `validate_ebook_format(file_path: Path, rule_spec: EbookRuleSpec) -> tuple[bool, list[str]]`
  - Méthode `validate_ebook_packaging(structure: dict, rule_spec: EbookRuleSpec) -> tuple[bool, list[str]]`
  - Méthode `validate_ebook_nfo(nfo_content: str, rule_spec: EbookRuleSpec) -> tuple[bool, list[str]]`
  - Méthode `validate_ebook_dirname(dirname: str, release_type: str, rule_spec: EbookRuleSpec) -> tuple[bool, list[str]]`

### Intégration Wizard

**Étape 3** :
- [ ] Charger règle eBOOK [2022] automatiquement si type = EBOOK
- [ ] Parser règle complète
- [ ] Stocker `EbookRuleSpec` dans wizard state
- [ ] Afficher règle dans NFO viewer

**Étape 4** :
- [ ] Valider format fichier contre `rule_spec.accepted_formats`
- [ ] Détecter DRM/Watermark → ERREUR si présent
- [ ] Valider taille fichier

**Étape 7** :
- [ ] Générer NFO avec toutes informations mandataires (Section 4.1)
- [ ] Valider NFO width ≤ 80 caractères
- [ ] Générer DIZ file (DISK: [xx/??], max 44x30)
- [ ] Utiliser template conforme règle

**Étape 8** :
- [ ] Valider ZIP size dans `rule_spec.zip_allowed_sizes`
- [ ] Valider nombre fichiers ≤ 99
- [ ] Valider structure ZIP+DIZ
- [ ] Valider filenames (8.3 pour volumes, max 140 pour archive)

**Packaging** :
- [ ] Générer dirname conforme Section 5 (selon type : magazine, comic, manga, book, newspaper)
- [ ] Valider dirname ≤ 243 caractères
- [ ] Appliquer toutes contraintes règle
- [ ] Validation finale complète

---

## 🚨 Règles Critiques à Respecter Absolument

### ⚠️ INTERDICTIONS ABSOLUES

1. ❌ **DRM/Watermark** : Interdit (doivent être retirés)
2. ❌ **Free from web** : Interdit (sauf internal releases)
3. ❌ **Conversions** : Interdites (epub→pdf, etc.)
4. ❌ **Homemade releases** : Interdits
5. ❌ **Covers séparés** : Interdits
6. ❌ **SFV dans ZIP** : Interdit
7. ❌ **Espaces dans filenames** (rar/zip/diz/nfo) : Interdits
8. ❌ **> 99 fichiers par ZIP** : Interdit
9. ❌ **ZIP size non autorisée** : Interdit (uniquement 7 tailles autorisées)

### ✅ OBLIGATIONS ABSOLUES

1. ✅ **.nfo file** : Obligatoire dans tous les cas
2. ✅ **.diz file** : Obligatoire
3. ✅ **Grouptag** : Obligatoire dans dirname
4. ✅ **Year tag** : Obligatoire dans dirname
5. ✅ **Source tag** : Obligatoire (SCAN/HYBRiD/RETAiL)
6. ✅ **Proof URL** : Obligatoire si RETAiL
7. ✅ **ZIP+DIZ** : Structure obligatoire
8. ✅ **NFO informations mandataires** : Toutes requises (ou dans dirname)

---

## 📚 Références

- **Site officiel** : [scenerules.org](https://scenerules.org/)
- **Règle eBOOK [2022]** : [HTML](https://scenerules.org/html/2022_EBOOK.html) | [NFO](https://scenerules.org/nfo/2022_EBOOK.nfo)
- **Dernière mise à jour scenerules.org** : 2024-04-23
- **Version règle** : 2022 (English - Current)
- **Signée par** : 13 groupes Scene

---

## ✅ Conclusion

Cette règle eBOOK [2022] contient **TOUTES** les spécifications nécessaires pour créer un packaging EBOOK conforme Scene.

**Obligation** : Cette règle DOIT être intégrée dans le système de packaging avant Phase 3 (Wizard).

**Validation** : Chaque étape du packaging DOIT valider contre cette règle complète.

**Conformité** : Aucun packaging EBOOK ne doit être créé sans validation complète contre cette règle.

---

**Document créé le** : 2025-11-01  
**Source** : Règle complète récupérée depuis [scenerules.org](https://scenerules.org/)  
**Statut** : ✅ **DOCUMENT COMPLET - PRÊT POUR INTÉGRATION**

