"""
Stripe Subscriptions API.

This module manages recurring SaaS subscriptions in Stripe.
"""

from integrations.stripe.clients import StripeClient


class StripeSubscriptions:
    """
    Service responsible for Stripe Subscription operations.
    """

    def __init__(self, client: StripeClient) -> None:
        self.client = client

    def find_by_hubspot_deal_id(
        self,
        hubspot_deal_id: str,
    ):
        """
        Find an existing subscription associated with a HubSpot Deal.
        """

        subscriptions = self.client.stripe.Subscription.list(
            status="all",
            limit=100,
        )

        for subscription in subscriptions.auto_paging_iter():

            metadata = subscription.metadata.to_dict()

            if (
                metadata.get("hubspot_deal_id")
                == hubspot_deal_id
            ):
                return subscription

        return None

    def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        hubspot_deal_id: str,
    ):
        """
        Create a recurring subscription for a Stripe customer.
        """

        return self.client.stripe.Subscription.create(
            customer=customer_id,
            items=[
                {
                    "price": price_id,
                }
            ],
            metadata={
                "hubspot_deal_id": hubspot_deal_id,
            },
        )

    def get_or_create_subscription(
        self,
        customer_id: str,
        price_id: str,
        hubspot_deal_id: str,
    ):
        """
        Return an existing subscription or create one when necessary.
        """

        subscription = self.find_by_hubspot_deal_id(
            hubspot_deal_id
        )

        if subscription:
            print(
                f"Subscription already exists: "
                f"{subscription.id}"
            )
            return subscription

        subscription = self.create_subscription(
            customer_id=customer_id,
            price_id=price_id,
            hubspot_deal_id=hubspot_deal_id,
        )

        print(
            f"Subscription created: "
            f"{subscription.id}"
        )

        return subscription