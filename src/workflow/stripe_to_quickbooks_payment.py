"""
Synchronize a Stripe payment to QuickBooks Online.

The workflow retrieves the real Stripe payment associated with
an invoice and applies it to the corresponding QuickBooks invoice.
"""

from datetime import datetime, timezone

from integrations.stripe.clients import StripeClient
from integrations.stripe.customers import StripeCustomers
from integrations.stripe.invoices import StripeInvoices

from integrations.quickbooks.clients import QuickBooksClient
from integrations.quickbooks.customers import QuickBooksCustomers
from integrations.quickbooks.invoices import QuickBooksInvoices
from integrations.quickbooks.payments import QuickBooksPayments


def unix_to_date(timestamp: int) -> str:
    """
    Convert a Unix timestamp to YYYY-MM-DD.
    """

    return datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    ).date().isoformat()


def sync_payment(
    hubspot_company_id: str,
    customer_name: str,
) -> dict:
    """
    Synchronize the latest Stripe payment to QuickBooks.
    """

    print("")
    print("Stripe -> QuickBooks Payment Sync")
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
            "Stripe invoice could not be found."
        )

    if stripe_invoice.status != "paid":
        raise ValueError(
            f"Stripe invoice is not paid: "
            f"{stripe_invoice.status}"
        )

    expanded_invoice = stripe_client.stripe.Invoice.retrieve(
        stripe_invoice.id,
        expand=["payments"],
    )

    if (
        not expanded_invoice.payments
        or not expanded_invoice.payments.data
    ):
        raise ValueError(
            "No Stripe payment was found for the invoice."
        )

    invoice_payment = expanded_invoice.payments.data[0]

    if invoice_payment.status != "paid":
        raise ValueError(
            f"Stripe payment is not paid: "
            f"{invoice_payment.status}"
        )

    payment_reference = invoice_payment.payment

    if (
        not payment_reference
        or not payment_reference.payment_intent
    ):
        raise ValueError(
            "Stripe PaymentIntent could not be found."
        )

    payment_intent_id = (
        payment_reference.payment_intent
    )

    amount = invoice_payment.amount_paid / 100

    transaction_date = unix_to_date(
        stripe_invoice.created
    )

    print("")
    print("Stripe payment source")
    print(f"Invoice: {stripe_invoice.id}")
    print(f"Payment Intent: {payment_intent_id}")
    print(f"Amount: ${amount:,.2f}")
    print(f"Date: {transaction_date}")

    # ---------------------------------------------------------
    # QuickBooks
    # ---------------------------------------------------------

    quickbooks_client = QuickBooksClient()

    quickbooks_customers = QuickBooksCustomers(
        quickbooks_client
    )

    quickbooks_invoices = QuickBooksInvoices(
        quickbooks_client
    )

    quickbooks_payments = QuickBooksPayments(
        quickbooks_client
    )

    customer = (
        quickbooks_customers.find_by_display_name(
            customer_name
        )
    )

    if not customer:
        raise ValueError(
            "QuickBooks customer could not be found."
        )

    invoice = (
        quickbooks_invoices.find_by_stripe_invoice_id(
            stripe_invoice.id
        )
    )

    if not invoice:
        raise ValueError(
            "QuickBooks invoice could not be found."
        )

    payment = (
        quickbooks_payments.get_or_create_payment(
            customer_id=customer["Id"],
            invoice_id=invoice["Id"],
            amount=amount,
            stripe_payment_intent_id=payment_intent_id,
            transaction_date=transaction_date,
        )
    )

    # Reload the invoice after the payment so we can inspect
    # the updated balance.
    refreshed_invoice = (
        quickbooks_invoices.find_by_stripe_invoice_id(
            stripe_invoice.id
        )
    )

    print("")
    print("Payment synchronization completed.")
    print(f"Stripe Payment Intent: {payment_intent_id}")
    print(f"QuickBooks Payment: {payment['Id']}")
    print(f"QuickBooks Invoice: {invoice['Id']}")
    print(
        f"Invoice Total: "
        f"${refreshed_invoice['TotalAmt']:,.2f}"
    )
    print(
        f"Invoice Balance: "
        f"${refreshed_invoice['Balance']:,.2f}"
    )

    return payment


if __name__ == "__main__":
    sync_payment(
        hubspot_company_id="58819345672",
        customer_name="Acme Corporation",
    )