"""
Inspect the Stripe financial transaction associated with a payment.

This workflow is read-only. No accounting records are created.
"""

from datetime import datetime, timezone

from integrations.stripe.clients import StripeClient
from integrations.stripe.balance_transaction import (
    StripeBalanceTransactions,
)


PAYMENT_INTENT_ID = "pi_3ULSBgCvIOVmaa3U0Jlu2dU1"


def format_timestamp(timestamp: int | None) -> str | None:
    """
    Convert a Unix timestamp to ISO UTC.
    """

    if timestamp is None:
        return None

    return datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    ).isoformat()


def main() -> None:
    client = StripeClient()

    balance_transactions = StripeBalanceTransactions(
        client
    )

    payment_intent = client.stripe.PaymentIntent.retrieve(
        PAYMENT_INTENT_ID,
        expand=["latest_charge"],
    )

    print("")
    print("Stripe PaymentIntent")
    print("--------------------")
    print(f"Payment Intent ID: {payment_intent.id}")
    print(f"Status: {payment_intent.status}")
    print(
        f"Amount: "
        f"${payment_intent.amount / 100:,.2f}"
    )
    print(
        f"Amount received: "
        f"${payment_intent.amount_received / 100:,.2f}"
    )

    charge = payment_intent.latest_charge

    if not charge:
        raise ValueError(
            "No Stripe charge was found."
        )

    print("")
    print("Stripe Charge")
    print("-------------")
    print(f"Charge ID: {charge.id}")
    print(f"Status: {charge.status}")
    print(
        f"Amount: "
        f"${charge.amount / 100:,.2f}"
    )
    print(
        f"Paid: {charge.paid}"
    )

    balance_transaction_id = charge.balance_transaction

    if not balance_transaction_id:
        raise ValueError(
            "No balance transaction was found "
            "for the Stripe charge."
        )

    balance_transaction = (
        balance_transactions.retrieve(
            balance_transaction_id
        )
    )

    print("")
    print("Stripe Balance Transaction")
    print("--------------------------")
    print(
        f"Balance Transaction ID: "
        f"{balance_transaction.id}"
    )
    print(
        f"Type: "
        f"{balance_transaction.type}"
    )
    print(
        f"Currency: "
        f"{balance_transaction.currency.upper()}"
    )
    print(
        f"Gross: "
        f"${balance_transaction.amount / 100:,.2f}"
    )
    print(
        f"Fee: "
        f"${balance_transaction.fee / 100:,.2f}"
    )
    print(
        f"Net: "
        f"${balance_transaction.net / 100:,.2f}"
    )
    print(
        f"Available on: "
        f"{format_timestamp(balance_transaction.available_on)}"
    )

    print("")
    print("Fee Details")
    print("-----------")

    for fee_detail in balance_transaction.fee_details:
        print(
            f"{fee_detail.type}: "
            f"${fee_detail.amount / 100:,.2f}"
        )


if __name__ == "__main__":
    main()