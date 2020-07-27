from typing import Dict

from django.http import HttpResponse

from moonshot.tests import MoonshotFunctionalTestCase, status

from ..models import Payment


class PaymentFTC(MoonshotFunctionalTestCase):

    # Creating payments

    def test_can_start_a_payment_session(self):
        """
        A payment intent is created after a user starts a payment session.
        """

        response: HttpResponse = self.client.post(
            "/payments/", dict(amount=5000, currency="GBP", email="luke@themoon.org")
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        instance = Payment.objects.get(uuid=response.data["uuid"])
        self.assertEqual(instance.amount, 5000)
        self.assertEqual(instance.currency, "GBP")
        self.assertEqual(instance.email, "luke@themoon.org")
        self.assertEqual(instance.status, "created")

    def test_cannot_start_payment_session_without_required_attributes(self):

        count = Payment.objects.count()

        required_attrs = ["amount", "currency", "email"]

        for attr in required_attrs:
            body: Dict = dict(amount=5000, currency="GBP", email="luke@themoon.org")
            body.pop(attr)
            response: HttpResponse = self.client.post(
                "/payments/", body,
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Payment.objects.count(), count)
