import allure
import pytest
from Pages.RespiblikaApi import Api
from links import base_url
from data_for_test import *

api = Api(base_url)


@pytest.mark.api
@allure.title("Получение списка бестселлеров")
@allure.description("Получение списка книг в категории Бестселлеры")
@allure.feature("Получение списка книг")
@allure.severity(severity_level='blocker')
def test_get_bestsellers_list():
    body = api.get_bestsellers_list()
    books = body['items']['data']
    with allure.step("Убедиться, что список книг не пустой"):
        assert len(books) > 0


@pytest.mark.api
@allure.title("Добавление товара в корзину")
@allure.description("Добавление книги из категории Бестселлеры в корзину")
@allure.feature("Добавление товара")
@allure.severity(severity_level='blocker')
def test_add_book_to_cart():
    book_list = api.get_bestsellers_list()
    with allure.step("Записать первый id в списке"):
        book_id = book_list['items']['data'][0]['attributes']['id']
    with allure.step("Отправить запрос на добавление книги"):
        with allure.step("Ввести данные для запроса"):
            item_id = book_id
            quantity = 1
        with allure.step("Отправить запрос"):
            new_book = api.add_book_to_cart(item_id, quantity)
    with allure.step("Записать id корзины"):
        cart_id = new_book['cart']['id']
    body = api.get_books_in_cart(cart_id)
    with allure.step("Проверить ответ"):
        with allure.step("В корзину добавлен 1 предмет"):
            assert len(body['cart']['items']) == 1
        with allure.step("В корзину добавлен товар с верным id"):
            assert body['cart']['items'][0]['item']['data']['id'] == str(book_id)
        with allure.step(
            "Количество добавленного товара соответствует заданному числу"
        ):
            assert body['cart']['items'][0]['quantity'] == quantity
        with allure.step("Сообщение соответствует ожидаемому"):
            assert body['message'] == 'Корзина создана'


@pytest.mark.api
@allure.title("Добавление товара с невалидным id")
@allure.description("Добавление товара с невалидным id в корзину")
@allure.feature("Добавление товара")
@allure.severity(severity_level='critical')
def test_add_book_invalid_id():
    with allure.step("Отправить запрос на добавление товара с невалидным id"):
        with allure.step("Ввести данные для запроса"):
            item_id = invalid_id
            quantity = 2
        with allure.step("Отправить запрос"):
            body = api.add_book_to_cart_invalid_id(item_id, quantity)
    with allure.step("Провести проверки"):
        with allure.step("Запрос не успешен"):
            assert body['success'] == False
        with allure.step("Сообщение 'Товар не добавлен'"):
            assert body['message'] == 'Товар не добавлен'


@pytest.mark.api
@allure.title("Увеличение количества товара")
@allure.description("Увеличение количества выбранного товара в корзине")
@allure.feature("Добавление товара")
@allure.severity(severity_level='critical')
def test_increase_quantity_in_cart():
    book_list = api.get_bestsellers_list()
    with allure.step("Записать первый id в списке"):
        book_id = book_list['items']['data'][0]['attributes']['id']
    with allure.step("Добавить книгу"):
        with allure.step("Записать данные для запроса"):
            item_id = book_id
            quantity = 1
        with allure.step("Отправить запрос на добавление в корзину"):
            new_book = api.add_book_to_cart(item_id, quantity)
    with allure.step("Записать id корзины"):
        cart_id = new_book['cart']['id']
        body = api.get_books_in_cart(cart_id)
        with allure.step("Записать количество товара"):
            number_before = body['cart']['items'][0]['quantity']
    with allure.step("Записать id товара в корзине"):
        cart_item_id = body['cart']['items'][0]['id']
    with allure.step("Увеличить количество товара в корзине"):
        result = api.increase_quantity_in_cart(cart_item_id)
        with allure.step("Записать количество товара"):
            number_after = result['cart']['items'][0]['quantity']
    with allure.step("Провести проверки"):
        with allure.step("Количество товара увеличилось на 1"):
            assert number_after - number_before == 1
        with allure.step("Количество товара равно 2"):
            assert result['cart']['items'][0]['quantity'] == 2


@pytest.mark.api
@allure.title("Удаление товара из корзины")
@allure.description("Удаление выбранного товара из корзины")
@allure.feature("Удаление товара")
@allure.severity(severity_level='critical')
def test_delete_item_from_cart():
    book_list = api.get_bestsellers_list()
    with allure.step("Записать количество товара"):
        book_id = book_list['items']['data'][0]['attributes']['id']
    with allure.step("Отправить запрос на добавление книги"):
        with allure.step("Записать данные для запроса"):
            item_id = book_id
            quantity = 1
        with allure.step("Добавить книгу в корзину"):
            new_book = api.add_book_to_cart(item_id, quantity)
    with allure.step("Записать id корзины"):
        cart_id = new_book['cart']['id']
    with allure.step("Получить id товара в корзине"):
        body = api.get_books_in_cart(cart_id)
        cart_item_id = body['cart']['items'][0]['id']
    with allure.step("Удалить товар из корзины"):
        result = api.delete(cart_item_id)
        with allure.step("Провести проверки"):
            with allure.step("Сообщение об удалении товара"):
                assert result['message'] == "Товар удален"
            with allure.step("Запрос успешен"):
                assert result['success'] == True


@pytest.mark.api
@allure.title("Удаление товара c невалидным id")
@allure.description("Удаление товара с невалидным id из корзины")
@allure.feature("Удаление товара")
@allure.severity(severity_level='major')
def test_delete_item_no_id():
    cart_item_id = 1000
    result = api.delete(cart_item_id)
    with allure.step("Провести проверки"):
        with allure.step("Проверить сообщение об удалении товара"):
            assert result['message'] == "Товар не удален"
        with allure.step("Убедиться, что запрос не успешен"):
            assert result['success'] == False
