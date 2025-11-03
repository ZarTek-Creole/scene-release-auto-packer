"""Tests for ScenerulesDownloadService."""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest
import requests

from web.services.scenerules_download import ScenerulesDownloadService


def test_list_available_rules():
    """Test list_available_rules returns list of rules."""
    service = ScenerulesDownloadService()
    rules = service.list_available_rules()

    assert isinstance(rules, list)
    assert len(rules) > 0
    assert all("name" in r for r in rules)
    assert all("section" in r for r in rules)
    assert all("year" in r for r in rules)
    assert all("url_nfo" in r for r in rules)


def test_download_rule_success():
    """Test download_rule success."""
    service = ScenerulesDownloadService()

    # Mock response
    mock_response = Mock()
    mock_response.text = "[2022] eBOOK Rules\nContent here."
    mock_response.content = mock_response.text.encode("utf-8")
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()

    with patch.object(service.session, "get", return_value=mock_response):
        result = service.download_rule("eBOOK", 2022)

        assert result["name"] == "[2022] eBOOK"
        assert result["section"] == "eBOOK"
        assert result["year"] == 2022
        assert result["content"] == "[2022] eBOOK Rules\nContent here."
        assert result["source"] == "scenerules.org"


def test_download_rule_not_found():
    """Test download_rule when rule not found."""
    service = ScenerulesDownloadService()

    # Mock 404 response
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status = Mock(
        side_effect=requests.exceptions.HTTPError(response=mock_response)
    )

    with patch.object(service.session, "get", return_value=mock_response):
        with pytest.raises(ValueError, match="Rule not found"):
            service.download_rule("Nonexistent", 2022)


def test_download_rule_by_url():
    """Test download_rule_by_url."""
    service = ScenerulesDownloadService()

    # Mock response
    mock_response = Mock()
    mock_response.text = "[2022] eBOOK Rules\nContent here."
    mock_response.content = mock_response.text.encode("utf-8")
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()

    with patch.object(service.session, "get", return_value=mock_response):
        url = "https://scenerules.org/nfo/2022_eBOOK.nfo"
        result = service.download_rule_by_url(url)

        assert result["name"] == "[2022] eBOOK"
        assert result["section"] == "eBOOK"
        assert result["year"] == 2022
        assert result["url"] == url


def test_check_rule_exists_true():
    """Test check_rule_exists returns True when rule exists."""
    service = ScenerulesDownloadService()

    # Mock HEAD response
    mock_response = Mock()
    mock_response.status_code = 200

    with patch.object(service.session, "head", return_value=mock_response):
        assert service.check_rule_exists("eBOOK", 2022) is True


def test_check_rule_exists_false():
    """Test check_rule_exists returns False when rule not found."""
    service = ScenerulesDownloadService()

    # Mock 404 response
    mock_response = Mock()
    mock_response.status_code = 404

    with patch.object(service.session, "head", return_value=mock_response):
        assert service.check_rule_exists("Nonexistent", 2022) is False


def test_check_rule_exists_network_error():
    """Test check_rule_exists handles network errors."""
    service = ScenerulesDownloadService()

    with patch.object(
        service.session, "head", side_effect=requests.exceptions.RequestException
    ):
        assert service.check_rule_exists("eBOOK", 2022) is False
