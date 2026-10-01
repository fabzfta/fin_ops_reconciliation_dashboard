"""
Inspect the payment associated with the latest Stripe invoice.

This workflow is read-only. No accounting records are created.
"""

from integrations.stripe.clients import StripeClient
from integrations.stripe.customers import StripeCustomers
from integrations.stripe.invoices import StripeInvoices


def main() -> None:
    client = StripeClient()

    customers = StripeCustomers(client)
    invoices = StripeInvoices(client)

    hubspot_company_id = "58819345672"

    customer = customers.find_by_hubspot_company_id(
        hubspot_company_id
    )

    if not customer:
        raise ValueError(
            "Stripe customer could not be found."
        )

    invoice = invoices.get_latest_customer_invoice(
        customer.id
    )

    if not invoice:
        raise ValueError(
            "Stripe invoice could not be found."
        )

    print("")
    print("Stripe Invoice")
    print("--------------")
    print(f"Invoice ID: {invoice.id}")
    print(f"Status: {invoice.status}")
    print(f"Total: ${invoice.total / 100:,.2f}")
    print(
        f"Amount paid: "
        f"${invoice.amount_paid / 100:,.2f}"
    )
    print(
        f"Amount remaining: "
        f"${invoice.amount_remaining / 100:,.2f}"
    )

    # Retrieve the invoice again while expanding its payment
    # information so we can inspect the real Stripe payment.
    expanded_invoice = client.stripe.Invoice.retrieve(
        invoice.id,
        expand=["payments"],
    )

    payments = expanded_invoice.payments

    print("")
    print("Stripe Invoice Payments")
    print("-----------------------")

    if not payments or not payments.data:
        print("No payments found.")
        return

    for invoice_payment in payments.data:
        print(
            f"Invoice Payment ID: "
            f"{invoice_payment.id}"
        )
        print(
            f"Status: "
            f"{invoice_payment.status}"
        )
        print(
            f"Amount paid: "
            f"${invoice_payment.amount_paid / 100:,.2f}"
        )

        payment = invoice_payment.payment

        if payment:
            print(
                f"Payment type: "
                f"{payment.type}"
            )

            if payment.payment_intent:
                print(
                    f"Payment Intent ID: "
                    f"{payment.payment_intent}"
                )

        print("-----------------------")


if __name__ == "__main__":
    main()