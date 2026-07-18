"""
1. Реализуйте функцию def str_to_int(str):
Функция принимает строку и возвращает тип int
In: "275295"
Out: 275295
Требования: Прямые преобразования (cast) из одного типа данных в
другой, а также использование массивов запрещены.
Подсказка: Используйте ASCII table
"""

import re
from functools import reduce
import pytest

pytestmark = pytest.mark.str_to_int

def str_to_int(number: str) -> int:
    if re.fullmatch(r'[-+]?\d+', number) is None:
        raise ValueError(f'Строка "{number}" пустая или содержит нечисловые символы')

    result = 0
    sign = 1
    if number.startswith(('-', '+')):
        if number.startswith('-'):
            sign = -1
        number = number[1:]

    result = reduce(lambda a, b: a * 10 + ord(b) - ord('0'), number, 0)

    return result * sign

@pytest.mark.parametrize('str_number, int_number', [('123', 123), ('0', 0), ('-1', -1), ('+1', 1)])
def test_str_to_int_success(str_number, int_number):
    assert str_to_int(str_number) == int_number

@pytest.mark.parametrize('number', ['', '-', '1.25', '10a'])
def test_str_to_int_except(number):
    with pytest.raises(ValueError) as except_info:
        str_to_int(number)

    assert except_info.type is ValueError
    assert str(except_info.value) == f'Строка "{number}" пустая или содержит нечисловые символы'
