"""
QuickBooks Online API client.

Provides authenticated access to the QuickBooks Accounting API.
"""

import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()


class QuickBooksClient:
    """
    HTTP client for the QuickBooks Online Accounting API.
    """

    TOKEN_FILE = Path(".quickbooks_tokens.json")

    def __init__(self) -> None:
        self.environment = os.getenv(
            "QUICKBOOKS_ENVIRONMENT",
            "sandbox",
        )

        if not self.TOKEN_FILE.exists():
            raise FileNotFoundError(
                "QuickBooks token file not found. "
                "Run quickbooks_authorize.py first."
            )

        credentials = json.loads(
            self.TOKEN_FILE.read_text(encoding="utf-8")
        )

        self.access_token = credentials["access_token"]
        self.realm_id = credentials["realm_id"]

        if self.environment == "sandbox":
            self.base_url = (
                "https://sandbox-quickbooks.api.intuit.com"
            )
        else:
            self.base_url = (
                "https://quickbooks.api.intuit.com"
            )

        self.session = requests.Session()

        self.session.headers.update(
            {
                "Authorization":
                    f"Bearer {self.access_token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def get(
        self,
        endpoint: str,
        params: dict | None = None,
    ) -> dict:
        """
        Execute an authenticated GET request.
        """

        url = f"{self.base_url}{endpoint}"

        response = self.session.get(
            url,
            params=params,
            timeout=30,
        )

        if not response.ok:
            print(
                f"QuickBooks API request failed: "
                f"{response.status_code}"
            )
            print(response.text)

        response.raise_for_status()

        return response.json()

    def query(
        self,
        query: str,
    ) -> dict:
        """
        Execute a QuickBooks SQL-like query.
        """

        endpoint = (
            f"/v3/company/{self.realm_id}/query"
        )

        return self.get(
            endpoint,
            params={
                "query": query,
                "minorversion": "75",
            },
        )

    def post(
        self,
        endpoint: str,
        json: dict,
    ) -> dict:
        """
        Execute an authenticated POST request.
        """

        url = f"{self.base_url}{endpoint}"

        response = self.session.post(
            url,
            json=json,
            params={
                "minorversion": "75",
            },
            timeout=30,
        )

        if not response.ok:
            print(
                f"QuickBooks API request failed: "
                f"{response.status_code}"
            )
            print(response.text)

        response.raise_for_status()

        return response.json()