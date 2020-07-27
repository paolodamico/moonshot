from typing import Tuple

from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_API_KEY


def create_payment_intent(id: str, amount: int, currency: str) -> Tuple[str, str]:

    intent: stripe.PaymentIntent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        metadata=dict(
            moonshot_id=id, integration_check="accept_a_payment"
        ),  # Verify integration @ https://stripe.com/docs/payments/accept-a-payment
    )

    return (intent.id, intent.client_secret)
