import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from links import main_url, books_url
from data_for_test import my_cookie


class MainPage:
    """
        Этот класс представляет главную страницу интернет-магазина.
    """
    def __init__(self, browser):
        """
            Этот метод является конструктором класса.
            Создает аттрибут _driver, который ссылается на объект браузера.
            Принимает на ввод объект browser.
            Переходит по заданному URL.
        """
        self._driver = browser
        self._driver.get(main_url)

    @allure.step("Провести авторизацию через добавление cookie")
    def authorize(self) -> None:
        """
            Это метод для авторизации через cookie.
            Передает в cookie словарь с токеном.
        """
        self._driver.add_cookie(my_cookie)
        self._driver.refresh()

    @allure.step("Проверить наличие иконки пользователя")
    def check_authorization(self, time: int) -> None:
        """
            Это метод для проверки авторизации.
            Принимает аттрибут time для использования
            явного ождания появления иконки пользователя.
        """
        WebDriverWait(self._driver, time).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.nr-avatar")
            )
        )

    @allure.step("Перейти в раздел 'Книги' каталога")
    def get_book_list(self, time: int) -> None:
        """
            Это метод для перехода в раздел Книги через каталог.
            Принимает аттрибут time для использования
            явного ожидания перехода на страницу "Книги"
        """
        with allure.step("Нажать на значок каталога"):
            self._driver.find_element(
                By.CSS_SELECTOR, "button.nr-header__burger-desktop"
            ).click()
        with allure.step("Нажать на линк 'Книги'"):
            WebDriverWait(self._driver, time).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.catalog-menu-wrapper')
                )
            )
            self._driver.find_element(
                By.CSS_SELECTOR, 'a.category-root-item-link[href="/knigi"]'
            ).click()
            WebDriverWait(self._driver, 20).until(EC.url_to_be(books_url))
        with allure.step("Получить текущий url"):
            new_url = self._driver.current_url
        with allure.step(
            "Проверить, что новый url совпадает с url раздела 'Книги'"
        ):
            assert new_url == books_url

    @allure.step("Поиск товаров через строку поиска")
    def search(self, text, time: int) -> None:
        """
            Это метод для осуществления поиска через строку "Поиск".
            Принимает на ввод текст для поиска и время в секундах
            для использования явного ожидания кликабельности
            кнопки "Найти".
        """
        with allure.step("Ввести в поле 'Поиск' текст"):
            self._driver.find_element(
                By.CSS_SELECTOR, 'input[placeholder="Поиск"]'
                ).send_keys(text)
            WebDriverWait(self._driver, time).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[title="Найти"]')
                )
            )
        with allure.step("Нажать на кнопку 'Найти'"):
            self._driver.find_element(
                By.CSS_SELECTOR, 'button[title="Найти"]'
            ).click()
