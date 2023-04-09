from django.shortcuts import render
from feedbacks.forms import FeedbackModelForm
from feedbacks.models import Feedback


def feedbacks(request, *args, **kwargs):
    feedbacks_list = Feedback.objects.iterator()
    form = FeedbackModelForm(user=request.user)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = FeedbackModelForm(data=request.POST, user=request.user)
            if form.is_valid():
                breakpoint()
                form.save()
        else:
            form.cleaned_data = {}
            form.add_error('text', 'Login to leave feedback')
    return render(request, 'feedbacks/index.html', context={
        'feedbacks': feedbacks_list,
        'form': form
    })
