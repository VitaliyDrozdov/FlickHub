from django.core import validators
from django.utils import timezone

MIN_RATING = 1
MAX_RATING = 10


def year_validator(value):
    year = timezone.now().year
    if value > year:
        raise validators.ValidationError(
            f'Year must be lower than or equal to {year}'
        )


def rating_validator(value):
    if value < MIN_RATING or value > MAX_RATING:
        raise validators.ValidationError('Rating must be between 1 and 10')
