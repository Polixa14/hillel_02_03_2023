import factory
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from pytest_factoryboy import register
from products.models import Product, Category
from project.constants import DECIMAL_PLACES
import os

fake = Faker()


@pytest.fixture(autouse=True)
def django_db_setup(db):
    import shutil
    from django.conf import settings
    yield
    if os.path.exists(settings.BASE_DIR / settings.MEDIA_ROOT):
        shutil.rmtree(settings.BASE_DIR / settings.MEDIA_ROOT)


@pytest.fixture(scope='session')
def faker_fixture():
    yield fake


@register
class UserFactory(factory.django.DjangoModelFactory):

    email = factory.LazyAttribute(lambda x: fake.email())
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    last_name = factory.LazyAttribute(lambda x: fake.last_name())
    phone_number = factory.LazyAttribute(
        lambda x: fake.random_number(digits=11)
    )
    is_phone_number_valid = True

    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)


@register
class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda x: fake.word())

    class Meta:
        model = Category
        django_get_or_create = ('name',)


@register
class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda x: fake.word())
    description = factory.LazyAttribute(lambda x: fake.word())
    sku = factory.LazyAttribute(lambda x: fake.random_number(digits=10))
    image = factory.django.ImageField()
    price = factory.LazyAttribute(lambda x: fake.pydecimal(
        min_value=30,
        left_digits=DECIMAL_PLACES,
        right_digits=DECIMAL_PLACES,
    ))

    class Meta:
        model = Product
        django_get_or_create = ('name', 'sku')

    @factory.post_generation
    def post(self, create, extracted, **kwargs):
        self.category.add(CategoryFactory())


@pytest.fixture(scope='function')
def login_client(db, client):

    def login_user(user=None, **kwargs):
        if user is None:
            user = UserFactory()
        password = '12345678'
        user.set_password(password)
        user.save()
        data = {'username': user.email,
                'password': password}
        response = client.post(reverse('login'), data=data)
        assert response.status_code == 302
        return client, user

    return login_user
