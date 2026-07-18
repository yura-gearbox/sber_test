import requests
from typing import TypeVar

T = TypeVar('T', int, float, str)


class ApiClient:
    def __init__(self, base_url: str, timeout: int = 5, headers: dict[str, str] | None = None) -> None:
        self._session = requests.Session()
        self._session.headers.update(headers)
        self._base_url = base_url
        self._timeout = timeout

    def close(self) -> None:
        self._session.close()

    def get(self, endpoint: str, validate: bool = True, timeout: int | None = None, **kwargs) -> requests.Response:
        if timeout is None:
            timeout = self._timeout

        response = self._session.get(
            f'{self._base_url}{endpoint}',
            timeout=timeout,
            **kwargs)
        # стандартная проверка status и Content-Type
        if validate:
            check_status(response.status_code, 200)
            check_content_type(
                response.headers['Content-Type'], 'application/json')

        return response

    def post(self, endpoint: str, validate: bool = True, timeout: int | None = None, **kwargs) -> requests.Response:
        if timeout is None:
            timeout = self._timeout

        response = self._session.post(
            f'{self._base_url}{endpoint}',
            timeout=timeout,
            **kwargs)
        # стандартная проверка status и Content-Type
        if validate:
            check_status(response.status_code, 200)
            check_content_type(
                response.headers['Content-Type'], 'application/json')

        return response


def check_status(actual_status: int, expected_status: int = 200) -> None:
    should_be_equal(actual_status, expected_status,
                    err_msg=f'Ожидался статус-код {expected_status}, но получен {actual_status}')


def check_content_type(actual_content_type: str, expected_content_type: str = 'application/json') -> None:
    should_be_equal(actual_content_type, expected_content_type,
                    err_msg=f'Ожидался Content-Type {expected_content_type}, но получен {actual_content_type}')


def check_status_in_list(actual_status: int, statuses_list: list[int]) -> None:
    should_be_in_list(actual_status, statuses_list,
                      err_msg=f'Актуальный статус {actual_status} отсутствует в списке ожидаемых статусов {statuses_list}')


def check_value_is_equal(actual_value: T, expected_value: T, name_value: str) -> None:
    should_be_equal(actual_value, expected_value,
                    err_msg=f'Значение {name_value} ожидалось {expected_value}, но получено {actual_value}')


def check_value_is_empty(actual_value: T, name_value: str) -> None:
    should_be_empty(actual_value,
                    err_msg=f'Значение {name_value} ожидалось пустым, но получено {actual_value}')


def check_value_is_none(actual_value: T, name_value: str) -> None:
    should_be_none(actual_value,
                   err_msg=f'Значение {name_value} ожидалось None, но получено {actual_value}')


def should_be_equal(actual_value: T, expected_value: T, err_msg: str | None = None) -> None:
    assert actual_value == expected_value, err_msg


def should_be_in_list(actual_value: T, values_list: list[T], err_msg: str) -> None:
    assert actual_value in values_list, err_msg


def should_be_empty(actual_value: T, err_msg: str) -> None:
    assert not actual_value, err_msg


def should_be_none(actual_value: T, err_msg: str) -> None:
    assert actual_value is None, err_msg
