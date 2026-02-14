import allure
import jsonschema
import pytest
import requests

from .schemas.inventory_schema import INVENTORY_SCHEMA
from .schemas.order_schema import ORDER_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("store")
class TestStore:

    @allure.title("Размещение заказа")
    def test_create_inventory(self):
        with allure.step("Подготовка данных для создания заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка POST-запроса на store/order с подготовленными данными"):
            response = requests.post(f"{BASE_URL}/store/order", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка содержимого ответа и валидация JSON-схемы"):
            response_json = response.json()
            jsonschema.validate(response_json, ORDER_SCHEMA)
            assert response_json["id"] == payload["id"]
            assert response_json["petId"] == payload["petId"]
            assert response_json["quantity"] == payload["quantity"]
            assert response_json["status"] == payload["status"]
            assert response_json["complete"] == payload["complete"]

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка GET-запроса на /store/order/{orderId}"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка что ответ содержит данные заказа с id = 1"):
            response_json = response.json()
            assert response_json["id"] == order_id

    @allure.title("Удаления заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка DELETE-запроса на /store/order/{orderId}"):
            delete_response = requests.delete(f"{BASE_URL}/store/order/{order_id}")
        with allure.step("Проверка статуса на DELETE"):
            assert delete_response.status_code == 200

        with allure.step("Отправка GET-запроса на /store/order/{orderId}"):
            get_response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа на GET"):
            assert get_response.status_code == 404

    @allure.title("Попытка получить ифнормацию о несуществующем заказе")
    def test_get_nonexistent_order_by_id(self):
        with allure.step("Отправка GET-запроса на /store/order/9999"):
            response = requests.get(f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Отправка GET-запроса на /store/inventory"):
            response = requests.get(f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка содержимого ответа в формате словаря"):
            response_json = response.json()
            assert isinstance(response_json, dict)

        with allure.step("Проверка JSON-схемы"):
            jsonschema.validate(response_json, INVENTORY_SCHEMA)