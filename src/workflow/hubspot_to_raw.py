"""
Extract HubSpot CRM entities into the local RAW storage layer.

This workflow retrieves operational CRM records from HubSpot and
persists the original API payloads without applying business
transformations.

All entities extracted during the same execution share the same
run_id, allowing the ingestion batch to be traced and audited.
"""

import os

from datetime import datetime, timezone

from dotenv import load_dotenv

from integrations.hubspot.clients import HubSpotClient
from integrations.hubspot.companies import HubSpotCompanies
from integrations.hubspot.contacts import HubSpotContacts
from integrations.hubspot.deals import HubSpotDeals
from storage.storage import LocalObjectStorage


load_dotenv()


# ------------------------------------------------------------------
# Source identifiers
# ------------------------------------------------------------------

COMPANY_ID = "58819345672"
DEAL_ID = "65516507983"

# Keep personal/test emails outside the source code.
CONTACT_EMAIL = os.getenv("HUBSPOT_CONTACT_EMAIL")


def generate_run_id() -> str:
    """
    Generate a unique identifier for the ingestion run.

    Returns:
        str:
            UTC timestamp formatted as an ingestion run identifier.
    """

    return datetime.now(
        timezone.utc
    ).strftime("%Y%m%dT%H%M%S%fZ")


def main() -> None:
    """
    Extract HubSpot Company, Contact, and Deal records
    and persist their raw API payloads.
    """

    if not CONTACT_EMAIL:
        raise ValueError(
            "HUBSPOT_CONTACT_EMAIL is not set in the environment variables."
        )

    run_id = generate_run_id()

    # --------------------------------------------------------------
    # Initialize services
    # --------------------------------------------------------------

    client = HubSpotClient()

    companies = HubSpotCompanies(client)
    contacts = HubSpotContacts(client)
    deals = HubSpotDeals(client)

    storage = LocalObjectStorage()

    print("")
    print("HubSpot RAW Ingestion")
    print("=====================")
    print(f"Run ID: {run_id}")

    # --------------------------------------------------------------
    # Company
    # --------------------------------------------------------------

    print("")
    print("Extracting HubSpot Company...")

    company = companies.get_by_id(
        COMPANY_ID
    )

    company_path = storage.put_json(
        source="hubspot",
        entity="companies",
        object_id=company["id"],
        payload=company,
        run_id=run_id,
    )

    print(f"Company stored: {company['id']}")
    print(f"Path: {company_path}")

    # --------------------------------------------------------------
    # Contact
    # --------------------------------------------------------------

    print("")
    print("Extracting HubSpot Contact...")

    contact = contacts.get_by_email(
        CONTACT_EMAIL
    )

    if contact is None:
        raise ValueError(
            f"HubSpot Contact not found: {CONTACT_EMAIL}"
        )

    contact_path = storage.put_json(
        source="hubspot",
        entity="contacts",
        object_id=contact["id"],
        payload=contact,
        run_id=run_id,
    )

    print(f"Contact stored: {contact['id']}")
    print(f"Path: {contact_path}")

    # --------------------------------------------------------------
    # Deal
    # --------------------------------------------------------------

    print("")
    print("Extracting HubSpot Deal...")

    deal = deals.get_by_id(
        DEAL_ID
    )

    deal_path = storage.put_json(
        source="hubspot",
        entity="deals",
        object_id=deal["id"],
        payload=deal,
        run_id=run_id,
    )

    print(f"Deal stored: {deal['id']}")
    print(f"Path: {deal_path}")

    # --------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------

    print("")
    print("HubSpot RAW ingestion completed successfully.")
    print("---------------------------------------------")
    print(f"Run ID: {run_id}")
    print("Objects stored: 3")


if __name__ == "__main__":
    main()