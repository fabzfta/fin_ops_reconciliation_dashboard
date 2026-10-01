"""
QuickBooks Customer integration.

Provides operations for finding, creating, and reusing
customers in QuickBooks Online.

For the current sandbox implementation, DisplayName is used
as the customer identifier. A persistent cross-system identity
mapping will be introduced later in the data platform.
"""

from integrations.quickbooks.clients import QuickBooksClient


class QuickBooksCustomers:
    """
    Manage QuickBooks Online customers.
    """

    def __init__(
        self,
        client: QuickBooksClient,
    ) -> None:
        self.client = client

    def find_by_display_name(
        self,
        display_name: str,
    ) -> dict | None:
        """
        Find a QuickBooks customer by its exact DisplayName.

        Args:
            display_name:
                Customer name stored in QuickBooks.

        Returns:
            QuickBooks Customer object when found.
            Otherwise, None.
        """

        # Escape single quotes before using the value
        # inside the QuickBooks query.
        safe_name = display_name.replace("'", "\\'")

        query = (
            "SELECT * FROM Customer "
            f"WHERE DisplayName = '{safe_name}' "
            "MAXRESULTS 1"
        )

        response = self.client.query(query)

        customers = (
            response
            .get("QueryResponse", {})
            .get("Customer", [])
        )

        if not customers:
            return None

        return customers[0]

    def create_customer(
        self,
        display_name: str,
        email: str,
    ) -> dict:
        """
        Create a customer in QuickBooks Online.

        Args:
            display_name:
                Customer company name.

            email:
                Customer primary email address.

        Returns:
            Newly created QuickBooks Customer object.
        """

        endpoint = (
            f"/v3/company/"
            f"{self.client.realm_id}/customer"
        )

        payload = {
            "DisplayName": display_name,
            "CompanyName": display_name,
            "PrimaryEmailAddr": {
                "Address": email,
            },
        }

        response = self.client.post(
            endpoint,
            json=payload,
        )

        return response["Customer"]

    def get_or_create_customer(
        self,
        display_name: str,
        email: str,
    ) -> dict:
        """
        Return an existing customer or create it when missing.

        This makes the customer provisioning workflow idempotent.
        """

        customer = self.find_by_display_name(
            display_name
        )

        if customer:
            print(
                f"Customer already exists: "
                f"{customer['DisplayName']} "
                f"({customer['Id']})"
            )

            return customer

        customer = self.create_customer(
            display_name=display_name,
            email=email,
        )

        print(
            f"Customer created: "
            f"{customer['DisplayName']} "
            f"({customer['Id']})"
        )

        return customer