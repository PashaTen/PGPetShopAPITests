import allure
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("pet")
class TestPet:

    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexustent_pet(self):
        with allure.step("Попытка удалить несуществующего питомца"):
            with allure.step("Отправка запроса на улдаление несуществующего питомца"):
                response = requests.delete(f"{BASE_URL}/pet/9999")

            with allure.step("Проверка статуса кода"):
                assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

            with allure.step("Проверка текстового содержима ответа"):
                assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление не существующего питомца"):
            payload = {"id": 9999}

        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            response = requests.get(f"{BASE_URL}/pet/9999", json=payload)

        with allure.step("проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "екст ошибки не совпал с ожидаемым"