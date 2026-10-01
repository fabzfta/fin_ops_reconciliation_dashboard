"""
HubSpot Deals API.

This module contains operations related to HubSpot Deal objects.

Deals represent commercial opportunities in the CRM. In the NovaTech
project, a Deal represents a potential SaaS subscription.

A successful Deal will eventually trigger the customer provisioning
flow in Stripe.
"""

from .clients import HubSpotClient


class HubSpotDeals:
    """
    Service responsible for HubSpot Deal operations.
    """

    ENDPOINT = "/crm/v3/objects/deals"

    def __init__(self, client: HubSpotClient):
        """
        Initialize the Deals service.

        Args:
            client:
                Authenticated HubSpotClient instance.
        """

        self.client = client

    def create_deal(
        self,
        name: str,
        amount: float,
        pipeline_id: str,
        stage_id: str,
    ) -> dict:
        """
        Create a new Deal in HubSpot.

        Args:
            name:
                Human-readable Deal name.

            amount:
                Total contract value.

            pipeline_id:
                HubSpot pipeline identifier.

            stage_id:
                Initial Deal stage identifier.

        Returns:
            dict:
                Newly created HubSpot Deal.
        """

        payload = {
            "properties": {
                "dealname": name,
                "amount": str(amount),
                "pipeline": pipeline_id,
                "dealstage": stage_id,
            }
        }

        return self.client.post(
            self.ENDPOINT,
            payload,
        )

    def update_stage(
        self,
        deal_id: str,
        stage_id: str,
    ) -> dict:
        """
        Move an existing Deal to another pipeline stage.

        Args:
            deal_id:
                HubSpot Deal ID.

            stage_id:
                Target stage ID.

        Returns:
            dict:
                Updated Deal returned by HubSpot.
        """

        endpoint = f"{self.ENDPOINT}/{deal_id}"

        payload = {
            "properties": {
                "dealstage": stage_id,
            }
        }

        return self.client.patch(
            endpoint,
            payload,
        )

    def get_by_id(
        self,
        deal_id: str,
    ) -> dict:
        """
        Retrieve a HubSpot Deal by ID.
        """

        endpoint = f"{self.ENDPOINT}/{deal_id}"

        params = {
            "properties": ",".join(
                [
                    "dealname",
                    "amount",
                    "pipeline",
                    "dealstage",
                    "closedate",
                ]
            )
        }

        return self.client.get(
            endpoint,
            params=params,
        )


if __name__ == "__main__":
    from pipeline import HubSpotPipelines

    client = HubSpotClient()

    # Retrieve pipeline metadata dynamically.
    pipelines = HubSpotPipelines(client)

    sales_pipeline = pipelines.find_pipeline_by_label(
        "Sales Pipeline"
    )

    qualified_stage = pipelines.find_stage_by_label(
        sales_pipeline,
        "Qualified To Buy",
    )

    # Create the Deals service.
    deals = HubSpotDeals(client)

    # Create NovaTech's first commercial opportunity.
    deal = deals.create_deal(
        name="Acme Corporation - Enterprise Plan",
        amount=60000,
        pipeline_id=sales_pipeline["id"],
        stage_id=qualified_stage["id"],
    )

    print(deal)