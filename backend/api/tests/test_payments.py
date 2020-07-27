import random
from typing import Dict

from django.http import HttpResponse

from moonshot.tests import MoonshotFunctionalTestCase, moonshot_vcr, status

from ..models import PRODUCTS, Payment


class PaymentFTC(MoonshotFunctionalTestCase):
    def helper_create_random_payments(self, length: int = 5) -> None:

        for i in range(length):
            product_id: str = random.choice(list(PRODUCTS.keys()))
            Payment.objects.create(
                product_id=product_id,
                amount=PRODUCTS[product_id]["amount"],
                currency=PRODUCTS[product_id]["currency"],
                email=f"person{random.randint(999, 9999)}@moonshot.io",
                status=random.choice([s[0] for s in Payment.STATUS_CHOICES]),
            )

    # Listing payments
    def test_can_list_payments(self):
        self.helper_create_random_payments()

        response: HttpResponse = self.client.get("/payments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["results"]), Payment.objects.count())

        for item in response.data["results"]:
            instance: Payment = Payment.objects.get(uuid=item["uuid"])
            self.assertEqual(item["status"], instance.status)
            self.assertEqual(item["product_id"], instance.product_id)
            self.assertEqual(item["amount"], instance.amount)
            self.assertEqual(item["currency"], instance.currency)

    # Creating payments

    @moonshot_vcr.use_cassette()
    def test_can_start_a_payment_session(self):
        """
        A payment intent is created after a user starts a payment session.
        """

        response: HttpResponse = self.client.post(
            "/payments/", dict(product_id="photoshoot", email="luke@themoon.org")
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure the client secret is present (PaymentIntent is created on Stripe)
        self.assertRegexpMatches(
            response.data["client_secret"], r"^pi_[A-Za-z0-9]+_secret_[A-Za-z0-9]+$"
        )

        instance = Payment.objects.get(uuid=response.data["uuid"])
        self.assertEqual(instance.amount, 19999)
        self.assertEqual(instance.currency, "USD")
        self.assertEqual(instance.email, "luke@themoon.org")
        self.assertEqual(instance.status, "created")
        self.assertRegexpMatches(instance.stripe_id, r"^pi_[A-Za-z0-9]+$")

    def test_cannot_start_payment_session_without_required_attributes(self):

        count = Payment.objects.count()

        required_attrs = ["product_id"]

        for attr in required_attrs:
            body: Dict = dict(product_id="troubleshoot", email="luke@themoon.org")
            body.pop(attr)
            response: HttpResponse = self.client.post(
                "/payments/", body,
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Payment.objects.count(), count)
