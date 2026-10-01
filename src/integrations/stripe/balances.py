"""
Stripe Balance integration.

Provides access to available and pending balances held
by Stripe for the connected account.
"""

from integrations.stripe.clients import StripeClient


class StripeBalances:
    """
    Access Stripe account balances.
    """

    def __init__(
        self,
        client: StripeClient,
    ) -> None:
        self.client = client

    def retrieve(self):
        """
        Retrieve the current Stripe balance.
        """

        return self.client.stripe.Balance.retrieve()