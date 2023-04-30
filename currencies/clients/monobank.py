from currencies.clients.base_client import BaseClient


class MonoBank(BaseClient):
    base_url = 'https://api.monobank.ua/bank/currency'

    def prepared_data(self):
        """
        [{"currencyCodeA":840,"currencyCodeB":980,"date":1682805674,"rateBuy":36.65,"rateCross":0,"rateSell":37.4406},
        {"currencyCodeA":978,"currencyCodeB":980,"date":1682805674,"rateBuy":40.3,"rateCross":0,"rateSell":41.5007},
        ...100 more...,
        {"currencyCodeA":978,"currencyCodeB":840,"date":1682805674,"rateBuy":1.094,"rateCross":0,"rateSell":1.107}]
        :return: dict
        """
        self._request('get')
        results = []
        if self.response:
            for currency in self.response.json():
                if currency['currencyCodeA'] in (840, 978) and \
                        currency['currencyCodeB'] == 980:
                    results.append({
                        'ticker': ('USD' if currency['currencyCodeA'] == 840
                                   else 'EUR'),
                        'buy': currency['rateBuy'],
                        'sell': currency['rateSell']
                    })
        return results


monobank_client = MonoBank()
