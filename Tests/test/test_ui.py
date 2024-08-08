import allure
import pytest
from Pages.MainUI import MainPage
from Pages.ResultPageUI import ResultPage
from Pages.CartUI import CartPage
from data_for_test import *
from links import *

@pytest.mark.ui
@allure.title("Авторизация в приложении")
@allure.description("Авторизация в приложении при помощи cookie")
@allure.feature("Авторизация")
@allure.severity(severity_level='blocker')
def test_auth(chrome_browser):
    main_page = MainPage(chrome_browser)
    main_page.authorize()
    main_page.check_authorization(10)

@pytest.mark.ui
@allure.title("Получение списка книг")
@allure.description("Получение списка книг в разделе 'Книги' каталога")
@allure.feature("Получение списка книг")
@allure.severity(severity_level='blocker')
def test_get_book_list(chrome_browser):
    main_page = MainPage(chrome_browser)
    main_page.get_book_list(15)

@pytest.mark.ui
@allure.title("Получение сообщения о неудачном результате поиска")
@allure.description("Проверка сообщения о том, что товар не найден")
@allure.feature("Поиск и фильтрация результатов")
@allure.severity(severity_level='critical')
def test_search_empty_result(chrome_browser):
    main_page = MainPage(chrome_browser)
    main_page.search(invalid_title, 20)
    result_page = ResultPage(chrome_browser)
    msg = result_page.get_empty_result_message(20)
    with allure.step("Проверить текст сообщения"):
        assert msg == "По вашему запросу товары не найдены."

@pytest.mark.ui
@allure.title("Поиск товара")
@allure.description("Проверка результатов поиска")
@allure.feature("Поиск и фильтрация результатов")
@allure.severity(severity_level='critical')
def test_search_goods(chrome_browser):
    main_page = MainPage(chrome_browser)
    main_page.search(title, 10)
    result_page = ResultPage(chrome_browser)
    actual_res = result_page.get_result(10)
    expected_res = result_page.сount_goods(10)
    with allure.step(
        """
        Проверить, что количество товаров в счетчике
        совпадает с фактическим количеством товаров на странице
        """
    ):
        assert actual_res == expected_res

@pytest.mark.ui
@allure.title("Получение количества товаров в корзине")
@allure.description("Проверка, что все выбранные товары добавлены в корзину ")
@allure.feature("Добавление товара")
@allure.severity(severity_level='critical')
def test_get_added_goods(chrome_browser):
    main_page = MainPage(chrome_browser)
    main_page.search(title_2, 15)
    result_page = ResultPage(chrome_browser)
    result_page.get_result(15)
    expected_res = result_page.сount_goods(15)
    cart_page = CartPage(chrome_browser)
    actual_res = cart_page.get_number_of_items(15)
    with allure.step(
        """
        Проверить, что количество товаров в корзине
        совпадает с количеством кликов по кнопке
        'В корзину'
        """
    ):
        assert actual_res == expected_res

@pytest.mark.ui
@allure.title("Фильтрация результатов поиска")
@allure.description(
    "Проверка, что приложение фильтрует результаты по наличию скидки"
    )
@allure.feature("Поиск и фильтрация результатов")
@allure.severity(severity_level='major')
def test_filter_search_results(chrome_browser):
    main_page = MainPage(chrome_browser)
    main_page.search(title_3, 20)
    result_page = ResultPage(chrome_browser)
    len_before = result_page.get_result(20)
    result_page.filter_results(30)
    len_after = result_page.get_filtered_search_result(20)
    with allure.step(
        """Убедиться, что отфильтрованный список
        товара короче списка до фильтрации"""
    ):
        assert len_after < len_before
