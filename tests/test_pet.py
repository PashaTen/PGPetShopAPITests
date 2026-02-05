import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("pet")
class TestPet:

    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Попытка удалить несуществующего питомца"):
            with allure.step("Отправка запроса на удаление несуществующего питомца"):
                response = requests.delete(f"{BASE_URL}/pet/9999")

            with allure.step("Проверка статуса кода"):
                assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

            with allure.step("Проверка текстового содержима ответа"):
                assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление не существующего питомца"):
            payload = {"id": 9999,
                       "name": "Non-existent Pet",
                       "status": "available"
                       }

        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            response = requests.put(f"{BASE_URL}/pet/", json=payload)

        with allure.step("проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса кода"):
            assert response.status_code == 404, "Код ответа не совпадает с ожидаемым"

        with allure.step("Проверка текстового содежимого"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {"id": 1,
                       "name": "Buddy",
                       "status": "available"
                       }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(f"{BASE_URL}/pet/", json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца несовпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "id питомца несовпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "id питомца несовпадает с ожидаемым"

    @allure.title("Добавление нового питомца с полными данными")
    def test_add_pet_with_full_data(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [
                    {
                        "id": 0,
                        "name": "string",
                    }
                ],
                "status": "available"
            }
        with allure.step("Отправка запроса на создания питомца"):
            response = requests.post(f"{BASE_URL}/pet/", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Валидация JSON-схемы ответа"):
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка всех параметров питомца в ответе"):
            assert response_json['id'] == payload['id']
            assert response_json['name'] == payload['name']
            assert response_json['status'] == payload['status']
            assert response_json['category']['id'] == payload['category']['id']
            assert response_json['category']['name'] == payload['category']['name']
            assert response_json['photoUrls'] == payload['photoUrls']
            assert response_json['tags'][0]['id'] == payload['tags'][0]['id']
            assert response_json['tags'][0]['name'] == payload['tags'][0]['name']

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_pet_name_and_status(self, update_pet, create_pet):
        with allure.step("Проверка исходных данных питомца"):
            assert create_pet["id"] == 1
            assert create_pet["name"] == "Buddy"
            assert create_pet["status"] == "available"

        with allure.step("Проверка обновленных данных"):
            assert update_pet["id"] == 1
            assert update_pet["name"] == "Buddy Updated"
            assert update_pet["status"] == "sold"
        with allure.step("Подготовка данных к обновлению"):
            update_payload = {
                "id": 1,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка put-запроса на /pet с подготовленными данными"):
            response = requests.put(f"{BASE_URL}/pet/", json=update_payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка ответа с обновленными данными питомца"):
            update_pet = response.json()
            assert update_pet["id"] == 1
            assert update_pet["name"] == "Buddy Updated"
            assert update_pet["status"] == "sold"


@allure.title("Удаление питомца по ID")
def test_delete_pet_by_id(create_pet):
    with allure.step("Отправить POST-запрос на /pet с подготовленными данными"):
        create_payload = {
            "id": 1,
            "name": "Buddy",
            "status": "available"
        }
        create_response = requests.post(f"{BASE_URL}/pet/", json=create_payload)
    with allure.step("Проверить статус ответа"):
        assert create_response.status_code == 200

    with allure.step("Получение ID созданного питомца"):
        pet_id = create_pet["id"]

    with allure.step("Отправка DELETE-запроса"):
        delete_response = requests.delete(f"{BASE_URL}/pet/{pet_id}")

    with allure.step("Проверка статуса ответа"):
        assert delete_response.status_code == 200

    with allure.step("Отправка GET-запроса"):
        response = requests.get(f"{BASE_URL}/pet/{pet_id}")

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 404
