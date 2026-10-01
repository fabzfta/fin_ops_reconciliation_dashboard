"""
Extract Stripe financial entities into the local RAW storage layer.

This workflow retrieves Stripe operational records and persists the
original API payloads without applying business transformations.

All objects extracted during the same execution share the same run_id,
allowing the ingestion batch to be traced and audited.
"""

import os

from datetime import datetime, timezone

import stripe
from dotenv import load_dotenv

from storage.storage import LocalObjectStorage


load_dotenv()


# ------------------------------------------------------------------
# Stripe configuration
# ------------------------------------------------------------------

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")


# ------------------------------------------------------------------
# Source identifiers
# ------------------------------------------------------------------

CUSTOMER_ID = "cus_VMAM1HOvvtovjS"

INVOICE_ID = "in_1ULSBgCvIOVmaa3UhgzKKQaj"

PAYMENT_INTENT_ID = "pi_3ULSBgCvIOVmaa3U0Jlu2dU1"

CHARGE_ID = "ch_3ULSBgCvIOVmaa3U0x5OFv9d"

BALANCE_TRANSACTION_ID = "txn_3ULSBgCvIOVmaa3U0HYW26hP"


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


def stripe_object_to_dict(
    stripe_object,
) -> dict:
    """
    Convert a Stripe SDK object into a plain Python dictionary.

    StripeObject instances may contain nested Stripe objects.
    to_dict_recursive() ensures the complete payload can be serialized
    by the storage layer.

    Args:
        stripe_object:
            Object returned by the Stripe Python SDK.

    Returns:
        dict:
            Recursively converted Stripe payload.
    """

    return stripe_object.to_dict()


def store_stripe_object(
    storage: LocalObjectStorage,
    entity: str,
    stripe_object,
    run_id: str,
):
    """
    Persist a Stripe object in the RAW storage layer.

    Args:
        storage:
            RAW object storage implementation.

        entity:
            Stripe entity name used in the storage path.

        stripe_object:
            Object returned by the Stripe SDK.

        run_id:
            Current ingestion run identifier.

    Returns:
        Path:
            Location where the RAW JSON object was stored.
    """

    payload = stripe_object_to_dict(
        stripe_object
    )

    object_id = payload["id"]

    return storage.put_json(
        source="stripe",
        entity=entity,
        object_id=object_id,
        payload=payload,
        run_id=run_id,
    )


def main() -> None:
    """
    Extract Stripe financial entities and persist their RAW payloads.
    """

    if not STRIPE_SECRET_KEY:
        raise ValueError(
            "STRIPE_SECRET_KEY is not set in the environment variables."
        )

    stripe.api_key = STRIPE_SECRET_KEY

    run_id = generate_run_id()

    storage = LocalObjectStorage()

    print("")
    print("Stripe RAW Ingestion")
    print("====================")
    print(f"Run ID: {run_id}")

    # --------------------------------------------------------------
    # Customer
    # --------------------------------------------------------------

    print("")
    print("Extracting Stripe Customer...")

    customer = stripe.Customer.retrieve(
        CUSTOMER_ID
    )

    customer_path = store_stripe_object(
        storage=storage,
        entity="customers",
        stripe_object=customer,
        run_id=run_id,
    )

    print(f"Customer stored: {customer.id}")
    print(f"Path: {customer_path}")

    # --------------------------------------------------------------
    # Invoice
    # --------------------------------------------------------------

    print("")
    print("Extracting Stripe Invoice...")

    invoice = stripe.Invoice.retrieve(
        INVOICE_ID
    )

    invoice_path = store_stripe_object(
        storage=storage,
        entity="invoices",
        stripe_object=invoice,
        run_id=run_id,
    )

    print(f"Invoice stored: {invoice.id}")
    print(f"Path: {invoice_path}")

    # --------------------------------------------------------------
    # Payment Intent
    # --------------------------------------------------------------

    print("")
    print("Extracting Stripe PaymentIntent...")

    payment_intent = stripe.PaymentIntent.retrieve(
        PAYMENT_INTENT_ID
    )

    payment_intent_path = store_stripe_object(
        storage=storage,
        entity="payment_intents",
        stripe_object=payment_intent,
        run_id=run_id,
    )

    print(f"PaymentIntent stored: {payment_intent.id}")
    print(f"Path: {payment_intent_path}")

    # --------------------------------------------------------------
    # Charge
    # --------------------------------------------------------------

    print("")
    print("Extracting Stripe Charge...")

    charge = stripe.Charge.retrieve(
        CHARGE_ID
    )

    charge_path = store_stripe_object(
        storage=storage,
        entity="charges",
        stripe_object=charge,
        run_id=run_id,
    )

    print(f"Charge stored: {charge.id}")
    print(f"Path: {charge_path}")

    # --------------------------------------------------------------
    # Balance Transaction
    # --------------------------------------------------------------

    print("")
    print("Extracting Stripe Balance Transaction...")

    balance_transaction = stripe.BalanceTransaction.retrieve(
        BALANCE_TRANSACTION_ID
    )

    balance_transaction_path = store_stripe_object(
        storage=storage,
        entity="balance_transactions",
        stripe_object=balance_transaction,
        run_id=run_id,
    )

    print(
        "Balance Transaction stored: "
        f"{balance_transaction.id}"
    )
    print(
        f"Path: {balance_transaction_path}"
    )

    # --------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------

    print("")
    print("Stripe RAW ingestion completed successfully.")
    print("--------------------------------------------")
    print(f"Run ID: {run_id}")
    print("Objects stored: 5")


if __name__ == "__main__":
    main()