from rest_framework.viewsets import ModelViewSet

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.order_by("-created")
    serializer_class = PaymentSerializer
