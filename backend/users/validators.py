import re

from rest_framework.validators import ValidationError


def validate_username(value):
    """Проверка имени и возврат некорректных символов."""
    forbidden_characters = "".join(re.split(r"[\w]|[.]|[@]|[+]|[-]+$", value))

    if forbidden_characters:
        raise ValidationError(
            f"Введены недопустимые символы: {forbidden_characters}"
            f" Недопускаются: пробел(перенос строки и т.п.)"
            " и символы, кроме . @ + - _"
        )
