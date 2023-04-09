from django.contrib.auth import login
from django.views.generic import FormView
from accounts.model_forms import RegistrationModelForm
from project import settings


class RegistrationView(FormView):
    form_class = RegistrationModelForm
    template_name = 'registration/singup.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)