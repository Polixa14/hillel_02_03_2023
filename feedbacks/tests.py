from django.urls import reverse
import random
from feedbacks.models import Feedback


def test_feedbacks(client, login_client, faker):
    url = reverse('feedbacks')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert not response.context.get('form')
    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context.get('form')

    feedback = faker.word()
    rating = random.randint(1, 5)
    data = {
        'user': user.id,
        'text': feedback,
        'rating': rating
    }
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == url
    assert response.redirect_chain[0][1] == 302
    assert Feedback.objects.filter(
        user=user,
        text=feedback,
        rating=rating
    ).exists()
