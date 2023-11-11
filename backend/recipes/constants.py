class TagFieldLength:
    NAME_MAX_LENGTH = 200
    COLOR_MAX_LENGTH = 7
    SLUG_MAX_LENGTH = 200


class IngredientFieldLength:
    NAME_MAX_LENGTH = 80
    MEASUREMENT_UNIT = 15


class RecipeValidTime:
    MIN_COOKING_TIME = 1
    MAX_COOKING_TIME = 9999


class IngredientValidAmount:
    MIN_AMOUNT = 1
    MAX_AMOUNT = 50
    MIN_INGREDIENT_AMOUNT = 1
