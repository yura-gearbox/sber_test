import json


BASE_URL = 'http://httpbin.org'
# BASE_URL = 'http://127.0.0.1:8000'
DEFAULT_TIMEOUT = 5
PARAMETERS_FILE = 'parameters.json'


def _load_parameters():
    with open(PARAMETERS_FILE) as json_file:
        return json.load(json_file)


_parameters = _load_parameters()


class ApiData:
    some_empty_dict = {}
    some_dict = {'key1': 'value1', 'key2': 'value2'}
    some_empty_file = {
        'empty_file': ('empty_file1.txt', '', 'text/plain')
    }
    some_files = {
        'file1': ('document1.txt', 'Very big file content 1', 'text/plain'),
        'file2': ('document2.txt', 'Very big file content 2', 'text/plain')
    }
    some_status_codes = [200, 301, 400, 500]
    some_multiple_status_codes = [200, 201, 204, 301]

    some_delays = _parameters['delays']
    some_headers = _parameters['headers']
