import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        """Тест создания пользователя"""
        user = User.objects.create(
            first_name="Иван",
            last_name="Иванов",
            email="ivan@example.com",
            phone="1234567890",
            password="password123"
        )
        assert user.email == "ivan@example.com"
        assert user.password == "password123"
        assert str(user.email) == "ivan@example.com"

    def test_user_role_default(self):
        """Тест значения роли по умолчанию"""
        user = User.objects.create(
            first_name="Алиса",
            email="alisa@example.com",
            password="securepass"
        )
        assert user.role is False  # Обычный пользователь по умолчанию

@pytest.mark.django_db
class TestUserAPI:
    client = APIClient()

    def test_user_create_api(self):
        """Тест API создания пользователя"""
        data = {
            "first_name": "Тест",
            "last_name": "Пользователь",
            "email": "test@example.com",
            "phone": "123456789",
            "password": "testpass123"
        }
        response = self.client.post("/users/register/", data, format="json")
        assert response.status_code == 201
        assert User.objects.filter(email="test@example.com").exists()

    def test_reset_password_request(self, mailoutbox):
        """Тест отправки запроса на сброс пароля"""
        user = User.objects.create(email="testuser@example.com", password="testpassword")
        response = self.client.post("/users/reset_password/", {"email": "testuser@example.com"})

        assert response.status_code == 200
        assert len(mailoutbox) == 1  # Проверяем, что письмо отправлено
        assert "Сброс пароля" in mailoutbox[0].subject
        response = self.client.post("/users/reset_password/", {"email": "123@example.com"})
        assert response.status_code == 404

    def test_reset_password_confirm(self):
        """Тест подтверждения сброса пароля"""
        user = User.objects.create(email="testuser@example.com", password="oldpassword")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        data = {
            "uid": uid,
            "token": token,
            "new_password": "newsecurepassword"
        }
        response = self.client.post("/users/reset_password_confirm/", data, format="json")

        assert response.status_code == 200
        user.refresh_from_db()
        assert user.check_password("newsecurepassword")
        token = '12141'
        data = {
            "uid": uid,
            "token": token,
            "new_password": "newsecurepassword"
        }
        response = self.client.post("/users/reset_password_confirm/", data, format="json")
        assert response.status_code == 400