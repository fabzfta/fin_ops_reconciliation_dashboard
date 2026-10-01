"""
HubSpot CRM Associations.

This module is responsible for creating relationships between
different HubSpot CRM objects.

Examples:

Contact -> Company
Deal    -> Company
Deal    -> Contact

Keeping association logic separate prevents relationship-specific
API calls from being duplicated across resource modules.
"""

from .clients import HubSpotClient


class HubSpotAssociations:
    """
    Service responsible for associations between HubSpot CRM objects.
    """

    def __init__(self, client: HubSpotClient):
        """
        Initialize the association service.

        Args:
            client:
                Authenticated HubSpotClient instance.
        """
        self.client = client

    def associate(self, from_object_type: str, from_object_id: str, to_object_type: str, to_object_id: str, association_type: str) -> dict:
        """
        Create an association between two HubSpot CRM objects.

        Args:
            from_object_type:
                Type of the source CRM object.
                Example: "contact"

            from_object_id:
                HubSpot ID of the source object.

            to_object_type:
                Type of the target CRM object.
                Example: "company"

            to_object_id:
                HubSpot ID of the target object.

            association_type:
                HubSpot association type.

                Example:
                "contact_to_company"

        Returns:
            dict:
                HubSpot API response.
        """

        endpoint = (
            f"/crm/v3/objects/{from_object_type}/"
            f"{from_object_id}/associations/"
            f"{to_object_type}/{to_object_id}/"
            f"{association_type}"
        )

        return self.client.put(endpoint)


if __name__ == "__main__":
    client = HubSpotClient()

    associations = HubSpotAssociations(client)

    deal_id = "65516507983"

    company_id = "58819345672"
    contact_id = "252076728918"

    # Associate the Deal with Acme Corporation.
    deal_company = associations.associate(
        from_object_type="deal",
        from_object_id=deal_id,
        to_object_type="company",
        to_object_id=company_id,
        association_type="deal_to_company",
    )

    print("Deal -> Company association created:")
    print(deal_company)

    # Associate the Deal with Sarah Johnson.
    deal_contact = associations.associate(
        from_object_type="deal",
        from_object_id=deal_id,
        to_object_type="contact",
        to_object_id=contact_id,
        association_type="deal_to_contact",
    )

    print("Deal -> Contact association created:")
    print(deal_contact)