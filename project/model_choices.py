from django.db.models import IntegerChoices


class DiscountTypes(IntegerChoices):
    VALUE = 0, 'VALUE'
    PERCENT = 1, 'PERCENT'
