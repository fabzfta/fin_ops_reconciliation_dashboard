"""
Test the QuickBooks Online Accounting API connection.

This script retrieves the Chart of Accounts from the
configured QuickBooks Sandbox company.
"""

from integrations.quickbooks.accounts import QuickBooksAccounts
from integrations.quickbooks.clients import QuickBooksClient


def main() -> None:
    client = QuickBooksClient()
    accounts_service = QuickBooksAccounts(client)

    accounts = accounts_service.list_accounts()

    print("")
    print("QuickBooks connection successful.")
    print(f"Accounts returned: {len(accounts)}")
    print("")
    print("Chart of Accounts")
    print("-----------------")

    for account in accounts:
        account_id = account.get("Id")
        name = account.get("Name")
        account_type = account.get("AccountType")
        account_subtype = account.get(
            "AccountSubType",
            "",
        )

        print(
            f"{account_id:>4} | "
            f"{account_type:<25} | "
            f"{account_subtype:<30} | "
            f"{name}"
        )


if __name__ == "__main__":
    main()