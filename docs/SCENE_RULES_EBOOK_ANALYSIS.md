# 📚 Analyse Complète des Règles Scene EBOOK - scenerules.org

**Date** : 2025-11-01  
**Source** : https://scenerules.org/  
**Objectif** : Comprendre intégralement les règles Scene EBOOK pour implémenter le packaging conforme

---

## 🎯 Règle EBOOK Actuelle (2022)

### Informations Clés

**Règle officielle** : **[2022] eBOOK [p/t/n/d]**

**Source** : https://scenerules.org/  
**Année** : 2022 (la plus récente)  
**Format** : Fichier `.nfo` (texte Scene standard)

**Disponibilité** :
- [p] = Picture (image)
- [t] = Text (texte/version texte)
- [n] = Numbered (version numérotée)
- [d] = Download (téléchargement)

---

## 📋 Structure des Règles Scene

### Format Général

Les règles Scene sont des fichiers `.nfo` qui contiennent :
1. **Spécifications de formatage** : Nommage fichiers, structure répertoires
2. **Règles de validation** : Formats acceptés, tailles min/max
3. **Standards de qualité** : Exigences techniques
4. **Structure de release** : Fichiers requis (ZIP, RAR, NFO, DIZ, SFV, etc.)

### Types de Règles

D'après https://scenerules.org/, les règles sont organisées par :
- **Scene** : English, Baltic, Danish, Dutch, Flemish, French, German, Hungarian, Italian, Lithuanian, Polish, Spanish, Swedish
- **Section** : eBOOK, TV-720p, TV-SD, X264, X265, BLURAY, etc.
- **Année** : Année de publication/révision (2022 pour eBOOK actuel)

---

## 🔍 Règles EBOOK Disponibles sur scenerules.org

### Règles Actuelles (Current English Rules)

**Règle principale** :
- **[2022] eBOOK** [p/t/n/d] ← **RÈGLE À UTILISER**

### Règles Historiques (Ye Olde English Rules)

**Anciennes règles EBOOK** (pour référence historique) :
- [2012] eBOOK [p/t/n/d]

**Règles EBOOK autres langues** :
- **German** :
  - [2002] EBOOK [p/t/n/d]
  - [2004] EBOOK3 [p/t/n/d]
  - [2009] EBOOK [p/t/n/d]
- **Polish** :
  - [2006] EBOOK [p/t/n/d]

**⚠️ Important** : Utiliser uniquement la règle **[2022] eBOOK** pour conformité actuelle.

---

## 📐 Structure Attendue d'une Release EBOOK Scene

### Composants Obligatoires

D'après les standards Scene standard, une release EBOOK complète doit contenir :

1. **Fichier source** : `.epub`, `.pdf`, `.mobi`, `.azw3`, `.cbz` (selon règle)
2. **Archive ZIP** : Contenant la release
3. **Archive RAR** : Contenant la release (optionnel selon règle)
4. **Fichier NFO** : Informations release (format Scene standard)
5. **Fichier DIZ** : Description release (optionnel)
6. **Fichier SFV** : Checksums pour validation (optionnel mais recommandé)

### Nommage Release

Format standard Scene :
```
GroupName-Author-Title-Format-Language-Year-ISBN-eBook
```

Exemple :
```
Group-IsaacAsimov-Foundation-EPUB-EN-2024-978-0-00-000000-0-eBook
```

### Structure Répertoires

```
ReleaseName/
├── ReleaseName.epub          # Fichier source
├── ReleaseName.nfo          # Informations Scene
├── ReleaseName.diz          # Description (optionnel)
└── ReleaseName.sfv          # Checksums (optionnel)
```

Puis archivé dans :
- `ReleaseName.zip`
- `ReleaseName.rar` (si requis par règle)

---

## 🔧 Analyse Technique Nécessaire

### Éléments à Extraire de la Règle [2022] eBOOK

Pour implémenter correctement le packaging, il faut analyser la règle et extraire :

#### 1. Formats de Fichiers Acceptés
- Quels formats `.epub`, `.pdf`, `.mobi`, `.azw3`, `.cbz` sont acceptés ?
- Y a-t-il des restrictions de taille ?
- Y a-t-il des exigences de qualité ?

#### 2. Structure de Nommage
- Format exact du nom de release
- Composants obligatoires (Group, Author, Title, Format, etc.)
- Séparateurs autorisés
- Longueur maximale/minimale

#### 3. Fichiers Requis
- NFO obligatoire ? Format exact ?
- DIZ requis ?
- SFV requis ?
- ZIP/RAR : les deux ou un seul ?

#### 4. Validation
- Checksums requis ? (CRC32, MD5, SHA1 ?)
- Validation intégrité fichiers ?
- Exigences métadonnées ?

#### 5. Structure Archivage
- Format ZIP (méthode compression, niveau)
- Format RAR (version, méthode)
- Répertoires autorisés dans archive ?

---

## 📥 Action Immédiate Requise

### Étape 1 : Télécharger et Analyser la Règle [2022] eBOOK

**Action** : Télécharger la règle complète depuis https://scenerules.org/

**Fichiers à récupérer** :
- Version texte [t] : Pour parsing automatique
- Version picture [p] : Pour référence visuelle
- Version download [d] : Fichier .nfo complet

**URL probable** : https://scenerules.org/nfo/[2022]_eBOOK.nfo (format à confirmer)

### Étape 2 : Parser la Règle

**Objectif** : Extraire toutes les spécifications de manière structurée

**Format attendu** : Fichier `.nfo` texte avec :
- Sections délimitées (format, nommage, validation, etc.)
- Règles spécifiques par format (.epub, .pdf, etc.)
- Exemples de nommage
- Exigences techniques

### Étape 3 : Documenter dans le Projet

**Créer** :
1. `docs/SCENE_RULES_EBOOK_2022.md` : Règle complète avec annotations
2. `docs/PACKAGING_EBOOK_SPECS.md` : Spécifications techniques extraites
3. Mettre à jour PRD-002 avec détails précis de validation

### Étape 4 : Implémenter la Validation

**Backend** : Service de validation selon règles extraites
**Frontend** : Validation temps réel pendant wizard étape 4 (fichier)

---

## 🎯 Intégration dans le Projet v2

### Backend : Service de Validation Règles

```python
# web/services/rule_parser.py
class RuleParser:
    """Parse Scene rules from scenerules.org format."""
    
    def parse_ebook_rule_2022(self, rule_content: str) -> EBookRuleSpec:
        """Parse la règle [2022] eBOOK et extraire spécifications."""
        # Analyse complète du fichier .nfo
        pass
    
    def validate_file_format(self, file_path: Path, rule_spec: EBookRuleSpec) -> ValidationResult:
        """Valider format fichier selon règle."""
        pass
    
    def validate_release_name(self, release_name: str, rule_spec: EBookRuleSpec) -> ValidationResult:
        """Valider nom de release selon règle."""
        pass

# web/services/packaging.py
class PackagingService:
    """Service de packaging conforme règles Scene."""
    
    def package_ebook(self, file_path: Path, group: str, rule: Rule) -> Release:
        """Packager EBOOK selon règle [2022] eBOOK."""
        # 1. Parser règle
        rule_spec = self.rule_parser.parse_ebook_rule_2022(rule.content)
        
        # 2. Valider fichier source
        validation = self.validate_file(file_path, rule_spec)
        if not validation.valid:
            raise ValidationError(validation.errors)
        
        # 3. Extraire métadonnées
        metadata = self.metadata_service.extract(file_path)
        
        # 4. Générer nom release conforme
        release_name = self.generate_release_name(metadata, group, rule_spec)
        
        # 5. Créer structure fichiers
        # 6. Générer NFO selon format règle
        # 7. Créer ZIP/RAR selon exigences règle
        # 8. Valider checksums si requis
        pass
```

### Frontend : Validation Temps Réel

```typescript
// frontend/src/services/ruleValidation.ts
export class RuleValidationService {
  async validateEBookFile(file: File, ruleId: string): Promise<ValidationResult> {
    // Appel API pour validation selon règle
    const response = await api.post(`/api/rules/${ruleId}/validate-file`, {
      filename: file.name,
      size: file.size,
      type: file.type,
    });
    return response.data;
  }
  
  async validateReleaseName(name: string, ruleId: string): Promise<ValidationResult> {
    // Validation nom release selon règle
    const response = await api.post(`/api/rules/${ruleId}/validate-name`, {
      name,
    });
    return response.data;
  }
}
```

---

## 📚 Références

- **scenerules.org** : https://scenerules.org/
- **Règle EBOOK 2022** : [2022] eBOOK [p/t/n/d]
- **Dernière mise à jour scenerules.org** : 2024-04-23
- **Dernière règle générale** : 2023_WEBFLAC.nfo

---

## ⚠️ Points Critiques

### 1. Conformité Totale Obligatoire

**Règle** : Le packaging EBOOK DOIT être **100% conforme** à la règle [2022] eBOOK.

**Implications** :
- Nommage strict selon format défini
- Structure fichiers exacte
- Validation complète avant packaging
- Tests de conformité obligatoires

### 2. Mise à Jour des Règles

**Risque** : Les règles Scene peuvent être mises à jour.

**Mitigation** :
- Vérifier régulièrement scenerules.org
- Permettre upload de nouvelles règles
- Versionner les règles dans la base de données
- Historique des règles utilisées par release

### 3. Parsing Robuste

**Défi** : Les règles `.nfo` sont en format texte libre.

**Solution** :
- Parser robuste avec regex et analyse syntaxique
- Extraction structurée des spécifications
- Validation manuelle si parsing ambigu
- Tests avec toutes les règles disponibles

---

## 🔄 Plan d'Action Immédiat

### Priorité 1 : Analyse Règle [2022] eBOOK

1. **Télécharger** la règle complète depuis scenerules.org
2. **Analyser** structure et contenu
3. **Extraire** toutes les spécifications
4. **Documenter** dans `docs/SCENE_RULES_EBOOK_2022.md`

### Priorité 2 : Implémentation Parser

1. **Créer** `RuleParserService` pour parsing règles `.nfo`
2. **Implémenter** extraction spécifications EBOOK
3. **Tests** avec règle [2022] eBOOK
4. **Valider** parsing complet et correct

### Priorité 3 : Intégration Packaging

1. **Mettre à jour** `PackagingService` pour utiliser règles parsées
2. **Valider** chaque étape selon règles extraites
3. **Tests** conformité complète
4. **Documentation** processus de validation

---

## ✅ Checklist Validation Règles EBOOK

### Analyse Règle
- [ ] Règle [2022] eBOOK téléchargée et analysée
- [ ] Formats fichiers acceptés identifiés
- [ ] Structure nommage extraite
- [ ] Fichiers requis identifiés (ZIP, RAR, NFO, DIZ, SFV)
- [ ] Exigences validation identifiées
- [ ] Spécifications techniques documentées

### Implémentation
- [ ] Parser de règles implémenté
- [ ] Validation format fichier selon règle
- [ ] Validation nommage selon règle
- [ ] Génération structure conforme
- [ ] Tests conformité 100%

### Documentation
- [ ] Règle complète documentée dans projet
- [ ] Spécifications techniques extraites
- [ ] PRD-002 mis à jour avec détails règles
- [ ] Guide packaging conforme créé

---

**⚠️ CRITIQUE** : Avant de commencer Phase 3 (Wizard), la règle [2022] eBOOK DOIT être analysée intégralement et les spécifications intégrées dans le service de packaging.

---

**Dernière mise à jour** : 2025-11-01  
**Statut** : ⚠️ Action requise avant Phase 3

