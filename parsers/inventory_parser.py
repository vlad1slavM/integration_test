from datetime import datetime
from pathlib import Path
from typing import Union

from models.inventory import InventoryModel
from settings.logger import logger


def is_float(number: str) -> Union[float, None]:
    try:
        float(str(number))
        return True
    except ValueError:
        return False


def get_date_format(date_str: str) -> Union[datetime, None]:
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        except ValueError:
            logger.warning(f'Invalid date format: {date_str = }')
            return None
    except TypeError:
        logger.warning('No date provided')
        return None


def parse(file_dir: Path) -> [InventoryModel]:
    """
    InventoryRunner
    :param file_dir: Имя директории
    :return: список объектов типа PriceModel
    """

    with (open(file_dir, 'r') as file):
        answer = []
        for line in file:
            items = line.split(',')
            if len(items) != 10:
                while len(items) != 10:
                    items.append(None)

            store_ext_id = items[0]
            price_ext_id = items[1]
            snap_datetime = get_date_format(items[2])
            in_matrix = items[3]
            in_matrix = bool(in_matrix) if str(in_matrix).lower() in {'true',
                                                                      'false',
                                                                      '1',
                                                                      '0'} else None
            qty = float(items[4]) if is_float(items[4]) else None
            sell_price = float(items[5]) if is_float(items[5]) else None
            prime_cost = float(items[6]) if is_float(items[6]) else None
            min_stock_level = float(items[7]) if is_float(items[7]) else None
            stock_in_days = int(items[8]) if str(items[8]).isdigit() else None
            in_transit = float(items[9]) if is_float(items[9]) else None
            if not store_ext_id:
                logger.warning(f'Не передан обязательный параметр. '
                               f'{store_ext_id = }')
                continue

            if not price_ext_id:
                logger.warning(f'Не передан обязательный параметр. '
                               f'{price_ext_id = }')
                continue

            if not snap_datetime:
                logger.warning(f'Не передан обязательный параметр. '
                               f'{snap_datetime = }')
                continue

            if qty is None:
                logger.warning(f'Не передан обязательный параметр. '
                               f'{qty = }')
                continue

            answer.append(InventoryModel(
                store_ext_id=store_ext_id, price_ext_id=price_ext_id,
                snap_datetime=snap_datetime, in_matrix=in_matrix,
                qty=qty, sell_price=sell_price, prime_cost=prime_cost,
                min_stock_level=min_stock_level,
                stock_in_days=stock_in_days, in_transit=in_transit))
    return answer
