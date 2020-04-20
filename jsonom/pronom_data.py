# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import re
from typing import Any, Dict, Literal, Pattern

import requests
from bs4 import BeautifulSoup
from requests import Response

import xmltodict

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


class PronomData:
    """Get BeautifulSoup and text objects from PRONOM."""

    base_url = "https://www.nationalarchives.gov.uk"

    def __init__(self, url: str):
        self.url = url.strip("/")

    def text(self) -> str:
        response_data: Response = requests.get(f"{self.base_url}/{self.url}")
        return response_data.text

    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.text(), features="html.parser")

    def latest_file(
        self, file_type: Literal["signature", "container"]
    ) -> Dict[Any, Any]:
        href_match: Pattern
        if file_type == "signature":
            href_match = re.compile(r"(?i)signature\s?file")
        elif file_type == "container":
            href_match = re.compile(r"(?i)container")
        else:
            raise ValueError(
                "file_type must be either signature or container."
            )
        link: str = self.soup().find_all(href=href_match)[-1].get("href")
        link_data: str = requests.get(f"{self.base_url}/{link}").text
        latest_file: Dict[Any, Any] = xmltodict.parse(link_data)
        return latest_file
