import re
from typing import Union

from pydantic import BaseModel

from settings.logger import logger


class PriceModel(BaseModel):
    """Модель для PriceRunner"""
    name: str
    categories: Union[str, None]
    price: Union[float, None]
    price_ext_id: str
    vat: Union[float, None]
    unit_type: Union[float, None]
    unit_ratio: Union[float, None]


class Regulars:
    """
    Класс, в котором содержаться регулярные выражения
    и методы для поиска по ним
    """

    name_reg = re.compile(r'^(.+?)(,\"|,[А-Я])')
    categories_reg = re.compile(
        r'(?:,[А-Я]|,"[А-Я])([^.а-я].+?),\d+(?:\.\d+)?(?:,|$)')

    price_reg = re.compile(r',([\d.,]+)$')

    @classmethod
    def match_name(cls, data: str) -> str:
        """
        Получить название продукта
        :param data: Строчка из файла
        :return: Название продукта
        """
        match = re.search(cls.name_reg, data)
        if match:
            return match.group(1)
        logger.warning(f'Can not find name with line {data}')
        return None

    @classmethod
    def match_categories(cls, data: str) -> str:
        """"""
        match = re.search(cls.categories_reg, data)
        if match:
            matched_str = match.group(0)
            if matched_str[1] == '"':
                return matched_str[2:matched_str.find(',', 2)]
            return matched_str[1:matched_str.find(',', 2)]
        logger.warning(f'Can not find categories with line {data}')
        return None

    def _get_all_digits(self, data: str):
        """
        Получить все цифры в конце сообщения
        :param data: Строчка из файла
        :return: список чисел
        """
        match = re.search(self.price_reg, data)
        if match:
            return match.group(0)[1:].split(',')
        logger.warning(f'Can not find digits in line {data = }')
        return None

    @classmethod
    def match_price(cls, data: str) -> float:
        """
        Получить цену продукта
        :param data: Строчка из файла
        :return: цену продукта
        """
        digits = cls._get_all_digits(cls, data)
        if digits and len(digits) > 1:
            try:
                return float(digits[0])
            except:
                logger.warning(
                    f'Price не соответствует формату price = {digits[0]} '
                    f'{data = }')
        return None

    @classmethod
    def match_price_ext_id(cls, data: str) -> int:
        """
        Получить ID продукта
        :param data: Строчка из файла
        :return: ID продукта
        """
        digits = cls._get_all_digits(cls, data)
        if digits:
            if len(digits) > 1:
                return digits[1]
            elif len(digits) == 1:
                return digits[0]

        logger.warning(f'Не передан обязательный параметр price_ext_id '
                       f'{data = }')
        return None

    @classmethod
    def match_vat(cls, data: str) -> float:
        """
        Получить ставку НДС продукта
        :param data: Строчка из файла
        :return: ставку НДС продукта
        """
        digits = cls._get_all_digits(cls, data)
        if digits:
            if len(digits) > 2:
                try:
                    return float(digits[2])
                except:
                    logger.warning(
                        f'vat не соответствует формату vat = {digits[2]}, '
                        f'{data = }')
        return None

    @classmethod
    def match_unit_type(cls, data: str) -> int:
        """
        Получить ставку НДС продукта
        :param data: Строчка из файла
        :return: ставку НДС продукта
        """
        digits = cls._get_all_digits(cls, data)
        if digits:
            if len(digits) > 3:
                try:
                    return int(digits[3])
                except:
                    logger.warning(
                        f'unit_type не соответствует формату '
                        f'unit_type = {digits[3]}, '
                        f'{data = }')
        return None

    @classmethod
    def match_unit_ration(cls, data: str) -> float:
        """
        Получить ставку НДС продукта
        :param data: Строчка из файла
        :return: ставку НДС продукта
        """
        digits = cls._get_all_digits(cls, data)
        if digits:
            if len(digits) > 4:
                try:
                    return float(digits[4])
                except:
                    logger.warning(
                        f'unit_ration не соответствует формату '
                        f' unit_ration = {digits[4]}, '
                        f'{data = }')
        return None
