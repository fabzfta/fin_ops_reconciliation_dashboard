"""
QuickBooks Payment integration.

Creates customer payments and applies them to QuickBooks invoices
while preventing duplicate payment processing.
"""

from integrations.quickbooks.clients import QuickBooksClient


class QuickBooksPayments:
    """
    Manage QuickBooks Online customer payments.
    """

    STRIPE_REFERENCE_PREFIX = "Stripe PaymentIntent:"

    def __init__(
        self,
        client: QuickBooksClient,
    ) -> None:
        self.client = client

    def list_payments(self) -> list[dict]:
        """
        Return QuickBooks customer payments.
        """

        response = self.client.query(
            "SELECT * FROM Payment MAXRESULTS 1000"
        )

        return (
            response
            .get("QueryResponse", {})
            .get("Payment", [])
        )

    def find_by_stripe_payment_intent_id(
        self,
        stripe_payment_intent_id: str,
    ) -> dict | None:
        """
        Find a payment previously created from a Stripe PaymentIntent.
        """

        expected_reference = (
            f"{self.STRIPE_REFERENCE_PREFIX} "
            f"{stripe_payment_intent_id}"
        )

        for payment in self.list_payments():
            if payment.get("PrivateNote") == expected_reference:
                return payment

        return None

    def create_payment(
        self,
        customer_id: str,
        invoice_id: str,
        amount: float,
        stripe_payment_intent_id: str,
        transaction_date: str,
    ) -> dict:
        """
        Create a QuickBooks payment and apply it to an invoice.
        """

        endpoint = (
            f"/v3/company/"
            f"{self.client.realm_id}/payment"
        )

        payload = {
            "CustomerRef": {
                "value": customer_id,
            },
            "TxnDate": transaction_date,
            "TotalAmt": amount,
            "PrivateNote": (
                f"{self.STRIPE_REFERENCE_PREFIX} "
                f"{stripe_payment_intent_id}"
            ),
            "Line": [
                {
                    "Amount": amount,
                    "LinkedTxn": [
                        {
                            "TxnId": invoice_id,
                            "TxnType": "Invoice",
                        }
                    ],
                }
            ],
        }

        response = self.client.post(
            endpoint,
            json=payload,
        )

        return response["Payment"]

    def get_or_create_payment(
        self,
        customer_id: str,
        invoice_id: str,
        amount: float,
        stripe_payment_intent_id: str,
        transaction_date: str,
    ) -> dict:
        """
        Return an existing payment or create it when missing.
        """

        payment = self.find_by_stripe_payment_intent_id(
            stripe_payment_intent_id
        )

        if payment:
            print(
                f"Payment already exists: "
                f"{payment['Id']} "
                f"(Stripe: {stripe_payment_intent_id})"
            )

            return payment

        payment = self.create_payment(
            customer_id=customer_id,
            invoice_id=invoice_id,
            amount=amount,
            stripe_payment_intent_id=stripe_payment_intent_id,
            transaction_date=transaction_date,
        )

        print(
            f"Payment created: "
            f"{payment['Id']} "
            f"(Stripe: {stripe_payment_intent_id})"
        )

        return payment