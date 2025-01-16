from rest_framework.generics import CreateAPIView, UpdateAPIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from users.models import User
from rest_framework.permissions import AllowAny
from users.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Создаём нового пользователя, и хешируем ему пароль"""

        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(UpdateAPIView):
    """Редактирование профиля пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


User = get_user_model()


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"Ошибка": "Нет пользователя с таким email"},
                status=status.HTTP_404_NOT_FOUND,
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

        send_mail(
            "Сброс пароля",
            f"Перейдите по ссылке чтоб изменить пароль: {reset_url}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return Response(
            {"сообщение": "Письмо для сброса пароля отправлено."},
            status=status.HTTP_200_OK,
        )


class ResetPasswordConfirmView(APIView):

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"Ошибка": "Неверная ссылка для сброса."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response(
                {"Сообщение": "Пароль успешно сброшен"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"Ошибка": "Неверная ссылка для сброса."},
                status=status.HTTP_400_BAD_REQUEST,
            )
