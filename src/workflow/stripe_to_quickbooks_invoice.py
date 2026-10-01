"""
Synchronize the latest Stripe invoice to QuickBooks Online.

Stripe is the billing source for the invoice amount.
QuickBooks is the accounting destination.
"""

from datetime import datetime, timezone

from integrations.stripe.clients import StripeClient
from integrations.stripe.customers import StripeCustomers
from integrations.stripe.invoices import StripeInvoices

from integrations.quickbooks.clients import QuickBooksClient
from integrations.quickbooks.customers import QuickBooksCustomers
from integrations.quickbooks.items import QuickBooksItems
from integrations.quickbooks.invoices import QuickBooksInvoices


def unix_to_date(timestamp: int) -> str:
    """
    Convert a Unix timestamp to YYYY-MM-DD.
    """

    return datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    ).date().isoformat()


def sync_invoice(
    hubspot_company_id: str,
    customer_name: str,
    customer_email: str,
) -> dict:
    """
    Synchronize the latest Stripe invoice to QuickBooks.
    """

    print("")
    print("Stripe -> QuickBooks Invoice Sync")
    print("---------------------------------")

    # ---------------------------------------------------------
    # Stripe
    # ---------------------------------------------------------

    stripe_client = StripeClient()

    stripe_customers = StripeCustomers(
        stripe_client
    )

    stripe_invoices = StripeInvoices(
        stripe_client
    )

    stripe_customer = (
        stripe_customers.find_by_hubspot_company_id(
            hubspot_company_id
        )
    )

    if not stripe_customer:
        raise ValueError(
            "Stripe customer could not be found."
        )

    stripe_invoice = (
        stripe_invoices.get_latest_customer_invoice(
            stripe_customer.id
        )
    )

    if not stripe_invoice:
        raise ValueError(
            "No Stripe invoice was found."
        )

    if stripe_invoice.currency.lower() != "usd":
        raise ValueError(
            "Only USD invoices are supported "
            "by this workflow."
        )

    amount = stripe_invoice.total / 100

    transaction_date = unix_to_date(
        stripe_invoice.created
    )

    print("")
    print("Stripe billing source")
    print(f"Invoice: {stripe_invoice.id}")
    print(f"Status: {stripe_invoice.status}")
    print(f"Amount: ${amount:,.2f}")
    print(f"Date: {transaction_date}")

    # ---------------------------------------------------------
    # QuickBooks
    # ---------------------------------------------------------

    quickbooks_client = QuickBooksClient()

    quickbooks_customers = QuickBooksCustomers(
        quickbooks_client
    )

    quickbooks_items = QuickBooksItems(
        quickbooks_client
    )

    quickbooks_invoices = QuickBooksInvoices(
        quickbooks_client
    )

    customer = (
        quickbooks_customers.get_or_create_customer(
            display_name=customer_name,
            email=customer_email,
        )
    )

    item = (
        quickbooks_items.get_or_create_service_item(
            name="NovaTech Enterprise Subscription",
            income_account_name="Subscription Revenue",
        )
    )

    invoice = quickbooks_invoices.get_or_create_invoice(
        customer_id=customer["Id"],
        item_id=item["Id"],
        amount=amount,
        description=(
            "NovaTech Enterprise monthly subscription"
        ),
        stripe_invoice_id=stripe_invoice.id,
        transaction_date=transaction_date,
    )

    print("")
    print("Invoice synchronization completed.")
    print(f"Stripe Invoice: {stripe_invoice.id}")
    print(f"QuickBooks Invoice: {invoice['Id']}")
    print(
        f"QuickBooks DocNumber: "
        f"{invoice.get('DocNumber')}"
    )
    print(
        f"QuickBooks Total: "
        f"${invoice.get('TotalAmt', 0):,.2f}"
    )
    print(
        f"QuickBooks Balance: "
        f"${invoice.get('Balance', 0):,.2f}"
    )

    return invoice


if __name__ == "__main__":
    sync_invoice(
        hubspot_company_id="58819345672",
        customer_name="Acme Corporation",
        customer_email="sarah.johnson@acme.example",
    )