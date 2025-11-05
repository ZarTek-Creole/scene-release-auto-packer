"""Service de téléchargement des règles Scene depuis scenerules.org.

Ce service gère le téléchargement et la synchronisation des règles Scene depuis
le site scenerules.org, qui est la référence officielle pour les règles de
nommage et packaging des releases Scene.

Architecture :
- Utilise requests.Session pour réutiliser les connexions HTTP
- Gère les timeouts et erreurs réseau
- Supporte les formats NFO (ASCII art) et HTML
- Gère les encodages UTF-8 et ISO-8859-1 (standard pour fichiers NFO)

Complexité moyenne : O(1) pour la plupart des opérations, avec dépendance
à la latence réseau pour les téléchargements.

Note importante : Les règles Scene sont disponibles en plusieurs formats :
- NFO : Format ASCII art standard (80 colonnes max)
- HTML : Version formatée pour lecture web

Les URLs suivent le pattern : /nfo/{year}_{section}.nfo
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urljoin

import requests


class ScenerulesDownloadService:
    """Service de téléchargement et gestion des règles Scene depuis scenerules.org.

    Ce service permet de télécharger les règles Scene officielles depuis
    scenerules.org, qui est la référence standard pour les règles de nommage
    et packaging des releases Scene.

    Fonctionnalités :
    - Liste des règles disponibles
    - Téléchargement par section et année
    - Téléchargement par URL directe
    - Vérification d'existence d'une règle

    Exemple d'utilisation :
        service = ScenerulesDownloadService()
        rules = service.list_available_rules()
        rule_data = service.download_rule("eBOOK", year=2022)
        exists = service.check_rule_exists("eBOOK", year=2022)
    """

    BASE_URL = "https://scenerules.org"
    NFO_URL_TEMPLATE = "{base_url}/nfo/{year}_{section}.nfo"
    HTML_URL_TEMPLATE = "{base_url}/html/{year}_{section}.html"

    def __init__(self, timeout: int = 30) -> None:
        """Initialise le service de téléchargement.

        Cette méthode configure une session HTTP réutilisable avec un User-Agent
        personnalisé et un timeout configurable. L'utilisation de requests.Session
        permet de réutiliser les connexions TCP, améliorant les performances
        lors de multiples téléchargements.

        Algorithme :
        1. Création d'une session HTTP réutilisable
        2. Configuration du User-Agent pour identification
        3. Configuration du timeout pour éviter les blocages

        Complexité : O(1) - Initialisation simple sans dépendances externes.

        Pièges potentiels :
        - Le timeout doit être suffisant pour les téléchargements lents
        - Le User-Agent peut être bloqué par certains serveurs (rare)
        - La session doit être fermée si le service n'est plus utilisé
          (mais généralement géré automatiquement par le garbage collector)

        Args:
            timeout: Timeout en secondes pour les requêtes HTTP (défaut: 30).
                     Doit être adapté selon la vitesse de connexion réseau.
        """
        self.timeout = timeout
        # Création d'une session HTTP réutilisable
        # Avantage : réutilisation des connexions TCP, amélioration des performances
        self.session = requests.Session()
        # Configuration du User-Agent pour identification dans les logs serveur
        # Format : "ApplicationName/Version"
        self.session.headers.update(
            {
                "User-Agent": "eBook-Scene-Packer-v2/1.0",
            }
        )

    def list_available_rules(self) -> list[dict[str, Any]]:
        """Liste les règles disponibles sur scenerules.org.

        Cette méthode retourne une liste des règles Scene connues avec leurs
        métadonnées (nom, section, année, URLs). Actuellement, cette liste est
        statique basée sur les règles connues. En production, cette méthode
        pourrait scraper la page d'index de scenerules.org pour obtenir une
        liste dynamique.

        Algorithme :
        1. Construction d'une liste statique de règles connues
        2. Génération des URLs NFO et HTML pour chaque règle
        3. Retour de la liste complète avec métadonnées

        Complexité : O(1) - Liste statique, pas de traitement complexe.

        Structure des métadonnées retournées :
        - name : Nom complet de la règle (ex: "[2022] eBOOK")
        - section : Section Scene (ex: "eBOOK", "TV-720p")
        - year : Année de la règle (ex: 2022)
        - scene : Nom de la scène (ex: "English")
        - url_nfo : URL du fichier NFO
        - url_html : URL de la version HTML

        Note : Cette implémentation utilise une liste statique. Pour une
        implémentation complète, il faudrait :
        - Scraper la page d'index de scenerules.org
        - Parser le HTML pour extraire les règles disponibles
        - Construire dynamiquement la liste des règles

        Pièges potentiels :
        - La liste statique peut être obsolète si de nouvelles règles sont ajoutées
        - Les URLs peuvent changer si la structure du site évolue
        - Pas de vérification que les règles listées existent réellement

        Returns:
            Liste de dictionnaires contenant les métadonnées de chaque règle disponible.
            Chaque dictionnaire contient : name, section, year, scene, url_nfo, url_html.
        """
        # Liste statique des règles connues
        # NOTE : Future improvement - En production, scraper la page d'index pour obtenir
        # une liste dynamique. Cette amélioration nécessiterait :
        # - Scraping HTML de la page d'index scenerules.org
        # - Parsing HTML pour extraire les règles disponibles
        # - Construction dynamique de la liste
        # Voir issue #XXX ou ADR pour détails d'implémentation
        known_rules = [
            {
                "name": "[2022] eBOOK",
                "section": "eBOOK",
                "year": 2022,
                "scene": "English",
                "url_nfo": urljoin(self.BASE_URL, "/nfo/2022_eBOOK.nfo"),
                "url_html": urljoin(self.BASE_URL, "/html/2022_eBOOK.html"),
            },
            {
                "name": "[2022] TV-720p",
                "section": "TV-720p",
                "year": 2022,
                "scene": "English",
                "url_nfo": urljoin(self.BASE_URL, "/nfo/2022_TV-720p.nfo"),
                "url_html": urljoin(self.BASE_URL, "/html/2022_TV-720p.html"),
            },
            {
                "name": "[2022] TV-SD",
                "section": "TV-SD",
                "year": 2022,
                "scene": "English",
                "url_nfo": urljoin(self.BASE_URL, "/nfo/2022_TV-SD.nfo"),
                "url_html": urljoin(self.BASE_URL, "/html/2022_TV-SD.html"),
            },
            {
                "name": "[2022] X264",
                "section": "X264",
                "year": 2022,
                "scene": "English",
                "url_nfo": urljoin(self.BASE_URL, "/nfo/2022_X264.nfo"),
                "url_html": urljoin(self.BASE_URL, "/html/2022_X264.html"),
            },
            {
                "name": "[2022] X265",
                "section": "X265",
                "year": 2022,
                "scene": "English",
                "url_nfo": urljoin(self.BASE_URL, "/nfo/2022_X265.nfo"),
                "url_html": urljoin(self.BASE_URL, "/html/2022_X265.html"),
            },
        ]

        return known_rules

    def download_rule(
        self, section: str, year: int = 2022, scene: str = "English"
    ) -> dict[str, Any]:
        """Télécharge une règle Scene depuis scenerules.org.

        Cette méthode télécharge le fichier NFO d'une règle Scene spécifique
        depuis scenerules.org et retourne son contenu avec les métadonnées.

        Algorithme :
        1. Nettoyage du nom de section (remplacement espaces par underscores)
        2. Construction de l'URL NFO selon le template : /nfo/{year}_{section}.nfo
        3. Requête HTTP GET avec timeout
        4. Vérification du statut HTTP (raise_for_status)
        5. Décodage du contenu (UTF-8 en priorité, fallback ISO-8859-1)
        6. Extraction des métadonnées et construction du dictionnaire de retour

        Complexité : O(1) pour les opérations locales, dépend de la latence
        réseau pour le téléchargement (O(n) où n est la taille du fichier).

        Gestion des encodages :
        - UTF-8 en priorité (standard moderne)
        - ISO-8859-1 en fallback (standard pour fichiers NFO ASCII art)
        - Les fichiers NFO Scene utilisent souvent ISO-8859-1 pour les caractères
          spéciaux ASCII art (box-drawing characters)

        Gestion des erreurs :
        - HTTP 404 : ValueError levée avec message explicite
        - Autres erreurs HTTP : RequestException levée
        - Erreurs réseau : RequestException levée avec détails

        Pièges potentiels :
        - Les espaces dans les noms de sections doivent être remplacés par "_"
        - Certains serveurs peuvent bloquer les User-Agents non standards
        - Le timeout doit être suffisant pour les fichiers volumineux
        - Les fichiers NFO peuvent être très volumineux (ASCII art)

        Format URL :
        - Template : "https://scenerules.org/nfo/{year}_{section}.nfo"
        - Exemple : "https://scenerules.org/nfo/2022_eBOOK.nfo"

        Args:
            section: Section de la règle (ex: "eBOOK", "TV-720p", "X264").
            year: Année de la règle (défaut: 2022). Les règles Scene sont généralement
                  mises à jour annuellement.
            scene: Nom de la scène (défaut: "English"). La plupart des règles sont
                   en anglais, mais certaines scènes ont des règles spécifiques.

        Returns:
            Dictionnaire contenant les données de la règle :
            - name : Nom complet de la règle (ex: "[2022] eBOOK")
            - content : Contenu brut du fichier NFO (format ASCII art)
            - section : Section de la règle
            - year : Année de la règle
            - scene : Nom de la scène
            - source : Source de la règle (toujours "scenerules.org")
            - url : URL complète du fichier téléchargé

        Raises:
            ValueError: Si la règle n'existe pas (HTTP 404).
            requests.RequestException: Si le téléchargement échoue (erreur réseau,
                                        timeout, ou autre erreur HTTP).
        """
        # Nettoyage du nom de section pour l'URL
        # Les espaces sont remplacés par des underscores dans les URLs
        section_clean = section.replace(" ", "_")

        # Construction de l'URL selon le template
        url = self.NFO_URL_TEMPLATE.format(
            base_url=self.BASE_URL, year=year, section=section_clean
        )

        try:
            # Requête HTTP GET avec timeout configuré
            # La session réutilise les connexions TCP pour améliorer les performances
            response = self.session.get(url, timeout=self.timeout)

            # Vérification du statut HTTP
            # Lève une HTTPError si le statut est >= 400
            response.raise_for_status()

            # Décodage du contenu avec gestion des encodages
            # Essai UTF-8 en premier (standard moderne)
            try:
                content = response.text
            except UnicodeDecodeError:
                # Fallback vers ISO-8859-1 (standard pour fichiers NFO ASCII art)
                # Les fichiers NFO Scene utilisent souvent cet encodage pour les
                # caractères spéciaux ASCII art (box-drawing characters)
                content = response.content.decode("iso-8859-1")

            # Extraction des métadonnées depuis les paramètres
            # Construction du nom complet de la règle
            name = f"[{year}] {section}"
            if scene and scene != "English":
                # Ajout du nom de scène si différent de "English"
                name = f"[{scene}] {name}"

            # Construction du dictionnaire de retour avec toutes les métadonnées
            return {
                "name": name,
                "content": content,
                "section": section,
                "year": year,
                "scene": scene,
                "source": "scenerules.org",
                "url": url,
            }

        except requests.exceptions.HTTPError as e:
            # Gestion spécifique des erreurs HTTP
            if e.response.status_code == 404:
                # Règle non trouvée : ValueError avec message explicite
                raise ValueError(f"Rule not found: {section} [{year}]") from e
            # Autres erreurs HTTP : RequestException avec détails
            raise requests.RequestException(f"Failed to download rule: {e}") from e
        except requests.exceptions.RequestException as e:
            # Gestion des erreurs réseau (timeout, connexion, etc.)
            raise requests.RequestException(
                f"Network error downloading rule: {e}"
            ) from e

    def download_rule_by_url(self, url: str) -> dict[str, Any]:
        """Télécharge une règle depuis une URL spécifique.

        Cette méthode télécharge une règle Scene depuis une URL complète fournie
        directement, plutôt que de construire l'URL depuis section et année.
        Utile pour télécharger des règles depuis des URLs personnalisées ou
        des règles non standard.

        Algorithme :
        1. Requête HTTP GET avec timeout
        2. Vérification du statut HTTP
        3. Décodage du contenu (UTF-8 ou ISO-8859-1)
        4. Extraction des métadonnées depuis l'URL via regex
        5. Construction du dictionnaire de retour

        Complexité : O(1) pour les opérations locales, dépend de la latence
        réseau pour le téléchargement.

        Extraction des métadonnées depuis l'URL :
        - Pattern regex : `/(\\d{4})_([A-Za-z0-9-]+)\\.nfo$`
        - Capture l'année (4 chiffres) et la section (lettres, chiffres, tirets)
        - Si le pattern ne match pas, utilise des valeurs par défaut

        Pièges potentiels :
        - L'URL doit pointer vers un fichier NFO valide
        - La regex peut échouer pour des URLs non standard
        - Pas de validation que l'URL pointe vers scenerules.org

        Args:
            url: URL complète vers le fichier NFO de la règle.
                 Format attendu : "https://scenerules.org/nfo/{year}_{section}.nfo"

        Returns:
            Dictionnaire contenant les données de la règle :
            - name : Nom complet de la règle (ex: "[2022] eBOOK")
            - content : Contenu brut du fichier NFO
            - section : Section extraite de l'URL (ou "Unknown" si échec)
            - year : Année extraite de l'URL (ou 2022 par défaut)
            - scene : Nom de la scène (défaut: "English")
            - source : Source de la règle ("scenerules.org")
            - url : URL complète utilisée

        Raises:
            requests.RequestException: Si le téléchargement échoue (erreur réseau,
                                        timeout, ou erreur HTTP).
        """
        try:
            # Requête HTTP GET avec timeout configuré
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            # Décodage du contenu avec gestion des encodages
            # Même logique que download_rule : UTF-8 puis ISO-8859-1
            try:
                content = response.text
            except UnicodeDecodeError:
                content = response.content.decode("iso-8859-1")

            # Extraction des métadonnées depuis l'URL via regex
            # Pattern : /{year}_{section}.nfo à la fin de l'URL
            # Exemple : "https://scenerules.org/nfo/2022_eBOOK.nfo"
            # Capture : year=2022, section="eBOOK"
            match = re.search(r"/(\d{4})_([A-Za-z0-9-]+)\.nfo$", url)
            if match:
                year = int(match.group(1))  # Année extraite (4 chiffres)
                section = match.group(2).replace("_", " ")  # Section avec espaces restaurés
            else:
                # Valeurs par défaut si le pattern ne match pas
                year = 2022
                section = "Unknown"

            # Construction du nom complet de la règle
            name = f"[{year}] {section}"

            return {
                "name": name,
                "content": content,
                "section": section,
                "year": year,
                "scene": "English",  # Par défaut, pourrait être extrait du contenu
                "source": "scenerules.org",
                "url": url,
            }

        except requests.exceptions.RequestException as e:
            # Gestion des erreurs réseau et HTTP
            raise requests.RequestException(
                f"Failed to download rule from URL: {e}"
            ) from e

    def check_rule_exists(self, section: str, year: int = 2022) -> bool:
        """Vérifie si une règle existe sur scenerules.org.

        Cette méthode vérifie l'existence d'une règle sans télécharger son contenu,
        en utilisant une requête HEAD (plus légère qu'un GET complet). Utile pour
        vérifier rapidement si une règle est disponible avant de la télécharger.

        Algorithme :
        1. Nettoyage du nom de section (espaces → underscores)
        2. Construction de l'URL selon le template
        3. Requête HTTP HEAD (sans corps de réponse)
        4. Vérification du statut HTTP (200 = existe, autre = n'existe pas)

        Complexité : O(1) - Requête HEAD très rapide, pas de téléchargement de contenu.

        Avantages de HEAD vs GET :
        - Plus rapide : pas de téléchargement du contenu
        - Moins de bande passante utilisée
        - Idéal pour vérifier l'existence avant téléchargement

        Gestion des erreurs :
        - Toute exception réseau retourne False (safe default)
        - HTTP 200 = règle existe
        - HTTP 404 = règle n'existe pas
        - Autres erreurs = retourne False (safe default)

        Pièges potentiels :
        - Certains serveurs peuvent ne pas supporter HEAD (rare)
        - En cas d'erreur réseau, retourne False (peut être un faux négatif)
        - Ne vérifie pas que le contenu est valide, seulement l'existence

        Args:
            section: Section de la règle à vérifier (ex: "eBOOK", "TV-720p").
            year: Année de la règle à vérifier (défaut: 2022).

        Returns:
            True si la règle existe (HTTP 200), False sinon ou en cas d'erreur.
        """
        try:
            # Nettoyage du nom de section pour l'URL
            section_clean = section.replace(" ", "_")

            # Construction de l'URL selon le template
            url = self.NFO_URL_TEMPLATE.format(
                base_url=self.BASE_URL, year=year, section=section_clean
            )

            # Requête HTTP HEAD (sans téléchargement du contenu)
            # Plus rapide et économique en bande passante qu'un GET
            response = self.session.head(url, timeout=self.timeout)

            # HTTP 200 = règle existe, autre statut = n'existe pas ou erreur
            return response.status_code == 200
        except requests.exceptions.RequestException:
            # En cas d'erreur réseau, retourner False (safe default)
            # Cela évite de lever une exception, mais peut créer un faux négatif
            return False
