from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class RegistrationModelForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        else:
            raise ValidationError('User with this e-mail already registered')

    def clean(self):
        if self.cleaned_data.get('email'):
            self.cleaned_data['username'] = \
                self.cleaned_data['email'].split('@')[0]
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = self.cleaned_data['username']
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user
