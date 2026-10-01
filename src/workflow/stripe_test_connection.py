"""
Test Stripe API connectivity.

This script performs a read-only request to verify that the
application can authenticate successfully with Stripe.
"""

from integrations.stripe.clients import StripeClient


def main() -> None:
    client = StripeClient()

    # Retrieve a small customer list.
    # This is intentionally read-only: the purpose of this script
    # is only to validate authentication and connectivity.
    customers = client.stripe.Customer.list(limit=3)

    print("Stripe connection successful.")
    print(f"Customers returned: {len(customers.data)}")

    for customer in customers.data:
        print(
            f"- {customer.id}: "
            f"{customer.get('name', 'Unnamed customer')}"
        )


if __name__ == "__main__":
    main()