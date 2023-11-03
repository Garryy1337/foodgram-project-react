from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
)
from api.views import CustomUserViewSet

app_name = "api"
router = DefaultRouter()
router.register("ingredients", IngredientViewSet)
router.register("recipes", RecipeViewSet)
router.register("tags", TagViewSet)
router.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
