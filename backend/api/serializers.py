from typing import Dict

from rest_framework import serializers

from .models import Payment


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
        return obj._client_secret if hasattr(obj, "client_secret") else None
