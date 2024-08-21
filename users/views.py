from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializer import PaymentSerializer, UserSerializer, UserTokenObtainPairSerializer
from users.models import Payments, User
from rest_framework.permissions import AllowAny


class PaymentListAPIView(ListAPIView):
    """ Вывод платежей изначально по убыванию даты покупки.
    Но есть возможность изменить порядок сортировки по возрастанию.
    Так же доступна фильтрация по полям """
    queryset = Payments.objects.all().order_by('-payment_date')
    serializer_class = PaymentSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('payment_date',)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        # user.set_password(user.password)
        user.set_password(self.request.data.get('password'))
        user.save()


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
