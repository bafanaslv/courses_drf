from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from users.models import Payments


class PaymentsViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    filterset_fields = ["paid_course", "paid_date", "payment_method"]
