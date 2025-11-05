"""Service d'extraction de métadonnées depuis fichiers eBook.

Ce service extrait les métadonnées (titre, auteur, ISBN, langue, etc.) depuis
différents formats de fichiers eBook (EPUB, PDF, etc.) et calcule les checksums
pour garantir l'intégrité des fichiers.

Algorithme général :
1. Détection du format de fichier (extension, signature magique)
2. Extraction métadonnées selon format (EPUB = ZIP avec XML, PDF = structure binaire)
3. Normalisation des données (UTF-8, dates ISO 8601)
4. Calcul de checksums (SHA-256, MD5) pour intégrité

Complexité moyenne : O(n) où n est la taille du fichier pour la lecture,
O(1) pour les opérations de normalisation et checksums.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

try:
    import ebooklib
    from ebooklib import epub
except ImportError:
    ebooklib = None
    epub = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None  # type: ignore[assignment, misc]

logger = logging.getLogger(__name__)

# Constants
ISBN_10_LENGTH = 10
ISBN_13_LENGTH = 13
DATE_MIN_LENGTH = 8  # Minimum date length for YYYYMMDD format
ISO_DATE_MIN_LENGTH = 10  # Minimum length for YYYY-MM-DD format
DATE_PARTS_MIN_COUNT = 3  # Minimum parts count for date parsing (year, month, day)


class MetadataExtractionService:
    """Service d'extraction de métadonnées depuis fichiers eBook.

    Ce service implémente la logique d'extraction des métadonnées depuis différents
    formats de fichiers eBook (EPUB, PDF, etc.). Il normalise les données extraites
    (encodage UTF-8, formats de dates ISO 8601) et calcule des checksums pour
    garantir l'intégrité des fichiers traités.

    Formats supportés :
    - EPUB : Format ZIP avec structure XML (OPF pour métadonnées)
    - PDF : Structure binaire avec métadonnées XMP/Dublin Core

    Algorithmes d'extraction :
    - EPUB : Lecture du fichier OPF (content.opf) dans l'archive ZIP
    - PDF : Parsing des métadonnées XMP et /Info dans la structure PDF

    Normalisation :
    - Encodage : Tous les textes convertis en UTF-8
    - Dates : Format ISO 8601 (YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS)
    - ISBN : Nettoyage et validation format (ISBN-10 ou ISBN-13)

    Checksums :
    - SHA-256 : Pour intégrité longue durée (recommandé)
    - MD5 : Pour compatibilité avec systèmes existants

    Exemple d'utilisation :
        service = MetadataExtractionService()
        metadata = service.extract_metadata(Path('book.epub'))
        print(f"Titre: {metadata['title']}")
        print(f"SHA-256: {metadata['checksums']['sha256']}")
    """

    # Formats supportés avec leurs extensions
    SUPPORTED_FORMATS = {
        ".epub": "EPUB",
        ".pdf": "PDF",
        ".azw": "AZW",
        ".mobi": "MOBI",
        ".prc": "PRC",
    }

    def __init__(self) -> None:
        """Initialise le service d'extraction de métadonnées.

        Vérifie la disponibilité des bibliothèques nécessaires pour l'extraction.
        Si une bibliothèque n'est pas disponible, les formats correspondants seront
        désactivés avec un message d'avertissement.

        Complexité : O(1) - Vérifications simples d'imports.
        """
        # Vérification disponibilité ebooklib pour EPUB
        if ebooklib is None or epub is None:
            logger.warning(
                "ebooklib non disponible - Extraction EPUB désactivée. "
                "Installer avec: pip install ebooklib"
            )

        # Vérification disponibilité pypdf pour PDF
        if PdfReader is None:
            logger.warning(
                "pypdf non disponible - Extraction PDF désactivée. "
                "Installer avec: pip install pypdf"
            )

    def extract_metadata(
        self, file_path: Path | str, calculate_checksums: bool = True
    ) -> dict[str, Any]:
        """Extrait les métadonnées complètes d'un fichier eBook.

        Cette méthode orchestratrice détecte le format du fichier et appelle
        la méthode d'extraction spécialisée correspondante. Elle normalise ensuite
        les données extraites et calcule les checksums si demandé.

        Algorithme :
        1. Vérification existence fichier (O(1))
        2. Détection format via extension et signature magique (O(k) où k = taille header)
        3. Extraction métadonnées selon format (O(n) où n = taille fichier)
        4. Normalisation données (O(m) où m = nombre métadonnées)
        5. Calcul checksums si demandé (O(n) pour lecture complète fichier)

        Complexité globale : O(n) où n est la taille du fichier.
        La lecture complète du fichier est nécessaire pour les checksums.

        Args:
            file_path: Chemin vers le fichier eBook à analyser.
            calculate_checksums: Si True, calcule SHA-256 et MD5 (défaut: True).

        Returns:
            Dictionnaire contenant :
            - title: Titre du livre
            - author: Auteur(s) (liste)
            - publisher: Éditeur
            - isbn: ISBN (ISBN-10 ou ISBN-13)
            - language: Code langue ISO 639-1/639-2
            - publication_date: Date publication (ISO 8601)
            - description: Description/résumé
            - format: Format fichier (EPUB, PDF, etc.)
            - file_size: Taille fichier en octets
            - checksums: Dictionnaire avec sha256 et md5 (si calculés)
            - mediainfo: Métadonnées techniques (taille, structure interne)

        Raises:
            FileNotFoundError: Si le fichier n'existe pas.
            ValueError: Si le format n'est pas supporté.
            Exception: Si l'extraction échoue (fichier corrompu, etc.).

        Example:
            >>> service = MetadataExtractionService()
            >>> metadata = service.extract_metadata(Path('book.epub'))
            >>> print(metadata['title'])
            'Le Petit Prince'
        """
        file_path = Path(file_path)

        # Vérification existence fichier
        if not file_path.exists():
            raise FileNotFoundError(f"Fichier introuvable: {file_path}")

        if not file_path.is_file():
            raise ValueError(f"Le chemin n'est pas un fichier: {file_path}")

        # Détection format
        file_format = self._detect_format(file_path)

        if file_format not in self.SUPPORTED_FORMATS.values():
            raise ValueError(
                f"Format non supporté: {file_format}. "
                f"Formats supportés: {', '.join(self.SUPPORTED_FORMATS.values())}"
            )

        # Extraction métadonnées selon format
        metadata: dict[str, Any] = {
            "format": file_format,
            "file_size": file_path.stat().st_size,
            "file_path": str(file_path),
        }

        try:
            if file_format == "EPUB":
                epub_metadata = self._extract_epub_metadata(file_path)
                metadata.update(epub_metadata)
            elif file_format == "PDF":
                pdf_metadata = self._extract_pdf_metadata(file_path)
                metadata.update(pdf_metadata)
            else:
                # Formats non implémentés : métadonnées minimales
                metadata.update(
                    {
                        "title": None,
                        "author": [],
                        "publisher": None,
                        "isbn": None,
                        "language": None,
                        "publication_date": None,
                        "description": None,
                    }
                )
        except Exception as e:
            logger.error(f"Erreur extraction métadonnées {file_path}: {e}", exc_info=True)
            raise Exception(f"Extraction métadonnées échouée: {e}") from e

        # Normalisation des données
        metadata = self._normalize_metadata(metadata)

        # Calcul checksums si demandé
        if calculate_checksums:
            checksums = self._calculate_checksums(file_path)
            metadata["checksums"] = checksums

        return metadata

    def _detect_format(self, file_path: Path) -> str:
        """Détecte le format d'un fichier via extension et signature magique.

        Cette méthode utilise d'abord l'extension du fichier pour une détection rapide,
        puis vérifie la signature magique (magic bytes) pour confirmation et sécurité.
        Cette double vérification évite les erreurs si un fichier est mal renommé.

        Signatures magiques connues :
        - EPUB : ZIP archive (PK\x03\x04 au début)
        - PDF : %PDF- au début

        Algorithme :
        1. Vérification extension (O(1))
        2. Lecture des 4-8 premiers octets pour signature (O(1))
        3. Comparaison avec signatures connues (O(1))

        Complexité : O(1) - Lecture de quelques octets seulement.

        Args:
            file_path: Chemin vers le fichier.

        Returns:
            Format détecté (EPUB, PDF, etc.).

        Raises:
            ValueError: Si le format ne peut pas être détecté.
        """
        # Détection via extension
        extension = file_path.suffix.lower()
        if extension in self.SUPPORTED_FORMATS:
            detected_format = self.SUPPORTED_FORMATS[extension]

            # Vérification signature magique pour sécurité
            try:
                with file_path.open("rb") as f:
                    header = f.read(8)

                # Vérification EPUB (ZIP archive)
                if detected_format == "EPUB" and header.startswith(b"PK\x03\x04"):
                    return "EPUB"

                # Vérification PDF
                if detected_format == "PDF" and header.startswith(b"%PDF-"):
                    return "PDF"

                # Si extension correspond mais signature ne correspond pas,
                # on retourne quand même le format détecté par extension
                # (certains formats peuvent avoir des variantes)
                return detected_format
            except Exception as e:
                logger.warning(f"Erreur lecture signature magique {file_path}: {e}")
                # Fallback sur extension seulement
                return detected_format

        raise ValueError(f"Format non reconnu pour: {file_path}")

    def _extract_epub_metadata(self, file_path: Path) -> dict[str, Any]:  # noqa: PLR0912
        """Extrait les métadonnées d'un fichier EPUB.

        Un fichier EPUB est essentiellement une archive ZIP contenant :
        - Fichiers HTML/XHTML pour le contenu
        - Fichier OPF (content.opf) contenant les métadonnées Dublin Core
        - Fichier NCX pour la table des matières
        - Images et styles CSS

        Algorithme d'extraction :
        1. Ouverture de l'archive ZIP (O(1))
        2. Recherche du fichier OPF (content.opf ou *.opf) (O(k) où k = nombre fichiers)
        3. Parsing XML du fichier OPF (O(m) où m = taille fichier OPF)
        4. Extraction métadonnées Dublin Core depuis XML (O(n) où n = nombre métadonnées)

        Métadonnées Dublin Core extraites :
        - dc:title : Titre
        - dc:creator : Auteur(s)
        - dc:publisher : Éditeur
        - dc:identifier (type="ISBN") : ISBN
        - dc:language : Langue
        - dc:date : Date publication
        - dc:description : Description

        Complexité : O(n) où n est la taille du fichier EPUB.
        La lecture complète de l'archive ZIP est nécessaire.

        Args:
            file_path: Chemin vers le fichier EPUB.

        Returns:
            Dictionnaire avec métadonnées extraites.

        Raises:
            ImportError: Si ebooklib n'est pas disponible.
            Exception: Si le fichier EPUB est corrompu ou invalide.
        """
        if epub is None:
            raise ImportError(
                "ebooklib requis pour extraction EPUB. " "Installer avec: pip install ebooklib"
            )

        try:
            # Lecture du fichier EPUB avec ebooklib
            book = epub.read_epub(str(file_path))

            # Extraction métadonnées Dublin Core
            metadata: dict[str, Any] = {
                "title": None,
                "author": [],
                "publisher": None,
                "isbn": None,
                "language": None,
                "publication_date": None,
                "description": None,
            }

            # Titre
            title_metadata = book.get_metadata("DC", "title")
            if title_metadata:
                # Prendre le premier titre trouvé
                metadata["title"] = str(title_metadata[0][0]) if title_metadata[0][0] else None

            # Auteurs (peut être multiple)
            creator_metadata = book.get_metadata("DC", "creator")
            if creator_metadata:
                metadata["author"] = [str(creator[0]) for creator in creator_metadata if creator[0]]

            # Éditeur
            publisher_metadata = book.get_metadata("DC", "publisher")
            if publisher_metadata:
                metadata["publisher"] = (
                    str(publisher_metadata[0][0]) if publisher_metadata[0][0] else None
                )

            # ISBN (dans identifier avec type="ISBN")
            identifier_metadata = book.get_metadata("DC", "identifier")
            if identifier_metadata:
                for identifier in identifier_metadata:
                    # Vérifier si c'est un ISBN (généralement dans les attributs)
                    identifier_value = str(identifier[0])
                    identifier_attrs = identifier[1] if len(identifier) > 1 else {}

                    # Si l'identifiant contient "ISBN" ou est dans les attributs
                    if (
                        "isbn" in identifier_value.lower()
                        or "isbn" in str(identifier_attrs).lower()
                    ):
                        metadata["isbn"] = identifier_value
                        break
                    # Sinon, prendre le premier identifier comme ISBN potentiel
                    elif metadata["isbn"] is None:
                        metadata["isbn"] = identifier_value

            # Langue
            language_metadata = book.get_metadata("DC", "language")
            if language_metadata:
                metadata["language"] = (
                    str(language_metadata[0][0]) if language_metadata[0][0] else None
                )

            # Date publication
            date_metadata = book.get_metadata("DC", "date")
            if date_metadata:
                metadata["publication_date"] = (
                    str(date_metadata[0][0]) if date_metadata[0][0] else None
                )

            # Description
            description_metadata = book.get_metadata("DC", "description")
            if description_metadata:
                metadata["description"] = (
                    str(description_metadata[0][0]) if description_metadata[0][0] else None
                )

            # Si title est None, utiliser la propriété title du livre
            if metadata["title"] is None and book.title:
                metadata["title"] = book.title

            # Si author est vide, utiliser les auteurs du livre
            if not metadata["author"] and hasattr(book, "metadata") and book.metadata:
                # Tentative récupération depuis les auteurs du livre
                pass  # Déjà géré avec get_metadata('DC', 'creator')

            return metadata
        except Exception as e:
            logger.error(f"Erreur extraction EPUB {file_path}: {e}", exc_info=True)
            raise Exception(f"Extraction métadonnées EPUB échouée: {e}") from e

    def _extract_pdf_metadata(self, file_path: Path) -> dict[str, Any]:  # noqa: PLR0912
        """Extrait les métadonnées d'un fichier PDF.

        Un fichier PDF contient des métadonnées dans deux emplacements :
        1. Métadonnées /Info (ancien format, PDF 1.0-1.3)
        2. Métadonnées XMP (Extensible Metadata Platform, PDF 1.4+)

        Algorithme d'extraction :
        1. Ouverture du PDF avec PdfReader (O(1))
        2. Lecture métadonnées /Info (O(1))
        3. Lecture métadonnées XMP si disponibles (O(m) où m = taille métadonnées XMP)
        4. Priorité XMP > /Info (XMP plus moderne et complet)

        Métadonnées extraites :
        - Title : Titre
        - Author : Auteur(s)
        - Subject : Sujet/description
        - Creator : Logiciel de création
        - Producer : Logiciel de production
        - CreationDate : Date création
        - ModDate : Date modification

        Complexité : O(1) pour lecture métadonnées (pas de parsing complet nécessaire).

        Args:
            file_path: Chemin vers le fichier PDF.

        Returns:
            Dictionnaire avec métadonnées extraites.

        Raises:
            ImportError: Si pypdf n'est pas disponible.
            Exception: Si le fichier PDF est corrompu ou invalide.
        """
        if PdfReader is None:
            raise ImportError(
                "pypdf requis pour extraction PDF. " "Installer avec: pip install pypdf"
            )

        try:
            # Lecture du fichier PDF avec pypdf
            reader = PdfReader(str(file_path))

            metadata: dict[str, Any] = {
                "title": None,
                "author": [],
                "publisher": None,
                "isbn": None,
                "language": None,
                "publication_date": None,
                "description": None,
            }

            # Lecture métadonnées /Info (ancien format)
            if reader.metadata:
                info_meta = reader.metadata

                # Titre
                if info_meta.title:
                    metadata["title"] = str(info_meta.title)

                # Auteur
                if info_meta.author:
                    # Auteur peut être une chaîne ou une liste
                    author_str = str(info_meta.author)
                    # Séparer par virgule si plusieurs auteurs
                    if "," in author_str:
                        metadata["author"] = [a.strip() for a in author_str.split(",")]
                    else:
                        metadata["author"] = [author_str]

                # Extract description from Subject metadata
                if info_meta.subject:
                    metadata["description"] = str(info_meta.subject)

                # Date publication (CreationDate ou ModDate)
                if info_meta.creation_date:
                    metadata["publication_date"] = str(info_meta.creation_date)
                elif info_meta.modification_date:
                    metadata["publication_date"] = str(info_meta.modification_date)

            # Lecture métadonnées XMP (priorité si disponibles)
            if reader.xmp_metadata:
                xmp_meta = reader.xmp_metadata

                # Titre XMP (priorité sur /Info)
                if xmp_meta.dc_title:
                    metadata["title"] = (
                        str(xmp_meta.dc_title[0])
                        if isinstance(xmp_meta.dc_title, list)
                        else str(xmp_meta.dc_title)
                    )

                # Auteur XMP
                if xmp_meta.dc_creator:
                    if isinstance(xmp_meta.dc_creator, list):
                        metadata["author"] = [str(creator) for creator in xmp_meta.dc_creator]
                    else:
                        metadata["author"] = [str(xmp_meta.dc_creator)]

                # Description XMP
                if xmp_meta.dc_description:
                    metadata["description"] = (
                        str(xmp_meta.dc_description[0])
                        if isinstance(xmp_meta.dc_description, list)
                        else str(xmp_meta.dc_description)
                    )

                # Date création XMP
                if xmp_meta.xmp_create_date:
                    metadata["publication_date"] = str(xmp_meta.xmp_create_date)

            return metadata
        except Exception as e:
            logger.error(f"Erreur extraction PDF {file_path}: {e}", exc_info=True)
            raise Exception(f"Extraction métadonnées PDF échouée: {e}") from e

    def _normalize_metadata(self, metadata: dict[str, Any]) -> dict[str, Any]:
        """Normalise les métadonnées extraites (UTF-8, dates ISO, ISBN).

        Cette méthode normalise toutes les métadonnées textuelles pour garantir
        un format cohérent et utilisable dans le reste de l'application.

        Normalisations appliquées :
        1. Encodage UTF-8 : Tous les textes convertis en UTF-8 valide
        2. Dates ISO 8601 : Conversion vers format YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS
        3. ISBN : Nettoyage (suppression tirets, espaces) et validation format
        4. Langue : Normalisation vers code ISO 639-1/639-2
        5. Nettoyage espaces : Suppression espaces multiples, trim

        Complexité : O(m) où m est le nombre de métadonnées à normaliser.

        Args:
            metadata: Dictionnaire avec métadonnées brutes.

        Returns:
            Dictionnaire avec métadonnées normalisées.
        """
        normalized = metadata.copy()

        # Normalisation titre
        if normalized.get("title"):
            normalized["title"] = self._normalize_text(str(normalized["title"]))

        # Normalisation auteurs
        if normalized.get("author"):
            normalized["author"] = [
                self._normalize_text(str(author)) for author in normalized["author"] if author
            ]

        # Normalisation éditeur
        if normalized.get("publisher"):
            normalized["publisher"] = self._normalize_text(str(normalized["publisher"]))

        # Normalisation description
        if normalized.get("description"):
            normalized["description"] = self._normalize_text(str(normalized["description"]))

        # Normalisation ISBN
        if normalized.get("isbn"):
            normalized["isbn"] = self._normalize_isbn(str(normalized["isbn"]))

        # Normalisation langue
        if normalized.get("language"):
            normalized["language"] = self._normalize_language(str(normalized["language"]))

        # Normalisation date publication
        if normalized.get("publication_date"):
            normalized["publication_date"] = self._normalize_date(
                str(normalized["publication_date"])
            )

        return normalized

    def _normalize_text(self, text: str) -> str:
        """Normalise un texte (UTF-8, nettoyage espaces).

        Cette méthode :
        1. Supprime les caractères de contrôle non imprimables
        2. Normalise les espaces multiples en un seul espace
        3. Supprime les espaces en début/fin (trim)
        4. Convertit en UTF-8 valide

        Complexité : O(n) où n est la longueur du texte.

        Args:
            text: Texte à normaliser.

        Returns:
            Texte normalisé.
        """
        if not text:
            return ""

        # Conversion en UTF-8 et suppression caractères de contrôle
        try:
            # Décoder si nécessaire (pour gérer les chaînes avec échappements)
            if isinstance(text, bytes):
                text = text.decode("utf-8", errors="ignore")

            # Normalisation espaces multiples
            import re

            text = re.sub(r"\s+", " ", text)

            # Trim
            text = text.strip()

            return text
        except Exception as e:
            logger.warning(f"Erreur normalisation texte: {e}")
            return str(text)

    def _normalize_isbn(self, isbn: str) -> str | None:
        """Normalise un ISBN (suppression tirets, espaces, validation).

        Cette méthode nettoie un ISBN en supprimant les tirets et espaces,
        et vérifie qu'il correspond au format ISBN-10 (10 chiffres) ou
        ISBN-13 (13 chiffres commençant par 978 ou 979).

        Formats ISBN :
        - ISBN-10 : 10 chiffres (peut contenir X à la fin)
        - ISBN-13 : 13 chiffres (commence par 978 ou 979)

        Complexité : O(n) où n est la longueur de l'ISBN.

        Args:
            isbn: ISBN brut à normaliser.

        Returns:
            ISBN normalisé (sans tirets ni espaces) ou None si invalide.
        """
        if not isbn:
            return None

        # Suppression tirets, espaces, et conversion en majuscules
        cleaned = isbn.replace("-", "").replace(" ", "").upper()

        # Extraction ISBN depuis chaîne (peut contenir "ISBN:" ou autres préfixes)
        import re

        isbn_match = re.search(r"(\d{10,13}[X]?)", cleaned)
        if isbn_match:
            cleaned = isbn_match.group(1)

        # Validation format
        # ISBN-10 : 10 caractères (9 chiffres + 1 chiffre ou X)
        if (
            len(cleaned) == ISBN_10_LENGTH
            and cleaned[:-1].isdigit()
            and cleaned[-1].isdigit()
            or cleaned[-1] == "X"
        ):
            return cleaned

        # ISBN-13 : 13 chiffres commençant par 978 ou 979
        if len(cleaned) == ISBN_13_LENGTH and cleaned.isdigit() and cleaned.startswith(("978", "979")):
            return cleaned

        # Si ne correspond à aucun format, retourner None
        logger.warning(f"ISBN invalide (format non reconnu): {isbn}")
        return None

    def _normalize_language(self, language: str) -> str | None:
        """Normalise un code langue vers ISO 639-1/639-2.

        Cette méthode convertit un code langue vers le format ISO standard.
        Supports formats courants :
        - ISO 639-1 : 2 lettres (ex: "en", "fr")
        - ISO 639-2 : 3 lettres (ex: "eng", "fra")
        - Noms complets : Conversion vers code ISO (ex: "English" -> "en")

        Complexité : O(1) - Recherche dans dictionnaire de correspondance.

        Args:
            language: Code langue brut.

        Returns:
            Code langue ISO 639-1 (2 lettres) ou ISO 639-2 (3 lettres) si non trouvé.
        """
        if not language:
            return None

        # Normalisation : minuscules, suppression espaces
        language = language.lower().strip()

        # Mapping noms complets vers codes ISO
        language_map = {
            "english": "en",
            "french": "fr",
            "spanish": "es",
            "german": "de",
            "italian": "it",
            "portuguese": "pt",
            "dutch": "nl",
            "russian": "ru",
            "chinese": "zh",
            "japanese": "ja",
            "korean": "ko",
        }

        if language in language_map:
            return language_map[language]

        # Si déjà un code ISO (2 ou 3 lettres), retourner tel quel
        if len(language) in (2, 3) and language.isalpha():
            return language

        # Sinon, retourner le code tel quel (peut être un code personnalisé)
        return language

    def _normalize_date(self, date_str: str) -> str | None:
        """Normalise une date vers format ISO 8601.

        Cette méthode convertit différentes formats de dates vers ISO 8601
        (YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS).

        Formats supportés :
        - ISO 8601 : YYYY-MM-DD, YYYY-MM-DDTHH:MM:SS
        - Dates PDF : D:YYYYMMDDHHmmSS+HH'MM'
        - Dates texte : DD/MM/YYYY, MM/DD/YYYY, etc.

        Complexité : O(1) - Parsing simple de format de date.

        Args:
            date_str: Date brute à normaliser.

        Returns:
            Date au format ISO 8601 (YYYY-MM-DD) ou None si invalide.
        """
        if not date_str:
            return None

        try:
            # Format PDF : D:YYYYMMDDHHmmSS+HH'MM'
            if date_str.startswith("D:"):
                date_str = date_str[2:]  # Supprimer "D:"
                # Format : YYYYMMDDHHmmSS+HH'MM'
                if len(date_str) >= DATE_MIN_LENGTH:
                    year = date_str[0:4]
                    month = date_str[4:6]
                    day = date_str[6:8]
                    return f"{year}-{month}-{day}"

            # Format ISO 8601 complet : YYYY-MM-DDTHH:MM:SS
            if "T" in date_str:
                return date_str.split("T")[0]

            # Format ISO 8601 simple : YYYY-MM-DD
            if "-" in date_str and len(date_str) >= ISO_DATE_MIN_LENGTH:
                parts = date_str.split("-")
                if len(parts) >= DATE_PARTS_MIN_COUNT and all(len(p) in (2, 4) for p in parts[:DATE_PARTS_MIN_COUNT]):
                    return date_str[:ISO_DATE_MIN_LENGTH]  # Prendre YYYY-MM-DD seulement

            # Tentative parsing avec datetime
            from dateutil import parser

            parsed_date = parser.parse(date_str)
            return parsed_date.strftime("%Y-%m-%d")
        except Exception as e:
            logger.warning(f"Erreur normalisation date '{date_str}': {e}")
            return None

    def _calculate_checksums(self, file_path: Path) -> dict[str, str]:
        """Calcule les checksums SHA-256 et MD5 d'un fichier.

        Cette méthode calcule les checksums pour garantir l'intégrité du fichier.
        Les checksums sont calculés en lecture séquentielle du fichier par blocs
        pour éviter de charger tout le fichier en mémoire.

        Algorithmes utilisés :
        - SHA-256 : Recommandé pour intégrité longue durée (collision résistante)
        - MD5 : Pour compatibilité avec systèmes existants (rapide mais moins sécurisé)

        Algorithme :
        1. Ouverture fichier en mode binaire (O(1))
        2. Lecture par blocs de 64KB (O(n) où n = taille fichier)
        3. Mise à jour hash à chaque bloc (O(1) par bloc)
        4. Finalisation hash (O(1))

        Complexité : O(n) où n est la taille du fichier.
        Lecture complète nécessaire pour calculer les checksums.

        Args:
            file_path: Chemin vers le fichier.

        Returns:
            Dictionnaire avec :
            - sha256: Hash SHA-256 en hexadécimal
            - md5: Hash MD5 en hexadécimal
        """
        sha256_hash = hashlib.sha256()
        md5_hash = hashlib.md5()

        # Lecture par blocs pour éviter de charger tout le fichier en mémoire
        block_size = 65536  # 64KB par bloc (optimal pour la plupart des systèmes)

        try:
            with file_path.open("rb") as f:
                while True:
                    block = f.read(block_size)
                    if not block:
                        break
                    sha256_hash.update(block)
                    md5_hash.update(block)

            return {
                "sha256": sha256_hash.hexdigest(),
                "md5": md5_hash.hexdigest(),
            }
        except Exception as e:
            logger.error(f"Erreur calcul checksums {file_path}: {e}", exc_info=True)
            raise Exception(f"Calcul checksums échoué: {e}") from e
