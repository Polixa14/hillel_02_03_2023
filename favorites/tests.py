from django.urls import reverse
from favorites.models import FavoriteProduct


def test_favorites(client, login_client, product_factory):
    url = reverse('favorite')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == \
           reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302
    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200
    assert not response.context['favorite_products']
    for _ in range(3):
        FavoriteProduct.objects.get_or_create(
            user=user,
            product=product_factory(),
        )
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['favorite_products'].count() == \
           FavoriteProduct.objects.filter(user=user).count()


def test_adding_to_favorites(client, login_client, product_factory, faker):
    # add product to favorites
    product = product_factory()
    client, user = login_client()
    a = '1234'
    response = client.post(
        reverse('add_to_favorite', kwargs={'slug': product.slug}),
        data={'product': a},
        follow=True
    )
    assert response.status_code == 200
    assert FavoriteProduct.objects.count() == 0
    response = client.post(
        reverse('add_to_favorite', kwargs={'slug': product.slug}),
        data={'product': product.id},
        follow=True
    )
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == \
           reverse('details', kwargs={'slug': product.slug})
    assert response.redirect_chain[0][1] == 302

    # check if product in favorites
    response = client.get(reverse('favorite'))
    assert response.status_code == 200
    assert response.context['favorite_products'].first() == \
           FavoriteProduct.objects.get(user=user, product=product)

    # delete from favorites
    response = client.post(
        reverse('add_to_favorite', kwargs={'slug': product.slug}),
        data={'product': product.id},
        follow=True
    )
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == \
           reverse('details', kwargs={'slug': product.slug})
    assert response.redirect_chain[0][1] == 302

    # check if product in favorites
    response = client.get(reverse('favorite'))
    assert response.status_code == 200
    assert not response.context['favorite_products']
