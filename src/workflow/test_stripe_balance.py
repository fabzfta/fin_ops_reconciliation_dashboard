"""
Inspect the current Stripe account balance.

This workflow is read-only.
"""

from integrations.stripe.clients import StripeClient
from integrations.stripe.balances import StripeBalances


def format_money(
    amount: int,
    currency: str,
) -> str:
    """
    Format a Stripe monetary amount.
    """

    return (
        f"{currency.upper()} "
        f"{amount / 100:,.2f}"
    )


def print_balance_group(
    title: str,
    balances,
) -> None:
    """
    Print a Stripe balance group.
    """

    print("")
    print(title)
    print("-" * len(title))

    if not balances:
        print("No balance.")
        return

    for balance in balances:
        print(
            format_money(
                balance.amount,
                balance.currency,
            )
        )


def main() -> None:
    client = StripeClient()

    balances_service = StripeBalances(
        client
    )

    balance = balances_service.retrieve()

    print("")
    print("Stripe Account Balance")
    print("======================")

    print_balance_group(
        "Available",
        balance.available,
    )

    print_balance_group(
        "Pending",
        balance.pending,
    )


if __name__ == "__main__":
    main()