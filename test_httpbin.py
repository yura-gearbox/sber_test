"""
Напишите автотесты, которые будут проверять статусы и ответы запросов к следующим сервисам.
1. http://httpbin.org/get
2. http://httpbin.org/post
3. http://httpbin.org/status/{codes} метод GET
4. http://httpbin.org/delay/{delay} метод GET
    Удостовериться, что запрос выполняется с задержкой, переданной в запросе. Тест должен быть параметризованный, параметры должны браться из json файла в корне проекта
5. http://httpbin.org/response-headers?freeform=
    Тест должен быть параметризованный, параметры должны браться из json файла в корне проекта
"""

import pytest
import requests
import json
import models
from data import BASE_URL, DEFAULT_TIMEOUT, ApiData


@pytest.fixture(scope='session')
def api_session():
    session = requests.Session()
    session.headers.update({'Accept': 'application/json'})
    yield session
    session.close()


@pytest.mark.parametrize(
    'params_dict',
    [
        ApiData.some_empty_dict,
        ApiData.some_dict
    ],
    ids=[
        'without_parameters',
        'with_single_parameter'
    ])
def test_get_request(api_session, params_dict):
    response = api_session.get(
        f'{BASE_URL}/get', params=params_dict, timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    assert 'application/json' in response.headers['Content-Type']
    response_model = models.GetResponse.model_validate(response.json())
    assert response_model.args == params_dict


@pytest.mark.parametrize(
    'payload',
    [
        ApiData.some_empty_dict,
        ApiData.some_dict
    ],
    ids=[
        'empty_payload',
        'filled_payload'
    ])
def test_post_request_by_json(api_session, payload):
    response = api_session.post(
        f'{BASE_URL}/post', json=payload, timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    assert 'application/json' in response.headers['Content-Type']
    response_model = models.PostResponseJson.model_validate(response.json())
    assert response_model.json_data == payload
    assert json.loads(response_model.data) == payload
    assert not response_model.args
    assert not response_model.files
    assert not response_model.form


@pytest.mark.parametrize(
    'form_payload',
    [
        ApiData.some_empty_dict,
        ApiData.some_dict
    ],
    ids=[
        'empty_form',
        'filled_form'
    ])
def test_post_request_by_form(api_session, form_payload):
    response = api_session.post(
        f'{BASE_URL}/post', data=form_payload, timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    assert 'application/json' in response.headers['Content-Type']
    response_model = models.PostResponseForm.model_validate(response.json())
    assert response_model.form == form_payload
    assert not response_model.args
    assert not response_model.data
    assert not response_model.files
    assert response_model.json_data is None


@pytest.mark.parametrize(
    'file_payload',
    [
        ApiData.some_empty_file,
        ApiData.some_files
    ],
    ids=[
        'empty_file',
        'non_empty_files'
    ])
def test_post_request_by_file(api_session, file_payload):
    response = api_session.post(
        f'{BASE_URL}/post', files=file_payload, timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    assert 'application/json' in response.headers[
        'Content-Type'], f'Actual is {response.headers["Content-Type"]}'

    expected_files_content = {}
    for key, value in file_payload.items():
        expected_files_content[key] = value[1]

    response_model = models.PostResponseFile.model_validate(response.json())
    assert response_model.files == expected_files_content
    assert not response_model.args
    assert not response_model.data
    assert not response_model.form
    assert response_model.json_data is None


@pytest.mark.parametrize('status', ApiData.some_status_codes)
def test_status_code_request(api_session, status):
    response = api_session.get(
        f'{BASE_URL}/status/{status}', timeout=DEFAULT_TIMEOUT, allow_redirects=False)
    assert response.status_code == status


def test_multiple_status_codes_request(api_session):
    endpoint = f'status/{",".join([str(item) for item in ApiData.some_multiple_status_codes])}'
    response_status_codes = set()
    for _ in range(10):
        response = api_session.get(
            f'{BASE_URL}/{endpoint}', timeout=DEFAULT_TIMEOUT, allow_redirects=False)
        assert response.status_code in ApiData.some_multiple_status_codes
        response_status_codes.add(response.status_code)
    assert len(response_status_codes) > 1


@pytest.mark.parametrize('delay', ApiData.some_delays)
def test_get_request_with_delay(api_session, delay):
    timeout = DEFAULT_TIMEOUT if DEFAULT_TIMEOUT > delay else delay + 1
    response = api_session.get(f'{BASE_URL}/delay/{delay}', timeout=timeout)
    assert response.status_code == 200
    assert 'application/json' in response.headers['Content-Type']
    assert delay <= response.elapsed.total_seconds() < delay + 1
    response_model = models.GetResponseWithDelay.model_validate(
        response.json())
    assert not response_model.args
    assert not response_model.data
    assert not response_model.form
    assert not response_model.files


@pytest.mark.parametrize('headers_dict', ApiData.some_headers, ids=[str(item) for item in ApiData.some_headers])
def test_response_headers(api_session, headers_dict):
    response = api_session.get(
        f'{BASE_URL}/response-headers', params=headers_dict, timeout=DEFAULT_TIMEOUT)
    assert response.status_code == 200
    assert 'application/json' in response.headers['Content-Type']
    if headers_dict:
        for key, value in headers_dict.items():
            assert key in response.headers and str(
                value) == response.headers[key]
            assert key in response.json() and str(
                value) == response.json()[key]
