# ⚠️ EXIGENCE CRITIQUE - Intégration scenerules.org pour Packaging EBOOK

**Date** : 2025-11-01  
**Source** : [scenerules.org](https://scenerules.org/)  
**Statut** : ⚠️ **CRITIQUE - OBLIGATOIRE AVANT PHASE 3**

---

## 🚨 EXIGENCE ABSOLUE

**Pour packager des EBOOK, il est IMPÉRATIF de prendre connaissance TOTALE et INTÉGRALE des règles disponibles sur [scenerules.org](https://scenerules.org/).**

Le packaging EBOOK ne peut PAS être implémenté sans :
1. ✅ **Téléchargement** de la règle **[2022] eBOOK** complète depuis scenerules.org
2. ✅ **Analyse intégrale** du contenu de la règle
3. ✅ **Extraction** de toutes les spécifications techniques
4. ✅ **Parsing** automatisé des règles
5. ✅ **Validation** stricte contre les règles extraites
6. ✅ **Packaging conforme** à 100% selon spécifications

---

## 📋 Règle EBOOK à Analyser

### Règle Officielle Actuelle

**Source** : https://scenerules.org/  
**Règle** : **[2022] eBOOK** [p/t/n/d]

**Format** : Fichier `.nfo` (texte Scene standard)

**Disponibilité** :
- [p] = Picture (image) - Référence visuelle
- [t] = Text (texte) - Version texte pour parsing automatique ⭐
- [n] = Numbered - Version numérotée
- [d] = Download - Téléchargement direct ⭐

**URL probable** :
- HTML : `https://scenerules.org/html/2022_EBOOK.html`
- NFO : `https://scenerules.org/nfo/2022_EBOOK.nfo`

**⚠️ Action Immédiate** : Télécharger et analyser cette règle intégralement.

---

## 🔍 Informations de scenerules.org

D'après https://scenerules.org/, les règles sont organisées par :

### Scènes
- English ⭐ (PRIORITÉ pour EBOOK)
- Baltic, Danish, Dutch, Flemish, French, German, Hungarian, Italian, Lithuanian, Polish, Spanish, Swedish

### Sections EBOOK Disponibles

**Current English Rules** :
- **[2022] eBOOK** [p/t/n/d] ⭐ **VERSION ACTUELLE - PRIORITÉ ABSOLUE**

**Ye Olde English Rules** :
- [2012] eBOOK [p/t/n/d] (historique)

**Autres Scènes** :
- German : [2002] EBOOK, [2004] EBOOK3, [2009] EBOOK
- Polish : [2006] EBOOK

**⚠️ Utiliser UNIQUEMENT [2022] eBOOK English pour conformité actuelle.**

---

## 📐 Éléments à Extraire de la Règle

### 1. Formats de Fichiers Acceptés
- Quels formats exacts : `.epub`, `.pdf`, `.mobi`, `.azw3`, `.cbz` ?
- Restrictions de taille (min/max) ?
- Exigences de qualité/intégrité ?

### 2. Structure de Nommage
- Format exact du nom de release
- Composants obligatoires (Group, Author, Title, Format, Language, Year, ISBN)
- Séparateurs autorisés (`-`)
- Longueur maximale/minimale
- Cas (majuscules/minuscules)

### 3. Fichiers Requis dans Release
- Fichier source (obligatoire)
- ZIP (obligatoire ?)
- RAR (obligatoire ou optionnel ?)
- NFO (obligatoire ? format exact ?)
- DIZ (obligatoire ou optionnel ?)
- SFV (obligatoire ou optionnel ?)
- Checksums (algorithme ?)

### 4. Validation et Contraintes
- Checksums requis ? (CRC32, MD5, SHA1 ?)
- Validation intégrité fichiers ?
- Exigences métadonnées (titre, auteur, ISBN obligatoires ?)
- Contraintes taille fichiers/archives

### 5. Structure Archivage
- Format ZIP (méthode compression, niveau)
- Format RAR (version, méthode, si requis)
- Répertoires autorisés dans archive ?
- Structure exacte du contenu

### 6. Template NFO
- Template NFO standardisé fourni dans règle
- Format exact (ASCII ≤ 80 colonnes ?)
- Placeholders/formatage requis
- Structure sections NFO

---

## 🔧 Implémentation Nécessaire

### Backend : RuleParserService (CRITIQUE)

**Nouveau service** : `web/services/rule_parser.py`

```python
class RuleParserService:
    """Parse et extraire spécifications des règles Scene depuis scenerules.org."""
    
    def parse_ebook_rule_2022(self, rule_content: str) -> EbookRuleSpec:
        """Parser la règle [2022] eBOOK intégralement.
        
        ⚠️ CRITIQUE : Analyse TOTALE et INTÉGRALE de la règle.
        
        Retourne un objet structuré avec :
        - Formats fichiers acceptés
        - Structure nommage exacte
        - Fichiers requis
        - Règles de validation
        - Exigences packaging
        - Template NFO standardisé
        
        Args:
            rule_content: Contenu complet du fichier .nfo de la règle
            
        Returns:
            EbookRuleSpec: Spécifications complètes extraites
            
        Raises:
            RuleParseError: Si parsing échoue ou règle incomplète
        """
        # 1. Valider que contenu est complet
        # 2. Extraire section formats fichiers
        # 3. Extraire section nommage
        # 4. Extraire section fichiers requis
        # 5. Extraire section validation
        # 6. Extraire template NFO
        # 7. Extraire contraintes packaging
        # 8. Retourner EbookRuleSpec structuré
        pass
    
    def extract_file_formats(self, rule_content: str) -> dict[str, FileFormatSpec]:
        """Extraire formats de fichiers acceptés (.epub, .pdf, etc.).
        
        Returns:
            Dict avec format comme clé et spécifications comme valeur
        """
        pass
    
    def extract_naming_format(self, rule_content: str) -> NamingFormat:
        """Extraire format de nommage exact.
        
        Returns:
            NamingFormat avec format, composants, séparateurs, contraintes
        """
        pass
    
    def extract_required_files(self, rule_content: str) -> RequiredFiles:
        """Extraire fichiers requis (ZIP, RAR, NFO, DIZ, SFV).
        
        Returns:
            RequiredFiles avec booléens pour chaque type
        """
        pass
    
    def extract_nfo_template(self, rule_content: str) -> str:
        """Extraire template NFO standardisé de la règle.
        
        Returns:
            Template NFO (format ASCII, ≤ 80 colonnes)
        """
        pass
```

### Backend : ScenerulesDownloadService

**Nouveau service** : `web/services/scenerules_download.py`

```python
class ScenerulesDownloadService:
    """Télécharger règles depuis scenerules.org."""
    
    def download_ebook_rule_2022(self) -> str:
        """Télécharger règle [2022] eBOOK depuis scenerules.org.
        
        Returns:
            Contenu complet du fichier .nfo
            
        Raises:
            DownloadError: Si téléchargement échoue
        """
        # Télécharger depuis https://scenerules.org/nfo/2022_EBOOK.nfo
        # Cache local pour éviter re-téléchargements
        # Retourner contenu texte complet
        pass
    
    def cache_rule(self, rule_content: str, rule_name: str) -> None:
        """Mettre en cache local une règle téléchargée."""
        pass
```

### Backend : PackagingService Mis à Jour

**Service existant** : `web/services/packaging.py`

**Modifications CRITIQUES** :

```python
class PackagingService:
    def package_ebook(
        self,
        file_path: Path,
        group: str,
        rule: Rule
    ) -> Release:
        """Packager EBOOK selon règle [2022] eBOOK.
        
        ⚠️ CRITIQUE : Utilise règles parsées pour conformité 100%.
        
        Processus :
        1. Charger règle complète depuis DB ou scenerules.org
        2. Parser règle intégralement (RuleParserService)
        3. Récupérer spécifications parsées (rule_specs)
        4. Valider fichier source contre rule_spec.file_formats
        5. Extraire métadonnées
        6. Générer nom release conforme rule_spec.naming
        7. Créer structure fichiers selon rule_spec.required_files
        8. Générer NFO selon rule_spec.template
        9. Créer ZIP/RAR selon rule_spec.packaging
        10. Valider conformité finale contre toutes exigences
        11. ❌ JAMais packager si validation échoue
        
        Args:
            file_path: Chemin fichier source
            group: Nom groupe Scene
            rule: Règle Scene à appliquer
            
        Returns:
            Release packagée conforme
            
        Raises:
            ValidationError: Si validation contre règle échoue
            RuleNotFoundError: Si règle non disponible
            RuleParseError: Si parsing règle échoue
        """
        # 1. Charger règle complète
        if not rule.content:
            # Télécharger depuis scenerules.org si nécessaire
            downloader = ScenerulesDownloadService()
            rule.content = downloader.download_ebook_rule_2022()
            # Sauvegarder dans DB
        
        # 2. Parser règle intégralement
        parser = RuleParserService()
        rule_spec = parser.parse_ebook_rule_2022(rule.content)
        
        # 3. Stocker spécifications parsées
        self.store_rule_spec(rule.id, rule_spec)
        
        # 4. Valider fichier selon règles extraites
        validation = self.validate_file_against_rule(file_path, rule_spec)
        if not validation.valid:
            raise ValidationError(
                f"Fichier non conforme : {validation.errors}"
            )
        
        # 5. Générer nom conforme format exact
        release_name = self.generate_release_name(
            metadata, group, rule_spec.naming_format
        )
        
        # 6. Créer structure conforme règles
        # 7. Générer fichiers requis selon rule_spec.required_files
        # 8. Générer NFO selon rule_spec.template
        # 9. Créer ZIP/RAR selon rule_spec.packaging
        # 10. Valider conformité finale
        pass
```

---

## 📊 Base de Données : Table rule_specs

### Migration Nécessaire

```sql
CREATE TABLE rule_specs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    rule_id INT NOT NULL,
    rule_type VARCHAR(50) NOT NULL,
    rule_year INT NOT NULL,
    spec_json JSON NOT NULL,
    parsed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    parser_version VARCHAR(20) NOT NULL,
    FOREIGN KEY (rule_id) REFERENCES rules(id) ON DELETE CASCADE,
    UNIQUE KEY unique_rule_type_year (rule_id, rule_type, rule_year),
    INDEX idx_type_year (rule_type, rule_year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Voir** : `docs/DATABASE_ERD.md` pour spécifications complètes.

---

## ✅ Checklist OBLIGATOIRE Avant Phase 3

### Analyse Règle [2022] eBOOK
- [ ] Règle téléchargée depuis https://scenerules.org/
- [ ] Contenu analysé intégralement (TOTALE et INTÉGRALE)
- [ ] Formats fichiers acceptés identifiés précisément
- [ ] Structure nommage extraite (format exact, composants, séparateurs)
- [ ] Fichiers requis identifiés (ZIP, RAR, NFO, DIZ, SFV)
- [ ] Exigences validation identifiées (checksums, intégrité, métadonnées)
- [ ] Règles packaging extraites (compression, structure, volumes)
- [ ] Template NFO extrait (format ASCII ≤ 80 colonnes)
- [ ] Spécifications documentées dans `docs/SCENE_RULES_EBOOK_2022.md`

### Implémentation Backend
- [ ] `RuleParserService` créé
- [ ] Méthode `parse_ebook_rule_2022()` implémentée
- [ ] Extraction formats fichiers fonctionnelle
- [ ] Extraction format nommage fonctionnelle
- [ ] Extraction fichiers requis fonctionnelle
- [ ] Extraction template NFO fonctionnelle
- [ ] Extraction contraintes packaging fonctionnelle
- [ ] Table `rule_specs` créée (migration)
- [ ] Stockage spécifications parsées en JSON
- [ ] Tests parsing règle [2022] eBOOK (100% extraction)

### Intégration Packaging
- [ ] `PackagingService.package_ebook()` mis à jour pour utiliser règles parsées
- [ ] Validation fichier selon règles extraites
- [ ] Génération nom release conforme format exact
- [ ] Création structure fichiers selon règles
- [ ] Génération ZIP/RAR selon exigences règles
- [ ] Génération NFO selon template règle
- [ ] Validation conformité finale
- [ ] Tests conformité 100% (packaging complet)

### Documentation
- [ ] `docs/SCENE_RULES_EBOOK_ANALYSIS.md` créé
- [ ] `docs/SCENE_RULES_EBOOK_2022.md` créé (règle complète annotée)
- [ ] `docs/PREREQUISITES_PHASE3_WIZARD.md` créé
- [ ] PRD-002 mis à jour avec références règles
- [ ] API Reference mise à jour (endpoints parsing règles)
- [ ] DATABASE_ERD mis à jour (table rule_specs)

---

## 🔗 Références

- **scenerules.org** : https://scenerules.org/
- **Règle EBOOK 2022** : [2022] eBOOK [p/t/n/d]
- **Documentation projet** :
  - `docs/SCENE_RULES_EBOOK_ANALYSIS.md`
  - `docs/PREREQUISITES_PHASE3_WIZARD.md`
  - `docs/PRDs/PRD-002-Nouvelle-Release.md`

---

## ⚠️ Règle Absolue - Definition of Done

**JAMAIS commencer Phase 3 (Wizard) si la règle [2022] eBOOK n'est pas analysée intégralement et le RuleParserService implémenté.**

**Selon Definition of Done** : Chaque étape doit être complétée à 100% avant de continuer. L'analyse des règles est une étape CRITIQUE pour le packaging conforme.

**Statut actuel** : ⚠️ **Action requise avant Phase 3**

---

**Dernière mise à jour** : 2025-11-01  
**Source** : https://scenerules.org/  
**Priorité** : ⚠️ **CRITIQUE**

