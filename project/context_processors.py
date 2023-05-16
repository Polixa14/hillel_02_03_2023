from django.core.cache import cache

from products.models import Category


def slug_categories(request) -> dict:
    categories = cache.get('categories')
    breakpoint()
    if not categories:
        categories = Category.objects.values('slug', 'name')
        cache.set('categories', categories)
    return {'categories': categories}
