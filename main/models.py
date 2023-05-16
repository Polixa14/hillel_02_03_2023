from project.mixins.models import SingletonMixin
from django.db import models


class EmailConfig(SingletonMixin):
    contact_form_email = models.EmailField(max_length=255)

    def __str__(self):
        return self.contact_form_email
