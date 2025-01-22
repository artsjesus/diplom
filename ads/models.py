from django.db import models
from users.models import User


class Ads(models.Model):
    """объявление"""
    title = models.CharField(max_length=50, verbose_name="Название")
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор")
    created_at = models.DateTimeField(auto_now=True, verbose_name="дата создания")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Комментарий"""
    text = models.TextField(verbose_name="текст")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор")
    ad = models.ForeignKey(Ads, on_delete=models.CASCADE, verbose_name="Объявление")
    created_at = models.DateTimeField(auto_now=True, verbose_name="дата создания")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']

    def __str__(self):
        return self.text
