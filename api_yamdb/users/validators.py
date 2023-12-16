import re
from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            'Использование имени "me" в качестве username запрещено.'
        )
    regex = re.compile(r'^[\w.@+-]+\Z')
    if not regex.match(value):
        raise ValidationError(
            'Неверное значение username. '
            'Допустимы только буквы, цифры, символы ".", "@", "+" и "-".'
        )
    return value
