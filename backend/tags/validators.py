import re

from rest_framework.validators import ValidationError


def validate_color(value):
    """Валидация HEX-значения цвета."""
    match = re.search(r"^#[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}", value)
    if not match:
        raise ValidationError(
            "Проверьте, что ввели корректное значение HEX-цвета"
        )
