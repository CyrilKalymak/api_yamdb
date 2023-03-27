import datetime as dt
import re

from django.core.exceptions import ValidationError

PATTERN = r'[^\w.@+-]+'
SYMBOL_NAMES = {' ': 'пробел', ',': 'запятая', '/': 'слэш', '\\': 'бэк-слэш'}


def symbol_name(symbol):
    return SYMBOL_NAMES.get(symbol, symbol)


def username_validator(value):
    if value == 'me':
        raise ValidationError(
            'Для имени пользователя нельзя использовать «me»'
        )
    incorrect = list(set(''.join(re.findall(PATTERN, value))))
    if incorrect:
        raise ValidationError(
            (f'Символы {", ".join(map(symbol_name, incorrect))} '
             'нельзя использовать в имени')
        )
    return value


def spell_slug(value):
    re.fullmatch(r'^[-a-zA-Z0-9_]+$', value)
    if not re.fullmatch(r'^[-a-zA-Z0-9_]+$', value):
        raise ValidationError(
            'Проверьте правильноть написания слага.')
    if len(value) > 50:
        raise ValidationError(
              'Идентификатор не может быть длинее 50 символов.')
        return value


def title_year(value):
    if value < 0 or value > dt.datetime.now().year:
        raise ValidationError(
            'Проверьте год создания произведения.'
        )
    return value
