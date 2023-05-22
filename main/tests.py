from django.urls import reverse


def test_main(client):
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 200


def test_contact(client, faker):
    url = reverse('contact')
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'email': faker.email(),
        'subject': faker.word(),
        'text': faker.sentence()
    }
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('main')
    assert response.redirect_chain[0][1] == 302
