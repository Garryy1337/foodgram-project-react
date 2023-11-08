from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_username
from django.db.models import UniqueConstraint, CheckConstraint, Q


class User(AbstractUser):
    class FieldNames:
        USERNAME = 'email'
        REQUIRED = ['username', 'email']

    """Модель пользователей."""
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_username],
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    password = models.CharField(
        max_length=150,
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

        constraints = [
            UniqueConstraint(
                fields=["author", "user"],
                name="unique_subscription",
            ),
            CheckConstraint(
                check=~Q(user=models.F("author")),
                name="user_cannot_follow_himself",
            ),
        ]

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
