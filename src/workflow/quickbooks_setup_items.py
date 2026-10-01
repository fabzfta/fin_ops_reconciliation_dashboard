"""
Configure NovaTech products and services in QuickBooks.
"""

from integrations.quickbooks.clients import QuickBooksClient
from integrations.quickbooks.items import QuickBooksItems


def main() -> None:
    client = QuickBooksClient()
    items = QuickBooksItems(client)

    print("")
    print("Configuring NovaTech QuickBooks Items")
    print("-------------------------------------")

    item = items.get_or_create_service_item(
        name="NovaTech Enterprise Subscription",
        income_account_name="Subscription Revenue",
    )

    print("")
    print("QuickBooks Item configuration completed.")
    print(f"Item ID: {item['Id']}")
    print(f"Item Name: {item['Name']}")


if __name__ == "__main__":
    main()