"""
Inspect the latest Stripe invoice generated for Acme Corporation.

No accounting records are created by this workflow.
"""

from datetime import datetime, timezone

from integrations.stripe.clients import StripeClient
from integrations.stripe.customers import StripeCustomers
from integrations.stripe.invoices import StripeInvoices


def format_timestamp(timestamp: int | None) -> str | None:
    """
    Convert a Unix timestamp to an ISO UTC datetime.
    """

    if timestamp is None:
        return None

    return datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    ).isoformat()


def main() -> None:
    client = StripeClient()

    customers = StripeCustomers(client)
    invoices = StripeInvoices(client)

    # Use the real HubSpot Company ID used when the
    # Stripe customer was originally provisioned.
    hubspot_company_id = "58819345672"

    customer = customers.find_by_hubspot_company_id(
        hubspot_company_id
    )

    if not customer:
        raise ValueError(
            "Stripe customer could not be found."
        )

    invoice = invoices.get_latest_customer_invoice(
        customer_id=customer.id,
    )

    if not invoice:
        raise ValueError(
            "No Stripe invoice was found for this customer."
        )

    print("")
    print("Stripe Invoice")
    print("--------------")
    print(f"Invoice ID: {invoice.id}")
    print(f"Customer ID: {invoice.customer}")
    print(f"Status: {invoice.status}")
    print(f"Currency: {invoice.currency.upper()}")
    print(
        f"Total: "
        f"${invoice.total / 100:,.2f}"
    )
    print(
        f"Amount paid: "
        f"${invoice.amount_paid / 100:,.2f}"
    )
    print(
        f"Amount due: "
        f"${invoice.amount_due / 100:,.2f}"
    )
    print(
        f"Created at: "
        f"{format_timestamp(invoice.created)}"
    )

   
    print(
        f"Amount remaining: "
        f"${invoice.amount_remaining / 100:,.2f}"
)

    print("")
    print("Invoice Lines")
    print("-------------")

    for line in invoice.lines.data:
        print(
            f"${line.amount / 100:,.2f} | "
            f"{line.description}"
        )


if __name__ == "__main__":
    main()