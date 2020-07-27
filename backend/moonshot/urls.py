"""moonshot URL Configuration
"""
from typing import List

from api.views import PaymentViewSet, StripeWebhookView
from django.urls import path

urlpatterns: List = [
    path(
        "payments/",
        view=PaymentViewSet.as_view({"get": "list", "post": "create"}),
        name="payments",
    ),
    path("webhook/", view=StripeWebhookView.as_view(), name="stripe-webhook"),
]
