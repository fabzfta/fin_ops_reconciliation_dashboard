"""
Stripe Products and Prices API.

This module manages NovaTech's billing catalog in Stripe.

The implementation uses internal metadata keys to identify products
instead of depending on Stripe-generated IDs or product names.
"""

from importlib import metadata
from itertools import product

from integrations.stripe.clients import StripeClient


class StripeProducts:
    """
    Service responsible for Stripe Products and Prices.
    """

    def __init__(self, client: StripeClient) -> None:
        self.client = client

    def find_product_by_code(
        self,
        product_code: str,
    ):
        """
        Find an existing Stripe product using NovaTech metadata.

        Args:
            product_code:
                Internal business identifier such as "enterprise".

        Returns:
            Stripe Product if found, otherwise None.
        """

        products = self.client.stripe.Product.list(
            active=True,
            limit=100,
        )

        for product in products.auto_paging_iter():
            metadata = product.metadata.to_dict()

            if metadata.get("product_code") == product_code:
                return product

        return None

    def create_product(
        self,
        product_code: str,
        name: str,
    ):
        """
        Create a Stripe product.

        The internal product code is stored in metadata so our
        application does not depend on the display name.
        """

        return self.client.stripe.Product.create(
            name=name,
            metadata={
                "product_code": product_code,
            },
        )

    def get_or_create_product(
        self,
        product_code: str,
        name: str,
    ):
        """
        Return an existing product or create it when necessary.

        This makes catalog provisioning idempotent.
        """

        product = self.find_product_by_code(product_code)

        if product:
            print(
                f"Product already exists: "
                f"{product.name} ({product.id})"
            )

            return product

        product = self.create_product(
            product_code=product_code,
            name=name,
        )

        print(
            f"Product created: "
            f"{product.name} ({product.id})"
        )

        return product

    def find_monthly_price(
        self,
        product_id: str,
        unit_amount: int,
        currency: str = "usd",
    ):
        """
        Find an active monthly recurring price for a product.

        Stripe stores monetary amounts using the smallest currency
        unit. For USD, 500000 represents $5,000.00.
        """

        prices = self.client.stripe.Price.list(
            product=product_id,
            active=True,
            type="recurring",
            limit=100,
        )

        for price in prices.auto_paging_iter():
            if (
                price.unit_amount == unit_amount
                and price.currency == currency
                and price.recurring.interval == "month"
            ):
                return price

        return None

    def create_monthly_price(
        self,
        product_id: str,
        unit_amount: int,
        currency: str = "usd",
    ):
        """
        Create a monthly recurring Stripe price.
        """

        return self.client.stripe.Price.create(
            product=product_id,
            unit_amount=unit_amount,
            currency=currency,
            recurring={
                "interval": "month",
            },
        )

    def get_or_create_monthly_price(
        self,
        product_id: str,
        unit_amount: int,
        currency: str = "usd",
    ):
        """
        Return an existing monthly price or create it when necessary.
        """

        price = self.find_monthly_price(
            product_id=product_id,
            unit_amount=unit_amount,
            currency=currency,
        )

        if price:
            print(
                f"Price already exists: "
                f"{price.id}"
            )

            return price

        price = self.create_monthly_price(
            product_id=product_id,
            unit_amount=unit_amount,
            currency=currency,
        )

        print(
            f"Price created: "
            f"{price.id}"
        )

        return price

    def get_price_for_product_code(
        self,
        product_code: str,
    ):
        """
        Resolve the active monthly Stripe price for a product code.

        Args:
            product_code:
                NovaTech internal product identifier.

        Returns:
            Stripe Price.

        Raises:
            ValueError:
                If the product or price cannot be found.
        """

        product = self.find_product_by_code(
            product_code
        )

        if not product:
            raise ValueError(
                f"Stripe product '{product_code}' was not found."
            )

        prices = self.client.stripe.Price.list(
            product=product.id,
            active=True,
            type="recurring",
            limit=100,
        )

        for price in prices.auto_paging_iter():

            if price.recurring.interval == "month":
                return price

        raise ValueError(
            f"No active monthly price found for "
            f"product '{product_code}'."
        )