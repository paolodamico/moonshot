from typing import Dict

from django.http import HttpResponse

from moonshot.tests import MoonshotFunctionalTestCase, moonshot_vcr, status

from ..models import Payment


class PaymentFTC(MoonshotFunctionalTestCase):

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
