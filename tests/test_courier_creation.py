import pytest
import requests
from helpers.courier_helpers import generate_courier_data, delete_courier


class TestCourierCreation:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.courier_data = generate_courier_data()
        yield
        delete_courier(self.courier_data['login'], self.courier_data['password'])

    def test_create_courier_success(self):
        """Проверка успешного создания курьера со всеми обязательными полями"""
        response = requests.post(self.BASE_URL, json=self.courier_data)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    def test_create_duplicate_courier(self):
        """Проверка невозможности создания дубликата курьера"""
        requests.post(self.BASE_URL, json=self.courier_data)
        response = requests.post(self.BASE_URL, json=self.courier_data)

        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется"

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field(self, missing_field):
        """Проверка создания курьера без обязательного поля"""
        invalid_data = self.courier_data.copy()
        del invalid_data[missing_field]

        response = requests.post(self.BASE_URL, json=invalid_data)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"