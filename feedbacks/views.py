from django.urls import reverse_lazy
from feedbacks.forms import FeedbackModelForm
from feedbacks.models import Feedback
from django.views.generic import FormView
from django.core.cache import cache


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
        feedbacks = cache.get('feedbacks')
        if not feedbacks:
            feedbacks = Feedback.objects.all()
            cache.set('feedbacks', feedbacks)
        context['feedbacks'] = feedbacks
        if not self.request.user.is_authenticated:
            context.pop('form')
        return context
