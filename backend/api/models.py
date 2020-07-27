import uuid
from typing import Dict

from django.core.validators import MinValueValidator
from django.db import models

PRODUCTS: Dict = {
    "photoshoot": dict(amount=19999, currency="USD"),
    "troubleshoot": dict(amount=399999, currency="GBP"),
    "peashoot": dict(amount=399, currency="USD"),
    "shootout": dict(amount=4999, currency="GBP"),
}


class Payment(models.Model):

    CURRENCY_CHOICES = (
        ("USD", "US Dollar"),
        ("GBP", "British Pound"),
    )

    STATUS_CHOICES = (
        ("created", "Created"),
        ("paid", "Paid"),
        ("requires_action", "Requires authentication"),
        ("cancelled", "Cancelled"),
        ("fulfilled", "Fulfilled"),
    )

    uuid = models.UUIDField(
        "uuid", unique=True, db_index=True, default=uuid.uuid4, editable=False
    )
    stripe_id = models.CharField(
        "stripe ID", max_length=128, db_index=True, blank=True,
    )
    amount = models.IntegerField(
        "amount", validators=[MinValueValidator(1)]
    )  # in smallest currency unit
    currency = models.CharField(
        "currency", max_length=3, choices=CURRENCY_CHOICES, default="USD"
    )
    status = models.CharField(
        "status", max_length=16, choices=STATUS_CHOICES, default="created"
    )
    email = models.EmailField("email", blank=True)
    product_id = models.CharField("product ID", max_length=64)
    created = models.DateTimeField(auto_now_add=True)
