from django.urls import path
from users.apps import UsersConfig
from users.views import (PaymentListAPIView, UserCreateAPIView, UserListAPIView,
                         UserRetrieveAPIView, UserDestroyAPIView, UserUpdateAPIView)
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import UserTokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListAPIView.as_view(), name='users_list'),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='users_retrieve'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='users_update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='users_delete'),
    path("login/", UserTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
]
