from integrations.stripe.clients import StripeClient


def main() -> None:
    client = StripeClient()

    customers = client.stripe.Customer.list(
        limit=100,
    )

    print("")
    print("Stripe Customers")
    print("----------------")

    for customer in customers.auto_paging_iter():
        metadata = customer.metadata.to_dict()

        print(f"Customer ID: {customer.id}")
        print(f"Name: {customer.name}")
        print(f"Email: {customer.email}")
        print(
            "HubSpot Company ID: "
            f"{metadata.get('hubspot_company_id')}"
        )
        print("----------------")


if __name__ == "__main__":
    main()