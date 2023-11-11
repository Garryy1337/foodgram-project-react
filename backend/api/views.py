from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly,)
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.permissions import IsAdminAuthorOrReadOnly
from api.serializers import (
    IngredientSerializer,
    RecipeCreateUpdateSerializer,
    RecipeSerializer,
    ShortRecipeSerializer,
    SubscriptionSerializer,
    TagSerializer,)
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Subscription, User


class CustomUserViewSet(UserViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        """Список авторов, на которых подписан пользователь."""
        user = self.request.user
        queryset = user.followers.exclude(id=user.id)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=("post",),
    )
    def subscribe(self, request, id=None):
        """Подписка на автора."""
        user = self.request.user
        author = get_object_or_404(User, pk=id)

        if self.request.method == "POST":
            if Subscription.objects.filter(user=user, author=author).exists():
                return Response(
                    {"errors": "Подписка уже оформлена!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            queryset = Subscription.objects.create(author=author, user=user)
            serializer = SubscriptionSerializer(
                queryset, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None): 
        """Отписка от автора.""" 
        user = self.request.user 
        author = get_object_or_404(User, pk=id) 
 
        try:
            subscription = Subscription.objects.get(user=user, author=author)
        except Subscription.DoesNotExist:
            return Response( 
                {"errors": "Вы уже отписаны!"}, 
                status=status.HTTP_400_BAD_REQUEST, 
            ) 
 
        subscription.delete() 
 
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ("create", "partial_update"):
            return RecipeCreateUpdateSerializer

        return RecipeSerializer

    def add(self, model, user, pk, name):
        """Добавление рецепта."""
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = model.objects.filter(user=user, recipe=recipe)
        if relation.exists():
            return Response(
                {"errors": f"Нельзя повторно добавить рецепт в {name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_relation(self, model, user, pk, name):
        """ "Удаление рецепта из списка пользователя."""
        recipe = get_object_or_404(Recipe, pk=pk)
        relation = model.objects.filter(user=user, recipe=recipe)
        if not relation.exists():
            return Response(
                {"errors": f"Нельзя повторно удалить рецепт из {name}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action( 
        detail=True, 
        methods=("post",), 
        url_path="favorite", 
        url_name="favorite", 
    ) 
    def favorite(self, request, pk=None): 
        """Добавление рецепта в избранное.""" 
        user = request.user 
        name = "избранное"

        if request.method == "POST": 
            return self.add(Favorite, user, pk, name) 

    @favorite.mapping.delete
    def unfavorite(self, request, pk=None): 
        """Удаление рецепта из избранного.""" 
        user = request.user 
        name = "избранного"

        return self.delete_relation(Favorite, user, pk, name)

    @action( 
        detail=True, 
        methods=("post",), 
        url_path="shopping_cart", 
        url_name="shopping_cart", 
    ) 
    def shopping_cart(self, request, pk=None): 
        """Добавление рецепта в список покупок.""" 
        user = request.user 
        name = "список покупок"

        if request.method == "POST": 
            return self.add(ShoppingCart, user, pk, name) 

    @shopping_cart.mapping.delete
    def remove_from_cart(self, request, pk=None): 
        """Удаление рецепта из списка покупок.""" 
        user = request.user 
        name = "списка покупок"

        return self.delete_relation(ShoppingCart, user, pk, name)

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
        url_path="download_shopping_cart",
        url_name="download_shopping_cart",
    )
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in shopping_cart]
        buy = (
            IngredientInRecipe.objects.filter(recipe__in=recipes)
            .values("ingredient")
            .annotate(amount=Sum("amount"))
            .order_by("ingredient__name")
        )

        purchased = [
            "Список покупок:",
        ]
        for item in buy:
            ingredient = Ingredient.objects.get(pk=item["ingredient"])
            amount = item["amount"]
            purchased.append(
                f"{ingredient.name}: {amount}, "
                f"{ingredient.measurement_unit}"
            )
        purchased_in_file = "\n".join(purchased)

        response = HttpResponse(purchased_in_file, content_type="text/plain")
        response[
            "Content-Disposition"
        ] = "attachment; filename=shopping-list.txt"

        return response
