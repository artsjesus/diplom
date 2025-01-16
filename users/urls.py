from users.apps import UsersConfig
from django.urls import path
from users.views import UserCreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from users.views import ResetPasswordView, ResetPasswordConfirmView

app_name = UsersConfig.name


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("reset_password/", ResetPasswordView.as_view(), name="reset_password"),
    path(
        "reset_password_confirm/",
        ResetPasswordConfirmView.as_view(),
        name="reset_password_confirm",
    ),
]
