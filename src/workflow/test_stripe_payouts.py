"""
Inspect recent Stripe payouts.

This workflow is read-only and does not create or modify
any Stripe or QuickBooks records.
"""

from datetime import datetime, timezone

from integrations.stripe.clients import StripeClient
from integrations.stripe.payouts import StripePayouts


def format_timestamp(timestamp: int | None) -> str | None:
    """
    Convert a Unix timestamp to an ISO 8601 UTC datetime.
    """

    if timestamp is None:
        return None

    return datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    ).isoformat()


def format_money(
    amount: int,
    currency: str,
) -> str:
    """
    Format a Stripe monetary amount using its currency code.

    Stripe monetary values are represented in the smallest
    currency unit, such as cents.
    """

    value = amount / 100

    return f"{currency.upper()} {value:,.2f}"


def main() -> None:
    """
    Retrieve and display recent Stripe payouts.
    """

    client = StripeClient()

    payouts_service = StripePayouts(
        client
    )

    payouts = payouts_service.list_payouts(
        limit=10
    )

    print("")
    print("Stripe Payouts")
    print("--------------")

    if not payouts:
        print("No payouts found.")
        return

    for payout in payouts:
        formatted_amount = format_money(
            payout.amount,
            payout.currency,
        )

        created_at = format_timestamp(
            payout.created
        )

        arrival_date = format_timestamp(
            payout.arrival_date
        )

        print("")
        print(f"Payout ID: {payout.id}")
        print(f"Status: {payout.status}")
        print(f"Amount: {formatted_amount}")
        print(f"Created: {created_at}")
        print(f"Arrival date: {arrival_date}")
        print("----------------")


if __name__ == "__main__":
    main()