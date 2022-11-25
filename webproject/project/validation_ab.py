import re
from datetime import datetime
items_ab = ['Sort by ascending date', 'Sort by descending date', 'Sort alphabetically']


class DateIsNotValid(Exception):
    """You cannot add an invalid date"""


class DateVeryBig(Exception):
    """This date bigger than present year"""


class EmptyName(Exception):
    pass


class Field:
    def __init__(self, value: str) -> None:
        self.__value = None
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        def is_code_valid(phone_code: str) -> bool:
            if phone_code[:2] in ('03', '04', '05', '06', '09') and phone_code != '039':
                return True
            return False

        result = None
        phone = value.removeprefix('+').replace('(', '').replace(')', '').replace('-', '')
        if phone.isdigit():
            if phone.startswith('0') and len(phone) == 10 and is_code_valid(phone[:3]):
                result = '+38' + phone
            if phone.startswith('380') and len(phone) == 12 and is_code_valid(phone[2:5]):
                result = '+' + phone
            if 10 <= len(phone) <= 14 and not phone.startswith('0') and not phone.startswith('380'):
                result = '+' + phone
        if result is None:
            raise ValueError(f'Неправильний тип значення {value}')
        self.__value = result


class Birthday(Field):
    def __str__(self):
        if self.value is None:
            return '-'
        else:
            return f'{self.value:%Y-%m-%d}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value is None:
            self.__value = None
        else:
            try:
                self.__value = datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise DateIsNotValid


class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value is None:
            self.__value = None
        else:
            result = None
            get_emails = re.findall(r'\b[a-zA-Z][\w\.]+@[a-zA-Z]+\.[a-zA-Z]{2,}', value)
            if get_emails:
                for i in get_emails:
                    result = i
            if result is None:
                raise AttributeError(f"Неправильний тип значення {value}")
            self.__value = result


