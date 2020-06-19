# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import re
from typing import Any, Dict, Literal, Pattern

from bs4 import BeautifulSoup
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import xmltodict

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


class PronomData:
    """Get BeautifulSoup and raw data from PRONOM."""

    base_url = "https://www.nationalarchives.gov.uk"
    url = "aboutapps/pronom/droid-signature-files.htm"

    def __init__(self) -> None:
        self.session: Session = Session()

        # Mount baseurl session with retries
        _retries: Retry = Retry(
            total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount(self.base_url, HTTPAdapter(max_retries=_retries))

    def raw_data(self) -> str:
        return self.session.get(f"{self.base_url}/{self.url}").text

    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.raw_data(), features="html.parser")

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
        link_data: str = self.session.get(f"{self.base_url}/{link}").text
        latest_file: Dict[Any, Any] = xmltodict.parse(link_data)
        return latest_file
