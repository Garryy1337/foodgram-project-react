from django.contrib import admin

from recipes.models import Ingredient, Recipe


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeTagsInLine(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "text", "pub_date", "author")
    search_fields = ("name", "author")
    inlines = (RecipeIngredientsInLine, RecipeTagsInLine)
    empty_value_display = "-пусто-"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "unit_of_measurement")
    search_fields = ("name",)
    empty_value_display = "-пусто-"
