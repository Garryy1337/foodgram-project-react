import re

from rest_framework.validators import ValidationError


def validate_username(value):
    """Проверка имени и возврат не корректных символов."""
    forbidden_characters = "".join(re.split(r"[\w]|[.]|[@]|[+]|[-]+$", value))

    if len(forbidden_characters) != 0:
        raise ValidationError(
            f"Введены не допустимые символы: {forbidden_characters}"
            f"Не допускаются: пробел(перенос строки и т.п.)"
            " и символы, кроме . @ + - _"
        )
