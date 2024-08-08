import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from links import cart_url


class CartPage:
    """
        Этот класс представляет собой корзину интернет-магазина.
    """
    def __init__(self, browser):
        """
            Этот метод является конструктором класса.
            Создает аттрибут _driver, который ссылается на объект браузера.
            Принимает на ввод объект browser, открывает заданный url.
        """
        self._driver = browser
        self._driver.get(cart_url)

    @allure.step("Получить количество предметов в корзине")
    def get_number_of_items(self, time: int) -> int:
        """
            Это метод для получения количества предметов в корзине.
            Принимает аттрибут "время" для использования явного ожидания
            отображения элементов на странице.
            Возвращает количество элементов на странице.
        """
        WebDriverWait(self._driver, time).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'input[type="checkbox"]')
            )
        )
        added_books = self._driver.find_elements(
            By.CSS_SELECTOR, 'input[type="checkbox"]'
        )
        return len(added_books)
