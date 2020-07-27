import uuid

from django.core.validators import MinValueValidator
from django.db import models


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
        "stripe ID", max_length=128, unique=True, db_index=True
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
