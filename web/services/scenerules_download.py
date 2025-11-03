"""Scenerules.org download service.

This service downloads Scene rules from scenerules.org and manages
synchronization with local rules.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urljoin

import requests


class ScenerulesDownloadService:
    """Download and manage rules from scenerules.org."""

    BASE_URL = "https://scenerules.org"
    NFO_URL_TEMPLATE = "{base_url}/nfo/{year}_{section}.nfo"
    HTML_URL_TEMPLATE = "{base_url}/html/{year}_{section}.html"

    def __init__(self, timeout: int = 30):
        """Initialize service.

        Args:
            timeout: Request timeout in seconds.
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "eBook-Scene-Packer-v2/1.0",
            }
        )

    def list_available_rules(self) -> list[dict[str, Any]]:
        """List available rules on scenerules.org.

        Returns:
            List of available rules with metadata.
        """
        # For now, return a curated list based on known rules
        # In production, this could scrape the index page
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
        """Download a rule from scenerules.org.

        Args:
            section: Rule section (eBOOK, TV-720p, etc.).
            year: Rule year (default: 2022).
            scene: Scene name (default: English).

        Returns:
            Dictionary with rule data:
            - name: Rule name
            - content: Rule content (NFO format)
            - section: Section
            - year: Year
            - scene: Scene name
            - source: "scenerules.org"

        Raises:
            requests.RequestException: If download fails.
            ValueError: If rule not found.
        """
        # Construct URL
        section_clean = section.replace(" ", "_")
        url = self.NFO_URL_TEMPLATE.format(
            base_url=self.BASE_URL, year=year, section=section_clean
        )

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            # Try UTF-8 first, fallback to ISO-8859-1 (common for NFO)
            try:
                content = response.text
            except UnicodeDecodeError:
                content = response.content.decode("iso-8859-1")

            # Extract metadata from content
            name = f"[{year}] {section}"
            if scene and scene != "English":
                name = f"[{scene}] {name}"

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
            if e.response.status_code == 404:
                raise ValueError(f"Rule not found: {section} [{year}]") from e
            raise requests.RequestException(f"Failed to download rule: {e}") from e
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(
                f"Network error downloading rule: {e}"
            ) from e

    def download_rule_by_url(self, url: str) -> dict[str, Any]:
        """Download a rule from a specific URL.

        Args:
            url: Full URL to the rule NFO file.

        Returns:
            Dictionary with rule data.

        Raises:
            requests.RequestException: If download fails.
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            # Try UTF-8 first, fallback to ISO-8859-1
            try:
                content = response.text
            except UnicodeDecodeError:
                content = response.content.decode("iso-8859-1")

            # Extract metadata from URL and content
            # URL format: https://scenerules.org/nfo/2022_eBOOK.nfo
            match = re.search(r"/(\d{4})_([A-Za-z0-9-]+)\.nfo$", url)
            if match:
                year = int(match.group(1))
                section = match.group(2).replace("_", " ")
            else:
                year = 2022
                section = "Unknown"

            name = f"[{year}] {section}"

            return {
                "name": name,
                "content": content,
                "section": section,
                "year": year,
                "scene": "English",  # Default, could be extracted from content
                "source": "scenerules.org",
                "url": url,
            }

        except requests.exceptions.RequestException as e:
            raise requests.RequestException(
                f"Failed to download rule from URL: {e}"
            ) from e

    def check_rule_exists(self, section: str, year: int = 2022) -> bool:
        """Check if a rule exists on scenerules.org.

        Args:
            section: Rule section.
            year: Rule year.

        Returns:
            True if rule exists, False otherwise.
        """
        try:
            section_clean = section.replace(" ", "_")
            url = self.NFO_URL_TEMPLATE.format(
                base_url=self.BASE_URL, year=year, section=section_clean
            )
            response = self.session.head(url, timeout=self.timeout)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
