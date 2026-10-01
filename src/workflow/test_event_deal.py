"""
Temporary test for the Deal Closed Won domain event.

This script validates the event model before connecting the
CRM workflow to the Stripe billing integration.
"""

from domain.events import DealClosedWonEvent


def main() -> None:

    event = DealClosedWonEvent.create(
        deal_id="65514507983",
        company_id="58819345672",
        contact_id="252076728918",
        customer_name="Acme Corporation",
        customer_email="sarah.johnson@acme.example",
        product_code="enterprise",
        contract_value=60000,
        monthly_amount=5000,
    )

    print(event)


if __name__ == "__main__":
    main()