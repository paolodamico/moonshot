import logging

from rest_framework import exceptions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Payment
from .parsers import PlainTextJsonParser
from .serializers import PaymentSerializer
from .stripe import parse_webhook


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.order_by("-created")
    serializer_class = PaymentSerializer


class StripeWebhookView(GenericAPIView):

    response = Response(status=status.HTTP_200_OK)

    parser_classes = (PlainTextJsonParser,)

    def post(self, request, *args, **kwargs):

        signature = request.META.get("HTTP_STRIPE_SIGNATURE", "")
        event = parse_webhook(request.data, signature)

        if not event:  # signature mismatch or invalid payload
            logging.warning(
                "StripeWebhookView#post - Error parsing webhook or signature mismatch.",
            )
            raise exceptions.ValidationError()

        try:
            stripe_id = event.data.object.id
            event_type = event.type
        except AttributeError:
            logging.warning(
                "StripeWebhookView#post - Error parsing webhook, unexpected payload.",
            )
            raise exceptions.ValidationError()

        if event_type == "payment_intent.succeeded":

            try:
                instance = Payment.objects.get(stripe_id=stripe_id,)
            except Payment.DoesNotExist:
                logging.warning(
                    f"StripeWebhookView#post - failed processing {event_type} "
                    "webhook because object was not found.",
                )
                return self.response

            if instance.status != "created":
                logging.warning(
                    "StripeWebhookView#post - ignoring webhook because"
                    f"payment is in an invalid state ({instance.status})."
                )
                return self.response

            # Mark the payment as paid (completed)
            instance.status = "paid"
            instance.save()
        else:
            logging.warning(
                f"StripeWebhookView#post - received unhandled event ({event_type}).",
            )

        return self.response
