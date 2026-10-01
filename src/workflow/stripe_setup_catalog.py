"""
Provision the NovaTech SaaS product catalog in Stripe.

The workflow is idempotent: running it multiple times should not
create duplicate products or prices.
"""

from integrations.stripe.clients import StripeClient
from integrations.stripe.products import StripeProducts


PRODUCT_CATALOG = [
    {
        "code": "starter",
        "name": "NovaTech Starter",
        "monthly_amount": 50_000,
    },
    {
        "code": "professional",
        "name": "NovaTech Professional",
        "monthly_amount": 200_000,
    },
    {
        "code": "enterprise",
        "name": "NovaTech Enterprise",
        "monthly_amount": 500_000,
    },
]


def main() -> None:
    client = StripeClient()

    products = StripeProducts(client)

    for item in PRODUCT_CATALOG:

        product = products.get_or_create_product(
            product_code=item["code"],
            name=item["name"],
        )

        price = products.get_or_create_monthly_price(
            product_id=product.id,
            unit_amount=item["monthly_amount"],
        )

        print(
            f"Catalog ready: "
            f"{item['code']} -> {price.id}"
        )


if __name__ == "__main__":
    main()