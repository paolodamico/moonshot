from typing import Dict

from rest_framework import serializers

from .models import PRODUCTS, Payment
from .stripe import create_payment_intent


class PaymentSerializer(serializers.ModelSerializer):

    client_secret = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = (
            "uuid",
            "amount",
            "currency",
            "status",
            "email",
            "client_secret",
            "product_id",
        )
        extra_kwargs: Dict = dict(
            status=dict(read_only=True),
            amount=dict(required=False),
            email=dict(required=True),
        )

    def get_client_secret(self, obj: Payment) -> str:
        return obj._client_secret if hasattr(obj, "_client_secret") else None

    def validate_product_id(self, value):
        if value not in PRODUCTS:
            raise serializers.ValidationError("Invalid product.")
        return value

    def validate(self, data):
        product: Dict = PRODUCTS[data["product_id"]]
        data["amount"] = product["amount"]
        data["currency"] = product["currency"]
        return data

    def create(self, validated_data: Dict) -> Payment:

        # Create the internal instance first (to generate the ID)
        instance: Payment = super().create(validated_data)

        # Create the PaymentIntent with Stripe first
        stripe_id, client_secret = create_payment_intent(
            id=instance.uuid,
            amount=instance.amount,
            currency=instance.currency,
            email=instance.email,
        )

        # Update the instance with the PaymentIntent ID
        instance.stripe_id = stripe_id
        instance._client_secret = client_secret
        instance.save()

        return instance
