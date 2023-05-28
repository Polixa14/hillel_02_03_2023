from project.base_client import BaseClient
from bs4 import BeautifulSoup
import re
import logging

logger = logging.getLogger(__name__)


class MegasportClient(BaseClient):
    base_url = 'https://megasport.ua/ru/catalog/obuv/male/brands-nike/'

    def prepared_data(self):
        self._request('get',)
        products_list = []
        if self.response and self.response.status_code == 200:
            soup = BeautifulSoup(self.response.content, 'html.parser')
            category = soup.find('h2', class_='catalog-header').text
            for item in soup.find_all('div', class_='o_IeKu'):
                try:
                    products_list.append({
                        'image_url': item.find(
                            'img',
                            class_='kvmZAa lI3NFt'
                        ).get('src'),
                        'sku': re.search(
                            r'\d{3,}',
                            item.find('img', class_='kvmZAa lI3NFt').get('alt')
                        ).group(),
                        'name': re.sub(
                            r'[^\x00-\x7F]+',
                            ' ',
                            item.find('div', class_='NEP5vH').text
                        ),
                        'category': category,
                        'price': re.sub(
                            r'\D',
                            '',
                            item.find('span', class_='HwlSPP').text
                        )
                    })
                except Exception as err:
                    logger.error(err)
            return products_list

    def get_image(self, url):
        self._request('get', url=url)
        return self.response


megasport_client = MegasportClient()
