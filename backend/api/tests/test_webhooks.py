from django.http import HttpResponse
from django.utils import timezone

from moonshot.tests import MoonshotFunctionalTestCase, status

from ..models import Payment
from ..stripe import compute_webhook_signature


class WebhookFTC(MoonshotFunctionalTestCase):
    def helper_generate_stripe_signature(self, payload: str):
        timestamp = int(timezone.now().timestamp())
        signature = compute_webhook_signature("%d.%s" % (timestamp, payload))
        return f"t={timestamp},v1={signature}"

    def test_payment_intent_succeeded_webhook(self):

        instance = Payment.objects.create(
            stripe_id="pi_1234567890",
            amount=10000,
            currency="USD",
            email="leia@mars.gov",
        )

        body = """{
            "created":1595888609,
            "livemode":false,
            "id":"evt_00000000000000",
            "type":"payment_intent.succeeded",
            "object":"event",
            "api_version":"2020-03-02",
            "data":{
                "object":{
                    "id":"pi_1234567890",
                    "object":"payment_intent",
                    "mode":null,
                    "amount":10000,
                    "status": "succeeded"
                }
            }
        }"""

        signature: str = self.helper_generate_stripe_signature(body)

        response: HttpResponse = self.client.post(
            "/webhook/", body, format="json-txt", HTTP_STRIPE_SIGNATURE=signature,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, None)

        instance.refresh_from_db()
        self.assertEqual(instance.status, "paid")  # payment should be completed

    def test_payment_intent_succeeded_webhook_cannot_complete_already_completed(self):

        for _status in ["paid", "cancelled", "fulfilled"]:

            instance = Payment.objects.create(
                stripe_id=f"pi_1234567890{_status}",
                amount=10000,
                currency="USD",
                email="leia@mars.gov",
                status=_status,
            )

            body = """{
                "created":1595888609,
                "livemode":false,
                "id":"evt_00000000000000",
                "type":"payment_intent.succeeded",
                "object":"event",
                "api_version":"2020-03-02",
                "data":{
                    "object":{
                        "id":"{payment_intent_id}",
                        "object":"payment_intent",
                        "mode":null,
                        "amount":10000,
                        "status": "succeeded"
                    }
                }
            }"""
            body = body.replace("{payment_intent_id}", f"pi_1234567890{_status}")

            signature: str = self.helper_generate_stripe_signature(body)

            with self.assertLogs(level="WARNING") as logs:
                response: HttpResponse = self.client.post(
                    "/webhook/",
                    body,
                    format="json-txt",
                    HTTP_STRIPE_SIGNATURE=signature,
                )
                self.assertTrue(
                    any("payment is in an invalid state " in r for r in logs.output)
                )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, None)

            instance.refresh_from_db()
            self.assertEqual(instance.status, _status)  # status does not change

    def test_payment_intent_succeeded_webhook_when_payment_is_not_found(self):

        body = """{
            "created":1595888609,
            "livemode":false,
            "id":"evt_00000000000000",
            "type":"payment_intent.succeeded",
            "object":"event",
            "api_version":"2020-03-02",
            "data":{
                "object":{
                    "id":"pi_invalid",
                    "object":"payment_intent",
                    "mode":null,
                    "amount":10000,
                    "status": "succeeded"
                }
            }
        }"""

        signature: str = self.helper_generate_stripe_signature(body)

        with self.assertLogs(level="WARNING") as logs:
            response: HttpResponse = self.client.post(
                "/webhook/", body, format="json-txt", HTTP_STRIPE_SIGNATURE=signature,
            )
            self.assertTrue(
                any("webhook because object was not found" in r for r in logs.output)
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, None)

    def test_stripe_webhook_with_invalid_signature_fails(self):

        instance: Payment = Payment.objects.create(
            stripe_id="pi_abcdefghijklmnop",
            amount=10000,
            currency="USD",
            email="leia@mars.gov",
        )

        body = """{
            "created":1595888609,
            "livemode":false,
            "id":"evt_00000000000000",
            "type":"payment_intent.succeeded",
            "object":"event",
            "api_version":"2020-03-02",
            "data":{
                "object":{
                    "id":"pi_abcdefghijklmnop",
                    "object":"payment_intent",
                    "mode":null,
                    "amount":10000,
                    "status": "succeeded"
                }
            }
        }"""

        signature = self.helper_generate_stripe_signature(body)[
            :-1
        ]  # we remove the last character to make it invalid

        with self.assertLogs(level="WARNING") as logs:
            response: HttpResponse = self.client.post(
                "/webhook/", body, format="json-txt", HTTP_STRIPE_SIGNATURE=signature,
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue(
                any(
                    "Error parsing webhook or signature mismatch." in r
                    for r in logs.output
                )
            )

        instance.refresh_from_db()
        self.assertEqual(
            instance.status, "created"
        )  # make sure the status was not altered
