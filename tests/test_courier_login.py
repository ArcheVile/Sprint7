import pytest
import requests
from helpers.courier_helpers import create_test_courier


class TestCourierLogin:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.courier_data = create_test_courier()
        yield
        requests.delete(f"{self.BASE_URL}/{self.courier_data['id']}")

    def test_courier_login_success(self):
        """Проверка успешной авторизации курьера"""
        response = requests.post(
            f"{self.BASE_URL}/login",
            json={"login": self.courier_data["login"], "password": self.courier_data["password"]}
        )

        assert response.status_code == 200
        assert "id" in response.json()

    def test_courier_login_wrong_credentials(self):
        """Проверка авторизации с неверными учетными данными"""
        response = requests.post(
            f"{self.BASE_URL}/login",
            json={"login": self.courier_data["login"], "password": "wrong_password"}
        )

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_courier_login_missing_field(self, missing_field):
        """Проверка авторизации без обязательного поля"""
        payload = {"login": self.courier_data["login"], "password": self.courier_data["password"]}
        del payload[missing_field]

        response = requests.post(f"{self.BASE_URL}/login", json=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"