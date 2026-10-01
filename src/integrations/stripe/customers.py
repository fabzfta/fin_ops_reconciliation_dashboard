"""
Stripe Customers API.

This module manages customer provisioning in Stripe.

HubSpot Company IDs are stored in Stripe metadata so that customer
identity can be preserved across CRM and billing systems.
"""

from integrations.stripe.clients import StripeClient


class StripeCustomers:
    """
    Service responsible for Stripe Customer operations.
    """

    def __init__(self, client: StripeClient) -> None:
        self.client = client

    def find_by_hubspot_company_id(
        self,
        hubspot_company_id: str,
    ):
        """
        Find a Stripe customer using its HubSpot Company ID.

        Args:
            hubspot_company_id:
                External CRM identifier associated with the customer.

        Returns:
            Stripe Customer if found, otherwise None.
        """

        customers = self.client.stripe.Customer.list(
            limit=100,
        )

        for customer in customers.auto_paging_iter():

            metadata = customer.metadata.to_dict()

            if (
                metadata.get("hubspot_company_id")
                == hubspot_company_id
            ):
                return customer

        return None

    def create_customer(
        self,
        hubspot_company_id: str,
        name: str,
        email: str,
    ):
        """
        Create a Stripe customer linked to a HubSpot Company.
        """

        return self.client.stripe.Customer.create(
            name=name,
            email=email,
            metadata={
                "hubspot_company_id": hubspot_company_id,
            },
        )

    def get_or_create_customer(
        self,
        hubspot_company_id: str,
        name: str,
        email: str,
    ):
        """
        Return an existing customer or create it when necessary.
        """

        customer = self.find_by_hubspot_company_id(
            hubspot_company_id
        )

        if customer:
            print(
                f"Customer already exists: "
                f"{customer.name} ({customer.id})"
            )
            return customer

        customer = self.create_customer(
            hubspot_company_id=hubspot_company_id,
            name=name,
            email=email,
        )

        print(
            f"Customer created: "
            f"{customer.name} ({customer.id})"
        )

        return customer

    def attach_test_payment_method(
        self,
        customer_id: str,
        payment_method_id: str = "pm_card_visa",
    ):
        """
        Attach a Stripe test payment method to a customer and configure
        it as the default payment method for future invoices.

        This method must only be used in Stripe sandbox/test environments.

        Args:
            customer_id:
                Stripe Customer ID.

            payment_method_id:
                Stripe test PaymentMethod identifier.

        Returns:
            Stripe PaymentMethod attached to the customer.
        """

        payment_method = self.client.stripe.PaymentMethod.attach(
            payment_method_id,
            customer=customer_id,
        )

        # Use the PaymentMethod returned by Stripe.
        #
        # Stripe test tokens such as "pm_card_visa" may result in an
        # actual PaymentMethod resource with its own generated ID.
        attached_payment_method_id = payment_method.id

        self.client.stripe.Customer.modify(
            customer_id,
            invoice_settings={
                "default_payment_method": attached_payment_method_id,
            },
        )

        print(
            f"Payment method configured: "
            f"{attached_payment_method_id}"
        )

        return payment_method