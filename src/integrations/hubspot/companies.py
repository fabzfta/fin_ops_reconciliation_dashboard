"""
HubSpot Companies API.

This module contains operations related specifically to HubSpot
Company objects.

The HTTP communication itself is delegated to HubSpotClient.
This separation allows the generic API client to remain independent
from CRM-specific business objects.
"""
    
from .clients import HubSpotClient


class HubSpotCompanies:
    """
    Service responsible for HubSpot Company operations.
    """

    ENDPOINT = "/crm/v3/objects/companies"

    def __init__(self, client: HubSpotClient):
        """
        Initialize the Companies service.

        Args:
            client:
                An authenticated HubSpotClient instance.
        """
        self.client = client

    def create_company(
        self,
        name: str,
        domain: str,
        city: str,
        state: str,
        country: str,
    ) -> dict:
        """
        Create a new company in HubSpot.

        Args:
            name:
                Company name.

            domain:
                Company's website domain.

            city:
                Company headquarters city.

            state:
                Company headquarters state.

            country:
                Company headquarters country.

        Returns:
            dict:
                The newly created HubSpot Company.
        """

        payload = {
            "properties": {
                "name": name,
                "domain": domain,
                "city": city,
                "state": state,
                "country": country,
            }
        }

        return self.client.post(
            self.ENDPOINT,
            payload,
        )

    def get_by_id(
        self,
        company_id: str,
    ) -> dict:
        """
        Retrieve a HubSpot Company by ID.
        """

        endpoint = f"{self.ENDPOINT}/{company_id}"

        params = {
            "properties": ",".join(
                [
                    "name",
                    "domain",
                    "city",
                    "state",
                    "country",
                    "industry",
                ]
            )
        }

        return self.client.get(
            endpoint,
            params=params,
        )


if __name__ == "__main__":
    client = HubSpotClient()

    companies = HubSpotCompanies(client)

    company = companies.create_company(
        name="Acme Corporation",
        domain="acme.example",
        city="New York",
        state="NY",
        country="United States",
    )

    print(company)