from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from users.serializer import PaymentSerializer
from users.models import Payments


class PaymentListAPIView(ListAPIView):
    """ Вывод платежей изначально по убыванию даты покупки.
    Но есть возможность изменить порядок сортировки по возрастанию.
    Так же доступна фильтрация по полям """
    queryset = Payments.objects.all().order_by('-payment_date')
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('payment_date',)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
