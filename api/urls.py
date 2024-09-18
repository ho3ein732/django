from django.urls import path
from . import views
app_name = 'api'

urlpatterns = [
    # region user
    path('send-code/', views.SendVerificationCodeApiView.as_view(), name='register'),
    path('register/', views.UserRegistrationWithCodeApiView.as_view(), name='register'),
    path('users-list/', views.UserListApiView.as_view(), name='list_users'),
    # path('user-detail/<pk>', views.UserDetailApiView.as_view(), name='user_detail'),
    path('user-update/', views.UserUpdateApiView.as_view(), name='user_update'),
    path('user-add-address/', views.UserAddAddressApiView.as_view(), name='user_add_address'),

    # endregion
]