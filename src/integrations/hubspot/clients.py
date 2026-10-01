"""
HubSpot API Client.

This module provides a simple HTTP client for interacting with the
HubSpot CRM REST API.

At this stage of the project, the client is responsible for:

- Loading the HubSpot Service Key from environment variables.
- Creating an authenticated HTTP session.
- Sending GET requests to the HubSpot API.
- Raising exceptions when the API returns an unsuccessful response.

Later, this client will be extended with:
- POST, PATCH, and DELETE methods.
- Pagination handling.
- Retry strategies.
- Rate-limit handling.
- Structured logging.
- Custom exceptions.

The goal is to keep HubSpot authentication and HTTP communication
centralized instead of duplicating this logic across different
resources such as Companies, Contacts, and Deals.
"""


import os

import requests
from dotenv import load_dotenv


load_dotenv()


class HubSpotClient:
    BASE_URL = "https://api.hubapi.com"

    def __init__(self):
        self.access_token = os.getenv("HUBSPOT_ACCESS_TOKEN")

        if not self.access_token:
            raise ValueError("HUBSPOT_ACCESS_TOKEN is not set in the environment variables.")

        self.session = requests.Session()

        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",


            }
        )

    def get(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{self.BASE_URL}{endpoint}"

        response = self.session.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()
        
        return response.json()
    

    def post(self, endpoint: str, payload: dict) -> dict:
        
        url = f"{self.BASE_URL}{endpoint}"

        response = self.session.post(
            url,
            json=payload,
            timeout = 30,
        )

        if not response.ok:
            print(f"Request failed with status: {response.status_code}")
            print(f"URL: {response.url}")
            print(f"Response body: {response.text}")

        response.raise_for_status()

        return response.json()

    def put(self, endpoint: str, payload: dict | None = None) -> dict:
        """
        Send an authenticated PUT request to the HubSpot API.

        PUT requests can be used by HubSpot to create associations
        between CRM objects.

        Args:
            endpoint:
                HubSpot API endpoint.

            payload:
                Optional JSON payload.

        Returns:
            dict:
                JSON response returned by HubSpot.
                Some successful requests may return an empty response.
        """

        url = f"{self.BASE_URL}{endpoint}"

        response = self.session.put(
            url,
            json=payload,
            timeout=30,
        )

        # Print diagnostic information during development.
        if not response.ok:
            print(f"Request failed with status: {response.status_code}")
            print(f"URL: {response.url}")
            print(f"Response body: {response.text}")

        response.raise_for_status()

        # Some HubSpot endpoints return no JSON body after
        # completing an operation successfully.
        if not response.content:
            return {}

        return response.json()

    def patch(self, endpoint: str, payload: dict,) -> dict:
        """
        Send an authenticated PATCH request to the HubSpot API.

        PATCH requests are used to partially update an existing
        CRM resource without replacing the entire object.

        Args:
            endpoint:
                HubSpot API endpoint.

            payload:
                JSON payload containing the properties that should
                be updated.

        Returns:
            dict:
                Updated resource returned by HubSpot.

        Raises:
            requests.HTTPError:
                If HubSpot returns an unsuccessful HTTP status code.
        """

        url = f"{self.BASE_URL}{endpoint}"

        response = self.session.patch(
            url,
            json=payload,
            timeout=30,
        )

        if not response.ok:
            print(f"Request failed with status: {response.status_code}")
            print(f"URL: {response.url}")
            print(f"Response body: {response.text}")

        response.raise_for_status()

        return response.json()


if __name__ == "__main__":

    client = HubSpotClient()

    response = client.get(
        "/crm/v3/objects/companies"
        , params={"limit": 10}
    )

    print(response)




    