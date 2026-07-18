
BASE_URL = 'https://online.sberbank.ru/CSAFront/index.do'
TIMEOUT = 10
LOGIN = 'Avtotest'
PASSWORD = '123456'


class Locators:
    button_auth_by_login = 'button[aria-label="По логину и паролю"]'
    login_field = '[data-testid="input-text"]'
    password_field = '[data-testid="input-password"]'
    button_login = '[data-testid="button-continue"]'
    alert_text = 'div#password-error[role="alert"]'
