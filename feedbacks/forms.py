from django import forms
from django.utils.html import strip_tags
from feedbacks.models import Feedback


class FeedbackModelForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('user', 'text', 'rating')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if user:
            self.fields['user'].widget = forms.HiddenInput()
            self.fields['user'].initial = user
            self.fields['rating'].help_text = 'Choose rating'

    def clean_text(self):
        text = self.cleaned_data.get('text')
        return strip_tags(text)
