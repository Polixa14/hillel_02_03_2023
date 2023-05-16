from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from main.forms import ContactForm
from main.tasks import send_mail_from_contact_form


class MainView(TemplateView):
    template_name = 'main/index.html'


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'main/contacts.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        send_mail_from_contact_form.delay(
            form.cleaned_data.get('email'),
            form.cleaned_data.get('text'),
            form.cleaned_data.get('subject'),
        )
        return super().form_valid(form)
