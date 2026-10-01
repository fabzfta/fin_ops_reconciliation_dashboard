"""
Business domain events.

Domain events represent meaningful business state changes that can
trigger workflows across different systems.

They intentionally do not contain implementation details from
external platforms such as HubSpot or Stripe.
"""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class DealClosedWonEvent:
    """
    Event emitted when a CRM sales opportunity is successfully closed.

    This event creates a boundary between the CRM domain and downstream
    systems such as billing and accounting.
    """

    deal_id: str
    company_id: str
    contact_id: str

    customer_name: str
    customer_email: str

    product_code: str

    contract_value: float
    monthly_amount: float

    currency: str

    occurred_at: datetime

    @classmethod
    def create(
        cls,
        deal_id: str,
        company_id: str,
        contact_id: str,
        customer_name: str,
        customer_email: str,
        product_code: str,
        contract_value: float,
        monthly_amount: float,
        currency: str = "USD",
    ) -> "DealClosedWonEvent":
        """
        Create a DealClosedWonEvent using the current UTC timestamp.
        """

        return cls(
            deal_id=deal_id,
            company_id=company_id,
            contact_id=contact_id,
            customer_name=customer_name,
            customer_email=customer_email,
            product_code=product_code,
            contract_value=contract_value,
            monthly_amount=monthly_amount,
            currency=currency,
            occurred_at=datetime.now(timezone.utc),
        )