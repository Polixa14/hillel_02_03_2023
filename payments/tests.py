from django.urls import reverse


def test_payment(client, login_client):
    client, user = login_client()
    response = client.get(reverse('cart'))
    current_order = response.context['order']
    assert response.status_code == 200
    assert current_order

    response = client.post(reverse('payment'), follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('main')
    assert response.redirect_chain[0][1] == 302
    current_order.refresh_from_db()
    assert not current_order.is_active
    assert current_order.is_paid
