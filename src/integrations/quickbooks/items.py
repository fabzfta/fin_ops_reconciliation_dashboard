"""
QuickBooks Item integration.

Items represent products and services sold to customers.
"""

from integrations.quickbooks.clients import QuickBooksClient
from integrations.quickbooks.accounts import QuickBooksAccounts


class QuickBooksItems:
    """
    Manage QuickBooks products and services.
    """

    def __init__(
        self,
        client: QuickBooksClient,
    ) -> None:
        self.client = client

    def find_by_name(
        self,
        name: str,
    ) -> dict | None:
        """
        Find an item by its exact name.
        """

        safe_name = name.replace("'", "\\'")

        response = self.client.query(
            "SELECT * FROM Item "
            f"WHERE Name = '{safe_name}' "
            "MAXRESULTS 1"
        )

        items = (
            response
            .get("QueryResponse", {})
            .get("Item", [])
        )

        if not items:
            return None

        return items[0]

    def create_service_item(
        self,
        name: str,
        income_account_name: str,
    ) -> dict:
        """
        Create a service item associated with an income account.
        """

        accounts = QuickBooksAccounts(self.client)

        income_account = accounts.find_by_name(
            income_account_name
        )

        if not income_account:
            raise ValueError(
                f"Income account not found: "
                f"{income_account_name}"
            )

        endpoint = (
            f"/v3/company/"
            f"{self.client.realm_id}/item"
        )

        payload = {
            "Name": name,
            "Type": "Service",
            "IncomeAccountRef": {
                "value": income_account["Id"],
                "name": income_account["Name"],
            },
        }

        response = self.client.post(
            endpoint,
            json=payload,
        )

        return response["Item"]

    def get_or_create_service_item(
        self,
        name: str,
        income_account_name: str,
    ) -> dict:
        """
        Return an existing item or create it when missing.
        """

        item = self.find_by_name(name)

        if item:
            print(
                f"Item already exists: "
                f"{item['Name']} ({item['Id']})"
            )
            return item

        item = self.create_service_item(
            name=name,
            income_account_name=income_account_name,
        )

        print(
            f"Item created: "
            f"{item['Name']} ({item['Id']})"
        )

        return item