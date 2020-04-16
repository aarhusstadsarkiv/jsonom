# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import re
from typing import List, Pattern, Literal, Optional
import xmltodict
import requests
from requests import Response
from bs4 import BeautifulSoup


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


class PronomData:
    """Get BeautifulSoup and text objects from PRONOM."""

    base_url = "https://www.nationalarchives.gov.uk"

    def __init__(self, url: str):
        self.url = url.strip("/")

    def text(self, url: Optional[str] = None) -> str:
        _url: str = url or self.url
        _url = _url.strip("/")
        response_data: Response = requests.get(f"{self.base_url}/{_url}")
        return response_data.text

    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.text(), features="html.parser")

    def latest_file(self, file_type: Literal["signature", "container"]) -> str:
        href_match: Pattern
        if file_type == "signature":
            href_match = re.compile(r"(?i)signature\s?file")
        elif file_type == "container":
            href_match = re.compile(r"(?i)container")
        link: str = self.soup().find_all(href=href_match)[-1].get("href")
        return self.text(link)


# -----------------------------------------------------------------------------
# Function Definitions
# -----------------------------------------------------------------------------


# def get_latest_file(href_match: str) -> str:
#     data = PronomData("aboutapps/pronom/droid-signature-files.htm")
#     links: List[str] = []
#     href_regex: Pattern = re.compile(href_match)
#     for link in data.get_soup().find_all(href=href_regex):
#         links.append(link.get("href"))
#     return PronomData(links[-1]).get_text()
