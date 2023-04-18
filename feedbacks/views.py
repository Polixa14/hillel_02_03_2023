from django.urls import reverse_lazy
from feedbacks.forms import FeedbackModelForm
from feedbacks.models import Feedback
from django.views.generic import FormView


class FeedBacksView(FormView):
    template_name = 'feedbacks/index.html'
    form_class = FeedbackModelForm
    success_url = reverse_lazy('feedbacks')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedbacks'] = Feedback.objects.all()[:5]
        if not self.request.user.is_authenticated:
            context.pop('form')
        return context
