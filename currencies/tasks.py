from celery import shared_task
from currencies.clients.monobank import monobank_client
from currencies.clients.privatbank import privatbank_client
from currencies.models import CurrencyHistory
from project.celery import app
from django.utils import timezone
from datetime import timedelta


@shared_task
def get_currencies_task():
    currencies_data = privatbank_client.prepared_data() \
                 or monobank_client.prepared_data()
    save_currencies_task.delay(currencies_data)
    delete_old_currencies.delay()


@app.task
def save_currencies_task(data):
    currencies = []
    for currency in data:
        currencies.append(
            CurrencyHistory(
                **currency
            )
        )
    if currencies:
        CurrencyHistory.objects.bulk_create(currencies)


@app.task
def delete_old_currencies():
    CurrencyHistory.objects.filter(
        created_at__lt=timezone.now() - timedelta(days=7)
    ).delete()
