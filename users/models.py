from django.db import models
from django.contrib.auth.models import AbstractUser


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(max_length=13, **NULLABLE, verbose_name="Телефон")
    email = models.EmailField(unique=True, verbose_name="Email")
    role = models.BooleanField(default=False, verbose_name="Роль")
    image = models.ImageField(
        upload_to="users/image/", **NULLABLE, help_text="Загрузите свой аватар"
    )
    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def str(self):
        return self.email
