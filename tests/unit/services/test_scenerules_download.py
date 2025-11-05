"""Tests unitaires pour ScenerulesDownloadService.

Ces tests vérifient le téléchargement et la gestion des règles Scene depuis
scenerules.org avec mocks pour éviter les vraies requêtes HTTP.

Approche TDD : Tests écrits avant toute modification du service.
"""

from __future__ import annotations

from unittest.mock import MagicMock, Mock, patch

import pytest
import requests
from web.services.rule import ScenerulesDownloadService


class TestScenerulesDownloadService:
    """Tests unitaires pour ScenerulesDownloadService."""

    def test_init(self) -> None:
        """Test initialisation du service.
        
        Vérifie que le service s'initialise correctement avec timeout par défaut
        et session HTTP configurée.
        """
        service = ScenerulesDownloadService()
        
        assert service.timeout == 30
        assert service.session is not None
        assert service.session.headers["User-Agent"] == "eBook-Scene-Packer-v2/1.0"

    def test_init_custom_timeout(self) -> None:
        """Test initialisation avec timeout personnalisé.
        
        Vérifie que le timeout peut être personnalisé lors de l'initialisation.
        """
        service = ScenerulesDownloadService(timeout=60)
        
        assert service.timeout == 60

    def test_list_available_rules(self) -> None:
        """Test liste des règles disponibles.
        
        Vérifie que la méthode retourne une liste de règles avec métadonnées complètes.
        """
        service = ScenerulesDownloadService()
        rules = service.list_available_rules()
        
        assert isinstance(rules, list)
        assert len(rules) > 0
        
        # Vérification de la structure d'une règle
        rule = rules[0]
        assert "name" in rule
        assert "section" in rule
        assert "year" in rule
        assert "scene" in rule
        assert "url_nfo" in rule
        assert "url_html" in rule
        
        # Vérification que les URLs sont bien formées
        assert rule["url_nfo"].startswith("https://scenerules.org/nfo/")
        assert rule["url_html"].startswith("https://scenerules.org/html/")

    def test_download_rule_success(self) -> None:
        """Test téléchargement réussi d'une règle.
        
        Vérifie que la méthode télécharge correctement une règle et retourne
        les métadonnées attendues.
        """
        service = ScenerulesDownloadService()
        
        # Mock de la réponse HTTP
        mock_response = Mock()
        mock_response.text = "[2022] eBOOK\nOTHER\nPDF, EPUB"
        mock_response.content = b"[2022] eBOOK\nOTHER\nPDF, EPUB"
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        
        # Mock de la session
        service.session = Mock()
        service.session.get = Mock(return_value=mock_response)
        
        # Téléchargement de la règle
        result = service.download_rule("eBOOK", year=2022)
        
        # Vérifications
        assert result["name"] == "[2022] eBOOK"
        assert result["section"] == "eBOOK"
        assert result["year"] == 2022
        assert result["scene"] == "English"
        assert result["source"] == "scenerules.org"
        assert "[2022] eBOOK" in result["content"]
        assert "https://scenerules.org/nfo/2022_eBOOK.nfo" in result["url"]
        
        # Vérification que la requête a été appelée avec les bons paramètres
        service.session.get.assert_called_once()
        call_args = service.session.get.call_args
        assert "2022_eBOOK.nfo" in call_args[0][0]

    def test_download_rule_with_spaces(self) -> None:
        """Test téléchargement avec section contenant des espaces.
        
        Vérifie que les espaces dans les noms de sections sont correctement
        remplacés par des underscores dans l'URL.
        """
        service = ScenerulesDownloadService()
        
        # Mock de la réponse HTTP
        mock_response = Mock()
        mock_response.text = "[2022] TV-720p"
        mock_response.content = b"[2022] TV-720p"
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        
        # Mock de la session
        service.session = Mock()
        service.session.get = Mock(return_value=mock_response)
        
        # Téléchargement avec section contenant des espaces
        result = service.download_rule("TV 720p", year=2022)
        
        # Vérification que l'URL utilise des underscores
        call_args = service.session.get.call_args
        assert "2022_TV_720p.nfo" in call_args[0][0] or "2022_TV-720p.nfo" in call_args[0][0]

    def test_download_rule_custom_scene(self) -> None:
        """Test téléchargement avec scène personnalisée.
        
        Vérifie que le nom de la règle inclut la scène si elle est différente
        de "English".
        """
        service = ScenerulesDownloadService()
        
        # Mock de la réponse HTTP
        mock_response = Mock()
        mock_response.text = "Rule content"
        mock_response.content = b"Rule content"
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        
        # Mock de la session
        service.session = Mock()
        service.session.get = Mock(return_value=mock_response)
        
        # Téléchargement avec scène personnalisée
        result = service.download_rule("eBOOK", year=2022, scene="French")
        
        # Vérification que le nom inclut la scène
        assert result["name"] == "[French] [2022] eBOOK"
        assert result["scene"] == "French"

    def test_download_rule_not_found(self) -> None:
        """Test téléchargement d'une règle inexistante.
        
        Vérifie que la méthode lève une ValueError pour une règle non trouvée (404).
        """
        service = ScenerulesDownloadService()
        
        # Mock de la réponse HTTP avec 404
        mock_response = Mock()
        mock_response.status_code = 404
        
        # Mock de raise_for_status pour lever HTTPError
        http_error = requests.exceptions.HTTPError()
        http_error.response = mock_response
        mock_response.raise_for_status = Mock(side_effect=http_error)
        
        # Mock de la session
        service.session = Mock()
        service.session.get = Mock(return_value=mock_response)
        
        # Tentative de téléchargement (doit lever ValueError)
        with pytest.raises(ValueError, match="Rule not found"):
            service.download_rule("NonExistent", year=2022)

    def test_download_rule_network_error(self) -> None:
        """Test gestion des erreurs réseau.
        
        Vérifie que les erreurs réseau sont correctement gérées et propagées.
        """
        service = ScenerulesDownloadService()
        
        # Mock de la session pour lever une exception réseau
        service.session = Mock()
        service.session.get = Mock(side_effect=requests.exceptions.ConnectionError("Network error"))
        
        # Tentative de téléchargement (doit lever RequestException)
        with pytest.raises(requests.RequestException, match="Network error"):
            service.download_rule("eBOOK", year=2022)

    def test_download_rule_iso8859_encoding(self) -> None:
        """Test gestion de l'encodage ISO-8859-1.
        
        Vérifie que le service gère correctement les fichiers NFO encodés en
        ISO-8859-1 (fallback si UTF-8 échoue).
        """
        service = ScenerulesDownloadService()
        
        # Mock de la réponse HTTP avec encodage ISO-8859-1
        mock_response = Mock()
        # Simuler UnicodeDecodeError lors de l'accès à .text
        mock_response.content = b"\xe9\xe0\xe8"  # Caractères ISO-8859-1
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        
        # Créer une propriété qui lève UnicodeDecodeError
        def get_text():
            raise UnicodeDecodeError("utf-8", b"", 0, 1, "invalid")
        
        type(mock_response).text = property(lambda self: get_text())
        
        # Mock de la session
        service.session = Mock()
        service.session.get = Mock(return_value=mock_response)
        
        # Téléchargement (doit utiliser ISO-8859-1 en fallback)
        result = service.download_rule("eBOOK", year=2022)
        
        # Vérification que le contenu a été décodé
        assert "content" in result
        assert result["content"] == mock_response.content.decode("iso-8859-1")

    def test_download_rule_by_url_success(self) -> None:
        """Test téléchargement depuis URL spécifique.
        
        Vérifie que la méthode télécharge correctement une règle depuis une URL complète.
        """
        service = ScenerulesDownloadService()
        
        # Mock de la réponse HTTP
        mock_response = Mock()
        mock_response.text = "[2022] eBOOK\nOTHER\nPDF, EPUB"
        mock_response.content = b"[2022] eBOOK\nOTHER\nPDF, EPUB"
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        
        # Mock de la session
        service.session = Mock()
        service.session.get = Mock(return_value=mock_response)
        
        # Téléchargement depuis URL
        url = "https://scenerules.org/nfo/2022_eBOOK.nfo"
        result = service.download_rule_by_url(url)
        
        # Vérifications
        assert result["name"] == "[2022] eBOOK"
        assert result["section"] == "eBOOK"
        assert result["year"] == 2022
        assert result["url"] == url
        
        # Vérification que la requête a été appelée avec la bonne URL
        service.session.get.assert_called_once_with(url, timeout=30)

    def test_download_rule_by_url_extract_metadata(self) -> None:
        """Test extraction des métadonnées depuis l'URL.
        
        Vérifie que les métadonnées (année, section) sont correctement extraites
        de l'URL via regex.
        """
        service = ScenerulesDownloadService()
        
        # Mock de la réponse HTTP
        mock_response = Mock()
        mock_response.text = "Rule content"
        mock_response.content = b"Rule content"
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        
        # Mock de la session
        service.session = Mock()
        service.session.get = Mock(return_value=mock_response)
        
        # Téléchargement depuis URL avec métadonnées dans l'URL
        url = "https://scenerules.org/nfo/2023_TV-720p.nfo"
        result = service.download_rule_by_url(url)
        
        # Vérifications
        assert result["year"] == 2023
        assert result["section"] == "TV-720p"  # Underscores remplacés par espaces

    def test_download_rule_by_url_invalid_format(self) -> None:
        """Test téléchargement depuis URL avec format invalide.
        
        Vérifie que la méthode utilise des valeurs par défaut si l'URL ne
        correspond pas au format attendu.
        """
        service = ScenerulesDownloadService()
        
        # Mock de la réponse HTTP
        mock_response = Mock()
        mock_response.text = "Rule content"
        mock_response.content = b"Rule content"
        mock_response.status_code = 200
        mock_response.raise_for_status = Mock()
        
        # Mock de la session
        service.session = Mock()
        service.session.get = Mock(return_value=mock_response)
        
        # Téléchargement depuis URL avec format invalide
        url = "https://example.com/invalid-format.nfo"
        result = service.download_rule_by_url(url)
        
        # Vérifications : valeurs par défaut utilisées
        assert result["year"] == 2022
        assert result["section"] == "Unknown"
        assert result["name"] == "[2022] Unknown"

    def test_download_rule_by_url_error(self) -> None:
        """Test gestion des erreurs lors du téléchargement par URL.
        
        Vérifie que les erreurs sont correctement propagées.
        """
        service = ScenerulesDownloadService()
        
        # Mock de la session pour lever une exception
        service.session = Mock()
        service.session.get = Mock(side_effect=requests.exceptions.RequestException("Download failed"))
        
        # Tentative de téléchargement (doit lever RequestException)
        with pytest.raises(requests.RequestException, match="Failed to download rule from URL"):
            service.download_rule_by_url("https://scenerules.org/nfo/2022_eBOOK.nfo")

    def test_check_rule_exists_true(self) -> None:
        """Test vérification d'existence d'une règle (existe).
        
        Vérifie que la méthode retourne True pour une règle existante (HTTP 200).
        """
        service = ScenerulesDownloadService()
        
        # Mock de la réponse HTTP HEAD avec statut 200
        mock_response = Mock()
        mock_response.status_code = 200
        
        # Mock de la session
        service.session = Mock()
        service.session.head = Mock(return_value=mock_response)
        
        # Vérification de l'existence
        result = service.check_rule_exists("eBOOK", year=2022)
        
        # Vérifications
        assert result is True
        service.session.head.assert_called_once()
        call_args = service.session.head.call_args
        assert "2022_eBOOK.nfo" in call_args[0][0]

    def test_check_rule_exists_false(self) -> None:
        """Test vérification d'existence d'une règle (n'existe pas).
        
        Vérifie que la méthode retourne False pour une règle inexistante (HTTP 404).
        """
        service = ScenerulesDownloadService()
        
        # Mock de la réponse HTTP HEAD avec statut 404
        mock_response = Mock()
        mock_response.status_code = 404
        
        # Mock de la session
        service.session = Mock()
        service.session.head = Mock(return_value=mock_response)
        
        # Vérification de l'existence
        result = service.check_rule_exists("NonExistent", year=2022)
        
        # Vérifications
        assert result is False

    def test_check_rule_exists_network_error(self) -> None:
        """Test gestion des erreurs réseau lors de la vérification.
        
        Vérifie que la méthode retourne False en cas d'erreur réseau (safe default).
        """
        service = ScenerulesDownloadService()
        
        # Mock de la session pour lever une exception
        service.session = Mock()
        service.session.head = Mock(side_effect=requests.exceptions.ConnectionError("Network error"))
        
        # Vérification de l'existence (doit retourner False)
        result = service.check_rule_exists("eBOOK", year=2022)
        
        # Vérifications
        assert result is False

    def test_check_rule_exists_with_spaces(self) -> None:
        """Test vérification avec section contenant des espaces.
        
        Vérifie que les espaces sont correctement remplacés par des underscores.
        """
        service = ScenerulesDownloadService()
        
        # Mock de la réponse HTTP HEAD
        mock_response = Mock()
        mock_response.status_code = 200
        
        # Mock de la session
        service.session = Mock()
        service.session.head = Mock(return_value=mock_response)
        
        # Vérification avec section contenant des espaces
        service.check_rule_exists("TV 720p", year=2022)
        
        # Vérification que l'URL utilise des underscores
        call_args = service.session.head.call_args
        assert "2022_TV_720p.nfo" in call_args[0][0] or "2022_TV-720p.nfo" in call_args[0][0]

    @patch("web.services.rule.scenerules_download.requests.Session")
    def test_session_reuse(self, mock_session_class) -> None:
        """Test réutilisation de la session HTTP.
        
        Vérifie que la session HTTP est réutilisée pour améliorer les performances.
        """
        # Mock de la classe Session
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        service = ScenerulesDownloadService()
        
        # Vérification que la session a été créée une seule fois
        assert mock_session_class.called
        
        # Vérification que les headers ont été configurés
        mock_session.headers.update.assert_called_once()

