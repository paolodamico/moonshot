from typing import Optional, Tuple

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_payment_intent(
    id: str, amount: int, currency: str, email: str
) -> Tuple[str, str]:

    intent: stripe.PaymentIntent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        receipt_email=email,
        metadata=dict(
            moonshot_id=id, integration_check="accept_a_payment"
        ),  # Verify integration @ https://stripe.com/docs/payments/accept-a-payment
    )

    return (intent.id, intent.client_secret)


def parse_webhook(payload: str, signature: str) -> Optional[stripe.Event]:
    try:
        event = stripe.Webhook.construct_event(
            payload, signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        event = None
    return event


def compute_webhook_signature(payload: str) -> str:
    return stripe.webhook.WebhookSignature._compute_signature(
        payload, settings.STRIPE_WEBHOOK_SECRET
    )
