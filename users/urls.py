from django.urls import path
from users.apps import UsersConfig
from users.views import Payments

app_name = UsersConfig.name

urlpatterns = [
    path('users/', UsersListView.as_view(), name='users_list'),
    path('<int:pk>/user_update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/user_profile/', UserDetailView.as_view(), name='user_profile'),
    path('<int:pk>/user_profile_update/', UserProfileUpdateView.as_view(), name='user_update_profile'),
    path('<int:pk>/use_delete/', UserDeleteView.as_view(), name='user_delete'),
]
