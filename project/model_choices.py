from django.db.models import IntegerChoices


class DiscountTypes(IntegerChoices):
    VALUE = 0, 'VALUE'
    PERCENT = 1, 'PERCENT'


class Rating(IntegerChoices):
    ONE_STAR = 1, '1 stars'
    TWO_STARS = 2, '2 stars'
    THREE_STARS = 3, '3 stars'
    FOUR_STARS = 4, '4 stars'
    FIVE_STARS = 5, '5 stars'
