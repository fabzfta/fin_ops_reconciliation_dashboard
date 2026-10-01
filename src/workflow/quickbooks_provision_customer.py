"""
Provision a customer in QuickBooks Online.

This workflow creates the QuickBooks accounting customer
corresponding to an existing CRM and billing customer.

For now, DisplayName is used to identify an existing customer.
A persistent cross-system identity mapping will be introduced
later in the data platform.
"""

from integrations.quickbooks.clients import QuickBooksClient
from integrations.quickbooks.customers import QuickBooksCustomers


def provision_customer(
    customer_name: str,
    customer_email: str,
) -> dict:
    """
    Create or retrieve a customer in QuickBooks Online.

    Args:
        customer_name:
            Customer company name.

        customer_email:
            Customer primary email address.

    Returns:
        QuickBooks Customer object.
    """

    print("")
    print("Provisioning QuickBooks customer")
    print("-------------------------------")

    client = QuickBooksClient()
    customers = QuickBooksCustomers(client)

    customer = customers.get_or_create_customer(
        display_name=customer_name,
        email=customer_email,
    )

    print("")
    print("QuickBooks customer provisioning completed.")
    print(f"Customer ID: {customer['Id']}")
    print(f"Customer Name: {customer['DisplayName']}")

    return customer


if __name__ == "__main__":
    provision_customer(
        customer_name="Acme Corporation",
        customer_email="sarah.johnson@acme.example",
    )