import requests
from models.inventory import InventoryModel
from models.price import PriceModel
import random
from settings.logger import logger


def inventory_update_batch(items: list[InventoryModel], api_key: str):
    """
    Предназначен для загрузки состояния запасов на торговой точке
    :param items: Значения для записи (!до 1000 элементов)
    :param api_key: Token
    """
    url = f'https://api.heado.ru/management/{api_key}'
    data = {
        'id': random.randint(1000, 100000),
        'method': 'inventoryUpdateBatch',
        'params': {
            'items': items
        },
        'jsonrpc': "2.0"
    }
    r = requests.post(url, json=data)
    if r.status_code != 200:
        logger.exception(f"exception in method inventory_update_batch "
                         f"{r.status_code = }, {r.text = }")


def price_update_batch(items: list[PriceModel], api_key: str):
    """
    Предназначен для загрузки состояния запасов на торговой точке
    :param items: Значения для записи (!до 1000 элементов)
    :param api_key: Token
    """
    url = f'https://api.heado.ru/management/{api_key}'
    data = {
        'id': random.randint(1000, 100000),
        'method': 'price.updateBatch',
        'params': {
            'items': items
        },
        'jsonrpc': "2.0"
    }
    r = requests.post(url, json=data)
    if r.status_code != 200:
        logger.exception(f"exception in method price_update_batch "
                         f"{r.status_code = }, {r.text = }")
