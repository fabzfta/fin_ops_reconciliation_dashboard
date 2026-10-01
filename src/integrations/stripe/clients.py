"""
Stripe API Client.

This module provides the base configuration required to interact
with the Stripe API.

The client is responsible for:

- Loading the Stripe secret key from environment variables.
- Configuring the Stripe Python SDK.
- Providing access to Stripe resources.

Business-specific operations such as creating customers,
products, prices, and subscriptions belong in separate services.
"""

import os

import stripe
from dotenv import load_dotenv


load_dotenv()


class StripeClient:
    """
    Configure and expose the Stripe Python SDK.
    """

    def __init__(self) -> None:
        """
        Initialize Stripe authentication using environment variables.

        Raises:
            ValueError:
                If STRIPE_SECRET_KEY is not configured.
        """

        self.secret_key = os.getenv("STRIPE_SECRET_KEY")

        if not self.secret_key:
            raise ValueError(
                "STRIPE_SECRET_KEY is not configured."
            )

        # Configure authentication for every request performed
        # through the Stripe SDK.
        stripe.api_key = self.secret_key

        self.stripe = stripe