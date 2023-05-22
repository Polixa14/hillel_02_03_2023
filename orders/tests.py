import random
from datetime import timedelta

from django.urls import reverse
from decimal import Decimal
from django.utils import timezone
from payments.models import Discount
from project.model_choices import DiscountTypes


def test_cart(client, login_client, product_factory, faker):
    url = reverse('cart')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == \
           reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302
    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['order']
    assert not response.context['order'].order_items.exists()

    # adding to cart
    product = product_factory()
    response = client.post(
        reverse('add_to_cart'),
        data={'product': product.id},
        follow=True
    )
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('cart')
    assert response.redirect_chain[0][1] == 302
    response = client.get(url)
    order_item_1 = response.context['order'].order_items.first()
    assert order_item_1.product == product

    # updating quantity
    new_quantity = random.randint(1, 100)
    response = client.post(reverse('update_quantity'),
                           data={'quantity': new_quantity,
                                 'order_item': faker.uuid4()},
                           follow=True)

    assert response.context['form'].errors['order_item'][0] == \
           'Invalid Order Item ID'

    new_quantity = random.randint(1, 100)
    response = client.post(reverse('update_quantity'),
                           data={'quantity': new_quantity,
                                 'order_item': order_item_1.id},
                           follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('cart')
    assert response.redirect_chain[0][1] == 302
    assert response.context['order'].order_items.first().quantity == \
           new_quantity

    # apply discount
    code = faker.random_number(5)
    discount = Discount.objects.create(
        amount=11000,
        code=code
    )
    response = client.post(url, data={'discount': code}, follow=True)
    assert response.status_code == 200
    assert response.context['order'].total_price == \
           response.context['order'].total_price_with_discount

    amount = random.randint(10, 20)
    code = faker.random_number(5)
    discount = Discount.objects.create(
        amount=amount,
        code=code,
        valid_until=timezone.now() - timedelta(days=1)
    )
    response = client.post(url, data={'discount': code})
    assert response.status_code == 200
    assert response.context['form'].errors['discount'][0] == \
           'Discount expired'

    discount.valid_until = timezone.now() + timedelta(days=1)
    discount.save()
    response = client.post(url, data={'discount': faker.random_number(5)})
    assert response.status_code == 200
    assert response.context['form'].errors['discount'][0] == \
           'Invalid discount code'

    response = client.post(url, data={'discount': code}, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('cart')
    assert response.redirect_chain[0][1] == 302
    assert response.context['order'].total_price - discount.amount == \
           response.context['order'].total_price_with_discount

    code = faker.random_number(5)
    discount = Discount.objects.create(
        amount=amount,
        code=code,
        discount_type=DiscountTypes.PERCENT
    )
    response = client.post(url, data={'discount': code}, follow=True)
    price_with_discount = (response.context['order'].total_price -
                           response.context['order'].total_price *
                           discount.amount / 100).quantize(Decimal('1.00'))
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('cart')
    assert response.redirect_chain[0][1] == 302
    assert price_with_discount == \
           response.context['order'].total_price_with_discount

    # test deleting an order_item
    response = client.post(
        reverse(
            'delete_item',
            kwargs={'pk': response.context['order'].order_items.first().id}),
        data={'discount': code},
        follow=True
    )
    assert not response.context['order'].order_items.all()
