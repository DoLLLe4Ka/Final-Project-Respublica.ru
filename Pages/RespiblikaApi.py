import allure
import requests
from data_for_test import my_cookie
from links import *

class Api:
    def __init__(self, url):
        """
            Этот метод является конструктором класса.
            Создает аттрибут _driver, который ссылается на объект браузера.
            Принимает на ввод объект browser.
            Открывает указанный URL.
        """
        self._url = url


    @allure.step("Получить список бестселлеров")
    def get_bestsellers_list(self):
        """
            Это метод для получения информации о книгах
            в разделе Бестселлеры.
            Возвращает json. 
        """
        list = requests.get(self._url+"listing/knigi/bestsellery")
        assert list.status_code == 200
        return list.json()
    

    @allure.step("Добавление товара в корзину")
    def add_book_to_cart(self, item_id: int, quantity: int, update=True):
        """
            Этот метод добавляет товар в корзину.
            Принимает id товара, количество товара
            и аттрибут update.
            Возвращает json c данными об успешности запроса.        
        """
        with allure.step("Добавить товар в корзину"):
            book = {
                "item":{
                    "item_id": item_id,
                    "quantity": quantity,
                    "update": update
                }
            }
            resp = requests.post(self._url+'cart/add_item', json=book)
        with allure.step("Проверить статус-код"):
            assert resp.status_code == 200
            return resp.json()
    
    @allure.step("Отправка запроса с невалидным id")
    def add_book_to_cart_invalid_id(self, item_id: int, quantity: int, update=True):
        """
            Это метод для проверки статуса 400 в ответе
            при добавлении в корзину товара с невалидным id.
            Принимает id товара, количество товара и аттрибут update.
            Возвращает json c данными об успешности запроса.        
        """
        with allure.step("Отправить запрос на добавление товара с невалидным id"):
            book = {
                "item":{
                    "item_id": item_id,
                    "quantity": quantity,
                    "update": update
                }
            }
            resp = requests.post(self._url+'cart/add_item', json=book)
        with allure.step("Проверить статус-код"):
            assert resp.status_code == 400
            return resp.json()
    

    @allure.step("Получить книги в корзине")
    def get_books_in_cart(self, cart_id):
        """
            Это метод для получения информации о книгах в корзине.
            Принимает id корзины, возвращает json с информацией
            о корзине и книгах в ней.
        """
        cart = {
            "cart_id": cart_id
        }
        resp = requests.post(self._url+'cart/get_cart', json=cart)
        return resp.json()
    

    @allure.step("Удаление товара из корзины")
    def delete(self, cart_item_id: int):
        """
            Этот метод удаляет товар из корзины.
            Принимает id товара в корзине, возвращает json с информацией
            об успешности запроса.
        """
        cart = {
            "item":{
                "item_id": cart_item_id
            }
        }
        resp = requests.post(self._url+'cart/remove_item', json=cart)
        return resp.json()


    @allure.step("Увеличение количества выбранного товар")
    def increase_quantity_in_cart(self, cart_item_id: int):
        """
            Это метод для увеличения количества выбранного товара
            в корзине. 
            Принимает id товара в корзине, добавляет 1 к количеству. 
            Возвращает возвращает json с информацией о корзине и книгах в ней.
        """
        with allure.step("Добавить 1 к количеству товара"):
            cart = {
                "item":{
                    "item_id": cart_item_id
                }
            }
            resp = requests.post(self._url+'cart/plus_item', json=cart)
        with allure.step("Проверить статус-код"):
            assert resp.status_code == 200
            return resp.json()
