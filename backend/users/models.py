from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q
from users.user_constants import UserFieldLength


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password',
    ]

    """Модель пользователей."""
    email = models.EmailField(
        max_length=UserFieldLength.EMAIL_MAX_LENGTH,
        unique=True,
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
