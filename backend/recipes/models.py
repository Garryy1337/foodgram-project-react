from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)
from django.db import models
from users.models import User
from recipes.constants import (
    MIN_AMOUNT,
    MAX_AMOUNT,
    MIN_COOKING_TIME,
    MAX_COOKING_TIME,
)


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=200
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=7,
        null=True,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})',
                message='Поле должно содержать HEX-код выбранного цвета.'
            )
        ]

    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=200,
        unique=True,
        null=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=80,
        verbose_name="Название ингредиента",
        help_text="Название ингредиента",
    )
    measurement_unit = models.CharField(
        max_length=15,
        verbose_name="Единица измерения ингредиента",
        help_text="Единица измерения ингредиента",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

        constraints = (
            models.UniqueConstraint(
                fields=("name", "measurement_unit"),
                name="unique_ingredient",
            ),
        )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название рецепта",
        help_text="Название рецепта",
    )
    text = models.TextField(
        verbose_name="Описание рецепта",
        help_text="Описание рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInRecipe",
        related_name="recipes",
        verbose_name="Игредиенты для рецепта",
        help_text="Игредиенты для рецепта",
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                f'Минимальное значение - {MIN_COOKING_TIME}'),
            MaxValueValidator(
                MAX_COOKING_TIME,
                f'Максимальное значение - {MAX_COOKING_TIME}')
        ],
        verbose_name="Время приготовления, мин.",
        help_text="Время приготовления в минутах",
    )
    image = models.ImageField(
        verbose_name="Изображение для рецепта",
        help_text="Изображение для рецепта",
        upload_to="recipes/",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации рецепта",
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    tags = models.ManyToManyField(
        Tag,
        through="RecipeTags",
        related_name="recipes",
        verbose_name="Теги рецепта",
        help_text="Теги рецепта",
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, verbose_name="Ингредиент"
    )
    amount = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(
                MIN_AMOUNT, f'Минимальное значение - {MIN_AMOUNT}'),
            MaxValueValidator(
                MAX_AMOUNT, f'Максимальное значение - {MAX_AMOUNT}')
        ],
        verbose_name='Количество ингредиента'
    )

    class Meta:
        verbose_name = "Ингредиенты"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"В рецепте {self.recipe} есть ингредиент {self.ingredient}"


class RecipeTags(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="Рецепт"
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="Тег")

    class Meta:
        verbose_name = "Теги"
        verbose_name_plural = "Теги"

    def __str__(self):
        return f"У рецепта {self.recipe} есть тег {self.tag}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_favorite_recipe"
            ),
        )

    def __str__(self):
        return f"Рецепт {self.recipe} в избранном у пользователя {self.user}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_list",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_list",
        verbose_name="Рецепт",
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок"

        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_shopping_list_recipe"
            ),
        )

    def __str__(self):
        return (
            f"Рецепт {self.recipe} в списке покупок у пользователя {self.user}"
        )
