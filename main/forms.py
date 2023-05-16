from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)
