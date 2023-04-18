from django.urls import path
from feedbacks.views import FeedBacksView

urlpatterns = [
    path('', FeedBacksView.as_view(), name='feedbacks')
]
