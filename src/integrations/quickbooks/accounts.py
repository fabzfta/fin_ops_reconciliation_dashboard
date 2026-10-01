"""
QuickBooks Chart of Accounts integration.
"""

from integrations.quickbooks.clients import QuickBooksClient


class QuickBooksAccounts:
    """
    Manage QuickBooks Chart of Accounts.
    """

    def __init__(
        self,
        client: QuickBooksClient,
    ) -> None:
        self.client = client

    def list_accounts(self) -> list[dict]:
        """
        Return all accounts available in QuickBooks.
        """

        response = self.client.query(
            "SELECT * FROM Account MAXRESULTS 1000"
        )

        return (
            response
            .get("QueryResponse", {})
            .get("Account", [])
        )

    def find_by_name(
        self,
        name: str,
    ) -> dict | None:
        """
        Find an account by its exact name.
        """

        accounts = self.list_accounts()

        for account in accounts:
            if account.get("Name") == name:
                return account

        return None

    def create_account(
        self,
        name: str,
        account_type: str,
        account_subtype: str,
    ) -> dict:
        """
        Create a new QuickBooks account.
        """

        endpoint = (
            f"/v3/company/{self.client.realm_id}/account"
        )

        payload = {
            "Name": name,
            "AccountType": account_type,
            "AccountSubType": account_subtype,
        }

        response = self.client.post(
            endpoint,
            json=payload,
        )

        return response["Account"]

    def get_or_create_account(
        self,
        name: str,
        account_type: str,
        account_subtype: str,
    ) -> dict:
        """
        Return an existing account or create it when missing.
        """

        account = self.find_by_name(name)

        if account:
            print(
                f"Account already exists: "
                f"{name} ({account['Id']})"
            )
            return account

        account = self.create_account(
            name=name,
            account_type=account_type,
            account_subtype=account_subtype,
        )

        print(
            f"Account created: "
            f"{name} ({account['Id']})"
        )

        return account