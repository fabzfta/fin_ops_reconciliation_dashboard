"""
Close a HubSpot Deal.

This workflow simulates a sales opportunity being successfully closed.

Instead of hardcoding HubSpot internal stage IDs, the workflow
retrieves pipeline metadata and resolves the "Closed Won" stage
dynamically.

In the future, a Closed Won Deal will trigger the billing
provisioning workflow in Stripe.
"""

from integrations.hubspot.clients import HubSpotClient
from integrations.hubspot.deals import HubSpotDeals
from integrations.hubspot.pipeline import HubSpotPipelines


DEAL_ID = "65516507983"


def main() -> None:
    """
    Move the Acme Enterprise Deal to the Closed Won stage.
    """

    client = HubSpotClient()

    pipelines = HubSpotPipelines(client)
    deals = HubSpotDeals(client)

    # Retrieve the sales pipeline dynamically.
    sales_pipeline = pipelines.find_pipeline_by_label(
        "Sales Pipeline"
    )

    # Resolve the target stage from HubSpot metadata instead
    # of depending on an internal hardcoded stage ID.
    closed_won_stage = pipelines.find_stage_by_label(
        sales_pipeline,
        "Closed Won",
    )

    print(
        f"Moving Deal {DEAL_ID} "
        f"to stage '{closed_won_stage['label']}'..."
    )

    deal = deals.update_stage(
        deal_id=DEAL_ID,
        stage_id=closed_won_stage["id"],
    )

    print("Deal updated successfully.")
    print(deal)


if __name__ == "__main__":
    main()