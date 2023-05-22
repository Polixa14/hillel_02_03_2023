from .settings import *  # noqa

CELERY_TASK_ALWAYS_EAGER = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

LANGUAGE_CODE = 'en'
MEDIA_ROOT = 'media_test'
