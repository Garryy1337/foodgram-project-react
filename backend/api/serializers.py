from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import exceptions, serializers

from api.pagination import PageNumberPagination
from recipes.constants import IngredientValidAmount, RecipeValidTime
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Subscription, User


class CustomUserSerializer(UserSerializer):
    """Проверка подписки."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        user_id = self.context.get("request").user.id
        return Subscription.objects.filter(
            author=obj.id, user=user_id
        ).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """При создании пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class SubscriptionSerializer(CustomUserSerializer, PageNumberPagination):
    """Подписка."""

    email = serializers.ReadOnlyField(source="author.email")
    id = serializers.ReadOnlyField(source="author.id")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source="author.recipes.count")
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes_count(self, obj):
        """Количество рецептов автора."""
        return Recipe.objects.filter(author=obj.id).count()

    def get_recipes(self, obj):
        author_recipes = obj.author.recipes.all()

        if author_recipes:
            serializer = ShortRecipeSerializer(
                author_recipes,
                context={"request": self.context.get("request")},
                many=True,
            )
            return serializer.data

        return []

    def validate(self, data):
        user = self.context["request"].user
        author = data.get("author")

        if user == author:
            raise serializers.ValidationError(
                "Нельзя подписаться или отписаться от себя!"
            )

        if Subscription.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                "Подписка уже оформлена!"
            )

        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    """Для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    unit_of_measurement = serializers.ReadOnlyField(
        source="ingredient.unit_of_measurement"
    )

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "name", "unit_of_measurement", "amount")


class CreateUpdateRecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(
        validators=[
            MinValueValidator(
                IngredientValidAmount.MIN_INGREDIENT_AMOUNT,
                message=("Количество ингредиентов не может быть меньше "
                         f"{IngredientValidAmount.MIN_INGREDIENT_AMOUNT}.")
            )
        ]
    )

    class Meta:
        model = Ingredient
        fields = ("id", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        serializer = RecipeIngredientsSerializer(ingredients, many=True)

        return serializer.data

    def get_is_favorited(self, obj):
        """Добавлен ли рецепт в избранное."""
        user_id = self.context.get("request").user.id
        return Favorite.objects.filter(user=user_id, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """Добавлен ли рецепт в список покупок."""
        user_id = self.context.get("request").user.id
        return ShoppingCart.objects.filter(
            user=user_id, recipe=obj.id
        ).exists()

    class Meta:
        model = Recipe
        exclude = ("pub_date",)


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = CreateUpdateRecipeIngredientsSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=[
            MinValueValidator(
                RecipeValidTime.MIN_COOKING_TIME,
                message=("Время приготовления не может быть меньше"
                         f"{RecipeValidTime.MIN_COOKING_TIME}!")
            ),
            MaxValueValidator(
                RecipeValidTime.MAX_COOKING_TIME,
                message=("Время приготовления не может быть больше"
                         f"{RecipeValidTime.MAX_COOKING_TIME}!")
            )
        ]
    )

    def validate_tags(self, value):
        if not value:
            raise exceptions.ValidationError("Добавьте хотя бы один тег!")

        return value

    def validate_ingredients(self, value):
        if not value:
            raise exceptions.ValidationError(
                "Добавьте хотя бы один ингредиент!"
            )

        ingredients = [item["id"] for item in value]
        for ingredient in ingredients:
            if ingredients.count(ingredient) > 1:
                raise exceptions.ValidationError(
                    "Рецепт не может включать два одинаковых ингредиента!"
                )

        return value

    def create(self, validated_data):
        ingredients_amounts = []
        author = self.context.get("request").user
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            amount = ingredient.get("amount")
            ingredient = get_object_or_404(
                Ingredient, pk=ingredient.get("id").id
            )
        ingredients_amounts.append(IngredientInRecipe(
            recipe=recipe, ingredient=ingredient, amount=amount))

        IngredientInRecipe.objects.bulk_create(ingredients_amounts)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags.set(tags)

        ingredients = validated_data.pop("ingredients", None)
        if ingredients is not None:
            instance.ingredients.clear()

            for ingredient in ingredients:
                amount = ingredient.get("amount")
                ingredient = get_object_or_404(
                    Ingredient, pk=ingredient.get("id").id
                )

                IngredientInRecipe.objects.update_or_create(
                    recipe=instance,
                    ingredient=ingredient,
                    defaults={"amount": amount},
                )

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance, context={"request": self.context.get("request")}
        )

        return serializer.data

    class Meta:
        model = Recipe
        exclude = ("pub_date",)


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
