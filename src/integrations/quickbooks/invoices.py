"""
QuickBooks Invoice integration.

Creates accounting invoices from external billing events while
preventing duplicate invoices during event reprocessing.
"""

from integrations.quickbooks.clients import QuickBooksClient


class QuickBooksInvoices:
    """
    Manage QuickBooks Online invoices.
    """

    STRIPE_REFERENCE_PREFIX = "Stripe Invoice:"

    def __init__(
        self,
        client: QuickBooksClient,
    ) -> None:
        self.client = client

    def list_invoices(self) -> list[dict]:
        """
        Return QuickBooks invoices.
        """

        response = self.client.query(
            "SELECT * FROM Invoice MAXRESULTS 1000"
        )

        return (
            response
            .get("QueryResponse", {})
            .get("Invoice", [])
        )

    def find_by_stripe_invoice_id(
        self,
        stripe_invoice_id: str,
    ) -> dict | None:
        """
        Find an invoice previously created from a Stripe invoice.

        PrivateNote is used as the external billing reference.
        """

        expected_reference = (
            f"{self.STRIPE_REFERENCE_PREFIX} "
            f"{stripe_invoice_id}"
        )

        # PrivateNote is not used as a query filter here.
        # We retrieve invoices and compare locally.
        for invoice in self.list_invoices():
            if invoice.get("PrivateNote") == expected_reference:
                return invoice

        return None

    def create_invoice(
        self,
        customer_id: str,
        item_id: str,
        amount: float,
        description: str,
        stripe_invoice_id: str,
        transaction_date: str,
    ) -> dict:
        """
        Create a QuickBooks invoice from a Stripe billing invoice.
        """

        endpoint = (
            f"/v3/company/"
            f"{self.client.realm_id}/invoice"
        )

        payload = {
            "CustomerRef": {
                "value": customer_id,
            },
            "TxnDate": transaction_date,
            "PrivateNote": (
                f"{self.STRIPE_REFERENCE_PREFIX} "
                f"{stripe_invoice_id}"
            ),
            "Line": [
                {
                    "Amount": amount,
                    "Description": description,
                    "DetailType": "SalesItemLineDetail",
                    "SalesItemLineDetail": {
                        "ItemRef": {
                            "value": item_id,
                        },
                        "Qty": 1,
                        "UnitPrice": amount,
                    },
                }
            ],
        }

        response = self.client.post(
            endpoint,
            json=payload,
        )

        return response["Invoice"]

    def get_or_create_invoice(
        self,
        customer_id: str,
        item_id: str,
        amount: float,
        description: str,
        stripe_invoice_id: str,
        transaction_date: str,
    ) -> dict:
        """
        Return the existing QuickBooks invoice or create it.

        This provides idempotency when the same Stripe invoice
        is processed more than once.
        """

        invoice = self.find_by_stripe_invoice_id(
            stripe_invoice_id
        )

        if invoice:
            print(
                f"Invoice already exists: "
                f"{invoice['Id']} "
                f"(Stripe: {stripe_invoice_id})"
            )

            return invoice

        invoice = self.create_invoice(
            customer_id=customer_id,
            item_id=item_id,
            amount=amount,
            description=description,
            stripe_invoice_id=stripe_invoice_id,
            transaction_date=transaction_date,
        )

        print(
            f"Invoice created: "
            f"{invoice['Id']} "
            f"(Stripe: {stripe_invoice_id})"
        )

        return invoice