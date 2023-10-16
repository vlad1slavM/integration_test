import requests
from models.price import PriceModel


def price_update_batch(items: list[PriceModel]):
    """
    Предназначен для загрузки состояния запасов на торговой точке
    :param items: Значения для записи (!до 1000 элементов)
    """


