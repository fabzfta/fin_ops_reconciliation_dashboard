"""
Billing provisioning workflow.

This workflow consumes a DealClosedWonEvent and provisions the
corresponding customer and subscription in Stripe.

The workflow connects the CRM domain to the billing domain without
introducing Stripe-specific implementation details into HubSpot code.
"""

from domain.events import DealClosedWonEvent

from integrations.stripe.clients import StripeClient
from integrations.stripe.customers import StripeCustomers
from integrations.stripe.products import StripeProducts
from integrations.stripe.subscriptions import StripeSubscriptions


def provision_billing(
    event: DealClosedWonEvent,
) -> None:
    """
    Provision Stripe billing resources for a Closed Won Deal.
    """

    print(
        f"Processing DealClosedWonEvent "
        f"for Deal {event.deal_id}"
    )

    client = StripeClient()

    products = StripeProducts(client)
    customers = StripeCustomers(client)
    subscriptions = StripeSubscriptions(client)

    # Resolve the Stripe billing price using the internal
    # product code from the domain event.
    price = products.get_price_for_product_code(
        event.product_code
    )

    print(
        f"Resolved product '{event.product_code}' "
        f"to Stripe price {price.id}"
    )

    # Preserve customer identity across CRM and billing systems.
    customer = customers.get_or_create_customer(
        hubspot_company_id=event.company_id,
        name=event.customer_name,
        email=event.customer_email,
    )

    # Configure a test payment method for the sandbox customer.
    #
    # In production, payment method collection would happen through
    # Stripe Checkout, Elements, or another secure payment flow.
    customers.attach_test_payment_method(
        customer_id=customer.id,
    )

    # Preserve Deal -> Subscription identity so retries cannot
    # accidentally create duplicate subscriptions.
    subscription = subscriptions.get_or_create_subscription(
        customer_id=customer.id,
        price_id=price.id,
        hubspot_deal_id=event.deal_id,
    )

    print("")
    print("Billing provisioning completed.")
    print(f"Stripe Customer: {customer.id}")
    print(f"Subscription: {subscription.id}")


if __name__ == "__main__":

    # Temporary event fixture.
    #
    # Later this event will come automatically from the CRM workflow
    # instead of being manually constructed here.
    event = DealClosedWonEvent.create(
        deal_id="65516507983",
        company_id="58819345672",
        contact_id="252076728918",
        customer_name="Acme Corporation",
        customer_email="sarah.johnson@acme.example",
        product_code="enterprise",
        contract_value=60000,
        monthly_amount=5000,
    )

    provision_billing(event)