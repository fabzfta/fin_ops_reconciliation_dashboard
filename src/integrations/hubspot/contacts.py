"""
HubSpot Contacts API.

This module contains operations related to HubSpot Contact objects.

Contacts represent people associated with companies in the CRM.
For the NovaTech project, contacts will typically represent business
stakeholders such as CFOs, finance managers, and decision makers.
"""

from .clients import HubSpotClient


class HubSpotContacts:
    """
    Service responsible for HubSpot Contact operations.
    """

    ENDPOINT = "/crm/v3/objects/contacts"

    def __init__(self, client: HubSpotClient):
        """
        Initialize the Contacts service.

        Args:
            client:
                An authenticated HubSpotClient instance.
        """
        self.client = client

    def create_contact(
        self,
        first_name: str,
        last_name: str,
        email: str,
        job_title: str,
    ) -> dict:
        """
        Create a new contact in HubSpot.

        Args:
            first_name:
                Contact's first name.

            last_name:
                Contact's last name.

            email:
                Contact's business email address.

            job_title:
                Contact's role inside the company.

        Returns:
            dict:
                The newly created HubSpot Contact.
        """

        payload = {
            "properties": {
                "firstname": first_name,
                "lastname": last_name,
                "email": email,
                "jobtitle": job_title,
            }
        }

        return self.client.post(
            self.ENDPOINT,
            payload,
        )

    def get_by_email(
        self,
        email: str,
    ) -> dict | None:
        """
        Retrieve a HubSpot Contact by email address.

        Args:
            email:
                Contact email address.

        Returns:
            dict | None:
                HubSpot Contact when found, otherwise None.
        """

        endpoint = f"{self.ENDPOINT}/search"

        payload = {
            "filterGroups": [
                {
                    "filters": [
                        {
                            "propertyName": "email",
                            "operator": "EQ",
                            "value": email,
                        }
                    ]
                }
            ],
            "properties": [
                "firstname",
                "lastname",
                "email",
                "jobtitle",
                "phone",
            ],
            "limit": 1,
        }

        response = self.client.post(
            endpoint,
            payload,
        )

        results = response.get(
            "results",
            []
        )

        if not results:
            return None

        return results[0]

    def get_by_id(
        self,
        contact_id: str,
    ) -> dict:
        """
        Retrieve a HubSpot Contact by ID.
        """

        endpoint = f"{self.ENDPOINT}/{contact_id}"

        params = {
            "properties": ",".join(
                [
                    "firstname",
                    "lastname",
                    "email",
                    "jobtitle",
                    "phone",
                ]
            )
        }

        return self.client.get(
            endpoint,
            params=params,
        )


if __name__ == "__main__":
    client = HubSpotClient()

    contacts = HubSpotContacts(client)

    contact = contacts.create_contact(
        first_name="Sarah",
        last_name="Johnson",
        email="seuemail+sarah.acme@gmail.com",
        job_title="Chief Financial Officer",
    )

    print(contact)