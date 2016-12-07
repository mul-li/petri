import string

from werkzeug.routing import BaseConverter, ValidationError

numerals = string.digits + string.ascii_lowercase


def base36(n):
    d, m = divmod(n, 36)
    return base36(d) + numerals[m] if d > 0 else numerals[m]


class Base36Converter(BaseConverter):

    def __init__(self, map):
        super().__init__(map)

    def to_python(self, value):
        try:
            return int(value, base=36)
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        return base36(value)
