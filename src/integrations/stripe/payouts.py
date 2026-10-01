"""
Stripe Payout integration.

Provides access to transfers from the Stripe balance
to the company's external bank account.
"""

from integrations.stripe.clients import StripeClient


class StripePayouts:
    """
    Access Stripe payouts.
    """

    def __init__(
        self,
        client: StripeClient,
    ) -> None:
        self.client = client

    def list_payouts(
        self,
        limit: int = 10,
    ) -> list:
        """
        Return recent Stripe payouts.
        """

        payouts = self.client.stripe.Payout.list(
            limit=limit,
        )

        return list(payouts.data)