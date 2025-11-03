# ⚠️ Prérequis Critiques - Phase 3 : Nouvelle Release Wizard

**Date** : 2025-11-01  
**Objectif** : Documenter les prérequis OBLIGATOIRES avant de commencer Phase 3 (Wizard)

---

## 🚨 PRÉREQUIS ABSOLU : Analyse Règles Scene EBOOK

### Pourquoi C'est Critique

Pour packager un EBOOK de manière conforme aux standards Scene, il est **OBLIGATOIRE** de :

1. **Télécharger** la règle **[2022] eBOOK** complète depuis https://scenerules.org/
2. **Analyser intégralement** le contenu de la règle
3. **Extraire** toutes les spécifications techniques :
   - Formats de fichiers acceptés
   - Structure de nommage exacte
   - Fichiers requis (ZIP, RAR, NFO, DIZ, SFV)
   - Exigences de validation
   - Règles de packaging
4. **Implémenter** le parser de règles dans le backend
5. **Intégrer** les spécifications dans le service de packaging

**⚠️ SANS CETTE ANALYSE, LE PACKAGING NE SERA PAS CONFORME.**

---

## 📋 Règle EBOOK à Analyser

### Règle Officielle

**Source** : https://scenerules.org/  
**Règle** : **[2022] eBOOK** [p/t/n/d]

**Format** : Fichier `.nfo` (texte Scene standard)

**Disponibilité** :
- [p] = Picture (image) - Référence visuelle
- [t] = Text (texte) - Version texte pour parsing
- [n] = Numbered - Version numérotée
- [d] = Download - Téléchargement direct

### Action Immédiate Requise

**Avant Phase 3, il faut** :

1. ✅ Télécharger la règle [2022] eBOOK depuis scenerules.org
2. ✅ Analyser structure et contenu complet
3. ✅ Extraire toutes les spécifications dans format structuré
4. ✅ Créer `RuleParserService` pour parsing automatique
5. ✅ Implémenter validation selon règles extraites
6. ✅ Tests conformité 100%

---

## 🔧 Implémentation Nécessaire

### Backend : RuleParserService

**Nouveau service** : `web/services/rule_parser.py`

```python
class RuleParserService:
    """Parse et extraire spécifications des règles Scene."""
    
    def parse_ebook_rule_2022(self, rule_content: str) -> EBookRuleSpec:
        """Parser la règle [2022] eBOOK intégralement.
        
        Retourne un objet structuré avec :
        - Formats fichiers acceptés
        - Structure nommage
        - Fichiers requis
        - Règles de validation
        - Exigences packaging
        """
        pass
    
    def extract_file_formats(self, rule_content: str) -> list[str]:
        """Extraire formats de fichiers acceptés (.epub, .pdf, etc.)."""
        pass
    
    def extract_naming_format(self, rule_content: str) -> NamingFormat:
        """Extraire format de nommage exact."""
        pass
    
    def extract_required_files(self, rule_content: str) -> list[str]:
        """Extraire fichiers requis (ZIP, RAR, NFO, DIZ, SFV)."""
        pass
```

### Backend : PackagingService Mis à Jour

**Service existant** : `web/services/packaging.py`

**Modifications nécessaires** :

```python
class PackagingService:
    def package_ebook(self, file_path: Path, group: str, rule: Rule) -> Release:
        """Packager EBOOK selon règle [2022] eBOOK.
        
        ⚠️ CRITIQUE : Utilise règles parsées pour conformité 100%.
        """
        # 1. Parser règle intégralement
        rule_spec = self.rule_parser.parse_ebook_rule_2022(rule.content)
        
        # 2. Valider fichier selon règles extraites
        validation = self.validate_file_against_rule(file_path, rule_spec)
        if not validation.valid:
            raise ValidationError(validation.errors)
        
        # 3. Générer nom conforme format exact
        release_name = self.generate_release_name(metadata, group, rule_spec.naming_format)
        
        # 4. Créer structure conforme règles
        # 5. Générer fichiers requis (ZIP, RAR, NFO, etc.) selon règles
        # 6. Valider conformité finale
        pass
```

---

## 📊 Base de Données : Table rule_specs

### Nouvelle Table Nécessaire

```sql
CREATE TABLE rule_specs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    rule_id INT NOT NULL,
    rule_type VARCHAR(50) NOT NULL,  -- 'EBOOK', 'TV', 'DOCS', etc.
    rule_year INT NOT NULL,          -- 2022 pour eBOOK
    spec_json JSON NOT NULL,         -- Spécifications parsées structurées
    parsed_at DATETIME NOT NULL,
    parser_version VARCHAR(20) NOT NULL,
    FOREIGN KEY (rule_id) REFERENCES rules(id)
);

-- Index
CREATE INDEX idx_rule_specs_type_year ON rule_specs(rule_type, rule_year);
```

**Contenu `spec_json`** (exemple pour EBOOK) :
```json
{
  "file_formats": {
    "accepted": [".epub", ".pdf", ".mobi", ".azw3", ".cbz"],
    "max_size_mb": null,
    "min_size_kb": null,
    "validation_rules": {
      "epub": {
        "check_integrity": true,
        "required_metadata": ["title", "author", "isbn"]
      }
    }
  },
  "naming": {
    "format": "Group-Author-Title-Format-Language-Year-ISBN-eBook",
    "separators": ["-"],
    "components": {
      "Group": {"required": true, "format": "SceneGroup"},
      "Author": {"required": true, "format": "AuthorName"},
      "Title": {"required": true, "format": "BookTitle"},
      "Format": {"required": true, "values": ["EPUB", "PDF", "MOBI", "AZW3", "CBZ"]},
      "Language": {"required": true, "format": "ISO639"},
      "Year": {"required": true, "format": "YYYY"},
      "ISBN": {"required": false, "format": "ISBN13"},
      "eBook": {"required": true, "fixed": "eBook"}
    },
    "max_length": 250,
    "case_sensitive": false
  },
  "required_files": {
    "source": true,
    "zip": true,
    "rar": false,
    "nfo": true,
    "diz": false,
    "sfv": false
  },
  "packaging": {
    "zip": {
      "compression_level": 6,
      "method": "deflate",
      "comment": false
    },
    "rar": {
      "required": false,
      "version": null
    },
    "checksums": {
      "required": false,
      "algorithm": null
    }
  }
}
```

---

## ✅ Checklist Avant Phase 3

### Analyse Règle [2022] eBOOK
- [ ] Règle téléchargée depuis scenerules.org (versions [t] et [d])
- [ ] Contenu analysé intégralement
- [ ] Formats fichiers acceptés identifiés
- [ ] Structure nommage extraite (format exact, composants, séparateurs)
- [ ] Fichiers requis identifiés (ZIP, RAR, NFO, DIZ, SFV)
- [ ] Exigences validation identifiées
- [ ] Règles packaging extraites
- [ ] Spécifications documentées dans `docs/SCENE_RULES_EBOOK_2022.md`

### Implémentation Backend
- [ ] `RuleParserService` créé
- [ ] Méthode `parse_ebook_rule_2022()` implémentée
- [ ] Extraction formats fichiers fonctionnelle
- [ ] Extraction format nommage fonctionnelle
- [ ] Extraction fichiers requis fonctionnelle
- [ ] Table `rule_specs` créée (migration)
- [ ] Stockage spécifications parsées en JSON
- [ ] Tests parsing règle [2022] eBOOK (100% extraction)

### Intégration Packaging
- [ ] `PackagingService.package_ebook()` mis à jour pour utiliser règles parsées
- [ ] Validation fichier selon règles extraites
- [ ] Génération nom release conforme format exact
- [ ] Création structure fichiers selon règles
- [ ] Génération ZIP/RAR selon exigences règles
- [ ] Tests conformité 100% (packaging complet)

### Documentation
- [ ] `docs/SCENE_RULES_EBOOK_ANALYSIS.md` créé (ce document)
- [ ] `docs/SCENE_RULES_EBOOK_2022.md` créé (règle complète annotée)
- [ ] `docs/PACKAGING_EBOOK_SPECS.md` créé (spécifications techniques extraites)
- [ ] PRD-002 mis à jour avec références règles
- [ ] API Reference mise à jour (endpoints parsing règles)

---

## 🔗 Références

- **scenerules.org** : https://scenerules.org/
- **Règle EBOOK 2022** : [2022] eBOOK [p/t/n/d]
- **Documentation projet** : `docs/SCENE_RULES_EBOOK_ANALYSIS.md`

---

## ⚠️ Règle Absolue

**JAMAIS commencer Phase 3 (Wizard) si la règle [2022] eBOOK n'est pas analysée intégralement et le RuleParserService implémenté.**

**Selon Definition of Done** : Chaque étape doit être complétée à 100% avant de continuer. L'analyse des règles est une étape CRITIQUE pour le packaging conforme.

---

**Dernière mise à jour** : 2025-11-01  
**Statut** : ⚠️ Action requise avant Phase 3

