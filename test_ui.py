"""
1. Перейти на страницу https://online.sberbank.ru/CSAFront/index.do
2. Страница должна загрузиться в течение 10 секунд
3. Ввести логин Avtotest
4. Ввести pswd 123456
5. Нажать кнопку Продолжить
6. Проверить ожидаемый результат: появится сообщение об ошибке
"""

import pytest
from playwright.sync_api import Page
from base_page import BasePage
from ui_data import BASE_URL, TIMEOUT, LOGIN, PASSWORD, Locators


pytestmark = pytest.mark.ui


def test_login_error(page: Page):
    page = BasePage(page)
    # вход на главную страницу, здесь предлагается выбор варианта авторизации
    page.open(BASE_URL)
    page.wait_for_load(BASE_URL, timeout=TIMEOUT)

    # выбор авторизации по логину и паролю
    page.click_on_element(Locators.button_auth_by_login)
    page.should_be_enabled(Locators.button_login, timeout=TIMEOUT, err_msg=f'Страница авторизации по логину не загрузилась за {TIMEOUT} секунд')

    # ввод логина и пароля
    page.fill_field(Locators.login_field, LOGIN)
    page.fill_field(Locators.password_field, PASSWORD)

    # Клик по кнопке Войти
    page.click_on_element(Locators.button_login)

    # проверка ошибки авторизации
    page.should_be_visible(
        Locators.alert_text, err_msg='Сообщение об ошибке авторизации не появилось')
