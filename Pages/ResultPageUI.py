import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ResultPage:
    """
        Этот класс представляет страницу с результатами поиска
        через поисковую строку.
    """

    def __init__(self, browser):
        self._driver = browser
        """
            Этот метод является конструктором класса.
            Создает аттрибут _driver, который ссылается на объект браузера.
            Принимает на ввод объект browser.
        """

    @allure.step("Подсчет количества товаров, добавленных в корзину")
    def сount_goods(self, time: int) -> int:
        """
            Этот метод принимает на ввод время ожидания,
            пока все кнопки "В корзину" не отобразятся
            на странице, нажимает на кнопки и подсчитывает
            количество кликов, и прибавляет количество кнопок "Нет в наличии",
            если таковые имеются.
            Возвращает количество товаров на странице.
        """
        with allure.step("Кликнуть по каждой кнопке 'В корзину'"):
            WebDriverWait(self._driver, time).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'button[title="Добавить в корзину"]')
                )
            )
            add_buttons = self._driver.find_elements(
                By.CSS_SELECTOR, 'button[title="Добавить в корзину"]'
            )
            counter = 0
            for btn in add_buttons:
                WebDriverWait(self._driver, time).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'button[title="Добавить в корзину"]')
                    )
                )
                btn.click()
                with allure.step("Посчитать количество нажатых кнопок"):
                    WebDriverWait(self._driver, time).until(
                        EC.text_to_be_present_in_element(
                            (
                                (By.CSS_SELECTOR, 'a[title="Перейти в корзину"]')
                            ),
                            '1'
                        )
                    )
                counter += 1
        with allure.step(
            "Посчитать количество товаров, которых нет в наличии"
        ):
            no_buttons = self._driver.find_elements(
                By.CSS_SELECTOR, 'button[title="Нет в наличии"]'
            )
            num = len(no_buttons)
        with allure.step("Посчитать общее количество товаров на странице"):
            return counter+num

    @allure.step("Получение сообщения 'Товар не найден")
    def get_empty_result_message(self, time: int) -> str:
        """
            Этот метод проверяет, что на странице с "пустым"
            результатом поиска отображается сообщение "Товар не найден"
            Принимает на ввод время ожидания появления элемента
            с сообщением на странице результата поиска.
            Возвращает текст сообщения.
        """
        with allure.step(
            'Убедиться, что появляется сообщение, что товар не найден'
        ):
            WebDriverWait(self._driver, time).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.cart-none-title')
                )
            )
        with allure.step('Записать текст сообщения'):
            txt = self._driver.find_element(
                By.CSS_SELECTOR, 'div.cart-none-title'
            ).text
            return txt

    @allure.step("Получение количества товаров на странице")
    def get_result(self, time: int) -> str:
        """
            Этот метод принимает на ввод время ожидания,
            проверяет, что появился счетчик товаров
            и возвращает количество товаров на странице.
        """
        WebDriverWait(self._driver, time).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.items-count')
            )
        )
        txt = self._driver.find_element(
            By.CSS_SELECTOR, 'div.items-count'
        ).find_element(By.CSS_SELECTOR, 'strong').text
        return int(txt)

    @allure.step("Отфильтровать результаты поиска по наличию скидки")
    def filter_results(self, time: int) -> None:
        """
            Это метод для фильтрации результатов поиска.
            Принимает на ввод время ожидания, нажимает
            на чек-бокс "Только товары со скидкой"
            и на кнопку "Показать __ товаров"
        """
        self._driver.implicitly_wait(10)
        checkbox = self._driver.find_element(
            By.CSS_SELECTOR, "label.filter-checkbox-title"
        )
        checkbox.click()
        WebDriverWait(self._driver, time).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'button.filter-done-button')
            )
        )
        button = self._driver.find_element(
            By.CSS_SELECTOR, 'div.filter-check-popup'
        ).find_element(By.CSS_SELECTOR, 'button.filter-check-button')
        WebDriverWait(self._driver, time).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.filter-done-button')
            )
        )
        button.click()

    @allure.step("Получить количество отфильтрованных товаров")
    def get_filtered_search_result(self, time: int) -> str:
        """
            Это метод для отображения результатов поиска.
            Принимает на ввод время ожидания,
            проверяет, что URL страницы изменился
            и возвращает количество товаров на странице.
        """
        current_url = self._driver.current_url
        WebDriverWait(self._driver, time).until(
            EC.url_changes(current_url)
        )
        txt = self._driver.find_element(
            By.CSS_SELECTOR, 'div.items-count'
        ).find_element(By.CSS_SELECTOR, 'strong').text
        return int(txt)
