from currencies.clients.base_client import BaseClient


class PrivatBank(BaseClient):
    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    def prepared_data(self):
        """
        [{"ccy":"EUR","base_ccy":"UAH","buy":"40.13220","sale":"41.84100"},
        {"ccy":"USD","base_ccy":"UAH","buy":"36.56860","sale":"37.45318"}]
        :return: dict
        """
        self._request(
            'get',
            params={
                'json': '',
                'exchange': '',
                'coursid': 11
            }
        )
        results = []
        if self.response:
            for currency in self.response.json():
                results.append({
                    'ticker': currency['ccy'],
                    'buy': currency['buy'],
                    'sell': currency['sale']
                })
        return results


privatbank_client = PrivatBank()
