"""
Stripe Invoice integration.

Provides operations for retrieving billing invoices generated
by Stripe subscriptions.
"""

from integrations.stripe.clients import StripeClient


class StripeInvoices:
    """
    Access Stripe billing invoices.
    """

    def __init__(
        self,
        client: StripeClient,
    ) -> None:
        self.client = client

    def list_customer_invoices(
        self,
        customer_id: str,
    ) -> list:
        """
        Return invoices belonging to a Stripe customer.
        """

        invoices = self.client.stripe.Invoice.list(
            customer=customer_id,
            limit=100,
        )

        return list(invoices.auto_paging_iter())

    def get_latest_customer_invoice(
        self,
        customer_id: str,
    ):
        """
        Return the most recent invoice for a customer.
        """

        invoices = self.client.stripe.Invoice.list(
            customer=customer_id,
            limit=1,
        )

        if not invoices.data:
            return None

        return invoices.data[0]