from pathlib import Path
from settings.logger import logger
from models import price


def parse(file_dir: Path) -> [price.PriceModel]:
    """
    PriceRunner
    :param file_dir: Имя директории
    :return: список объектов типа PriceModel
    """
    prices = []
    Price = price.PriceModel
    with open(file_dir, 'r') as file:
        for line in file:
            name = price.Regulars.match_name(line)
            categories = price.Regulars.match_categories(line)
            product_price = price.Regulars.match_price(line)
            price_ext_id = price.Regulars.match_price_ext_id(line)
            vat = price.Regulars.match_vat(line)
            unit_type = price.Regulars.match_unit_type(line)
            unit_ratio = price.Regulars.match_unit_ration(line)
            if not name:
                logger.warning(f"Не передан обязательный параметр. "
                               f"В PriceRunner {name}")
                continue

            if not price_ext_id:
                logger.warning(f"Не передан обязательный параметр. "
                               f"В PriceRunner {price_ext_id}")
                continue

            prices.append(Price(name=name, categories=categories,
                                price=product_price, price_ext_id=price_ext_id,
                                vat=vat, unit_type=unit_type,
                                unit_ratio=unit_ratio))

    return prices
