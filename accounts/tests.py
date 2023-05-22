import re

from django.contrib.auth import get_user_model
from django.urls import reverse


def test_email_login(client, faker):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(errors == ['This field is required.']
               for errors in response.context['form'].errors.values())

    data['username'] = faker.email()
    data['password'] = faker.word()
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][0] == \
           'Please enter a correct email address and password. ' \
           'Note that both fields may be case-sensitive.'

    user, _ = get_user_model().objects.get_or_create(email=data['username'])
    user.set_password(data['password'])
    user.save()
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert response.url == reverse('main')


def test_phone_login(client, faker):
    url = reverse('login')
    data = {
        'username': faker.phone_number().split('x')[0],
        'password': faker.word()
    }
    user, _ = get_user_model().objects.get_or_create(
        phone_number=data['username']
    )
    user.set_password(data['password'])
    user.save()
    response = client.post(url, data=data)
    # User`s is_phone_number_valid = False
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][0] == \
           'Please enter a correct email address and password. ' \
           'Note that both fields may be case-sensitive.'

    user.is_phone_number_valid = True
    user.save()
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert response.url == reverse('main')


def test_registration(client, faker):
    url = reverse('registration')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(errors == ['This field is required.']
               for errors in response.context['form'].errors.values())

    password = faker.random_number(digits=7)
    data['email'] = faker.email()
    data['password1'] = password
    data['password2'] = password
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['password2'] == [
        'This password is too short. It must contain at least 8 characters.',
        'This password is entirely numeric.'
    ]

    password = data['email'].split('@')[0]
    data['password1'] = password
    data['password2'] = password
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['password2'][0] == \
           'The password is too similar to the email address.'

    data['password1'] = faker.password()
    data['password2'] = faker.password()
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['password2'][0] == \
           'The two password fields didn’t match.'

    user, _ = get_user_model().objects.get_or_create(email=data['email'])
    data['password2'] = data['password1']
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['email'][0] == \
           'User with this e-mail already registered'

    user.delete()
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert response.url == reverse('main')


def test_profile_edit(client, faker, login_client):
    url = reverse('edit_profile')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == \
           reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302

    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200

    first_name = faker.first_name()
    last_name = faker.last_name()

    data = {
        'first_name': first_name,
        'last_name': last_name,
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['phone_number'][0] == \
           'Phone number field must not be empy'

    data = {
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': faker.random_number(25)
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['phone_number'][0] == \
           'Invalid phone number'

    phone_number = faker.phone_number().split('x')[0]

    data = {
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert response.url == reverse('phone_validation')

    user.refresh_from_db()
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.phone_number == re.sub(r'[-.\s+()]', '', phone_number)
