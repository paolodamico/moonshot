from typing import Dict

from rest_framework import serializers

from .models import Payment
from .stripe import create_payment_intent


class PaymentSerializer(serializers.ModelSerializer):

    client_secret = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ("uuid", "amount", "currency", "status", "email", "client_secret")
        extra_kwargs: Dict = dict(
            status=dict(read_only=True),
            currency=dict(required=True),
            email=dict(required=True),
        )

    def get_client_secret(self, obj: Payment) -> str:
        return obj._client_secret if hasattr(obj, "_client_secret") else None

    def create(self, validated_data: Dict) -> Payment:

        # Create the internal instance first (to generate the ID)
        instance: Payment = super().create(validated_data)

        # Create the PaymentIntent with Stripe first
        stripe_id, client_secret = create_payment_intent(
            id=instance.id, amount=instance.amount, currency=instance.currency
        )

        # Update the instance with the PaymentIntent ID
        instance.stripe_id = stripe_id
        instance._client_secret = client_secret
        instance.save()

        return instance
