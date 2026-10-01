"""
Extract QuickBooks entities into the local RAW storage layer.

This workflow retrieves accounting records from QuickBooks Online
and persists the original API payloads without applying business
transformations.

All objects extracted during the same execution share the same
run_id, allowing the ingestion batch to be traced and audited.
"""

from datetime import datetime, timezone
from pathlib import Path

from integrations.quickbooks.clients import QuickBooksClient
from storage.storage import LocalObjectStorage


# ------------------------------------------------------------------
# QuickBooks source identifiers
# ------------------------------------------------------------------

CUSTOMER_ID = "58"
INVOICE_ID = "145"
PAYMENT_ID = "146"


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


def extract_query_result(
    response: dict,
    entity_name: str,
) -> dict:
    """
    Extract a single QuickBooks entity from a QueryResponse.

    QuickBooks Query API responses have the following structure:

        {
            "QueryResponse": {
                "Customer": [...]
            }
        }

    Args:
        response:
            Raw response returned by QuickBooks.

        entity_name:
            QuickBooks entity name, such as Customer,
            Invoice, or Payment.

    Returns:
        dict:
            The first matching QuickBooks entity.

    Raises:
        ValueError:
            If the requested entity cannot be found.
    """

    query_response = response.get(
        "QueryResponse",
        {},
    )

    results = query_response.get(
        entity_name,
        [],
    )

    if not results:
        raise ValueError(
            f"QuickBooks {entity_name} not found."
        )

    return results[0]


def store_quickbooks_object(
    storage: LocalObjectStorage,
    entity: str,
    object_id: str,
    payload: dict,
    run_id: str,
) -> Path:
    """
    Persist a QuickBooks object in the RAW storage layer.

    Args:
        storage:
            RAW object storage implementation.

        entity:
            Entity directory name.

        object_id:
            QuickBooks entity identifier.

        payload:
            Original QuickBooks API payload.

        run_id:
            Current ingestion run identifier.

    Returns:
        Path:
            Location where the RAW object was stored.
    """

    return storage.put_json(
        source="quickbooks",
        entity=entity,
        object_id=object_id,
        payload=payload,
        run_id=run_id,
    )


def main() -> None:
    """
    Extract QuickBooks Customer, Invoice, and Payment records
    and persist their RAW payloads.
    """

    run_id = generate_run_id()

    # --------------------------------------------------------------
    # Initialize services
    # --------------------------------------------------------------

    client = QuickBooksClient()
    storage = LocalObjectStorage()

    print("")
    print("QuickBooks RAW Ingestion")
    print("========================")
    print(f"Run ID: {run_id}")

    # --------------------------------------------------------------
    # Customer
    # --------------------------------------------------------------

    print("")
    print("Extracting QuickBooks Customer...")

    customer_response = client.query(
        f"SELECT * FROM Customer WHERE Id = '{CUSTOMER_ID}'"
    )

    customer = extract_query_result(
        response=customer_response,
        entity_name="Customer",
    )

    customer_path = store_quickbooks_object(
        storage=storage,
        entity="customers",
        object_id=customer["Id"],
        payload=customer,
        run_id=run_id,
    )

    print(
        f"Customer stored: {customer['Id']}"
    )
    print(
        f"Path: {customer_path}"
    )

    # --------------------------------------------------------------
    # Invoice
    # --------------------------------------------------------------

    print("")
    print("Extracting QuickBooks Invoice...")

    invoice_response = client.query(
        f"SELECT * FROM Invoice WHERE Id = '{INVOICE_ID}'"
    )

    invoice = extract_query_result(
        response=invoice_response,
        entity_name="Invoice",
    )

    invoice_path = store_quickbooks_object(
        storage=storage,
        entity="invoices",
        object_id=invoice["Id"],
        payload=invoice,
        run_id=run_id,
    )

    print(
        f"Invoice stored: {invoice['Id']}"
    )
    print(
        f"Path: {invoice_path}"
    )

    # --------------------------------------------------------------
    # Payment
    # --------------------------------------------------------------

    print("")
    print("Extracting QuickBooks Payment...")

    payment_response = client.query(
        f"SELECT * FROM Payment WHERE Id = '{PAYMENT_ID}'"
    )

    payment = extract_query_result(
        response=payment_response,
        entity_name="Payment",
    )

    payment_path = store_quickbooks_object(
        storage=storage,
        entity="payments",
        object_id=payment["Id"],
        payload=payment,
        run_id=run_id,
    )

    print(
        f"Payment stored: {payment['Id']}"
    )
    print(
        f"Path: {payment_path}"
    )

    # --------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------

    print("")
    print(
        "QuickBooks RAW ingestion completed successfully."
    )
    print(
        "------------------------------------------------"
    )
    print(f"Run ID: {run_id}")
    print("Objects stored: 3")


if __name__ == "__main__":
    main()