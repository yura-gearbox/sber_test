from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    # открыть страницу
    def open(self, url: str) -> None:
        self.page.goto(url, wait_until='commit')

    # клик на элементе
    def click_on_element(self, locator: str) -> None:
        self.page.click(selector=locator)

    # заполнить поле текстом
    def fill_field(self, locator: str, text: str) -> None:
        self.page.fill(selector=locator, value=text)

    # проверка, что страница загружена
    def wait_for_load(self, url: str, timeout: int = 3) -> None:
        self.page.wait_for_url(url, timeout=timeout * 1000, wait_until="load")

    # проверка доступности элемента
    def should_be_enabled(self, locator: str, timeout: int = 3, err_msg: str = None) -> None:
        expect(self.page.locator(locator), err_msg).to_be_enabled(
            timeout=timeout * 1000)

    # проверка видимости элемента
    def should_be_visible(self, locator: str, timeout: int = 3, err_msg: str = None) -> None:
        expect(self.page.locator(locator), err_msg).to_be_visible(
            timeout=timeout * 1000)
