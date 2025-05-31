import pytest
import requests
import allure
from helpers.courier_helpers import generate_courier_data, delete_courier


@allure.feature("Courier API")
@allure.story("Courier Creation")
class TestCourierCreation:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        with allure.step("Generate test courier data"):
            self.courier_data = generate_courier_data()
        yield
        with allure.step("Delete test courier"):
            delete_courier(self.courier_data['login'], self.courier_data['password'])

    @allure.title("Test successful courier creation")
    @allure.description("Verify that courier can be created with all required fields")
    def test_create_courier_success(self):
        """Проверка успешного создания курьера со всеми обязательными полями"""
        with allure.step("Send POST request to create courier"):
            response = requests.post(self.BASE_URL, json=self.courier_data)

        with allure.step("Verify response status code is 201"):
            assert response.status_code == 201

        with allure.step("Verify response body contains ok: true"):
            assert response.json() == {"ok": True}

    @allure.title("Test duplicate courier creation")
    @allure.description("Verify that duplicate courier cannot be created")
    def test_create_duplicate_courier(self):
        """Проверка невозможности создания дубликата курьера"""
        with allure.step("Create initial courier"):
            requests.post(self.BASE_URL, json=self.courier_data)

        with allure.step("Send duplicate POST request"):
            response = requests.post(self.BASE_URL, json=self.courier_data)

        with allure.step("Verify response status code is 409"):
            assert response.status_code == 409

        with allure.step("Verify error message about duplicate login"):
            assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Test courier creation with missing field")
    @allure.description("Verify that courier cannot be created without required fields")
    @pytest.mark.parametrize("missing_field", ["login", "password"])  # Только обязательные поля
    def test_create_courier_missing_field(self, missing_field):
        """Проверка создания курьера без обязательного поля"""
        with allure.step(f"Prepare request data without {missing_field}"):
            invalid_data = self.courier_data.copy()
            del invalid_data[missing_field]

        with allure.step("Send POST request with incomplete data"):
            response = requests.post(self.BASE_URL, json=invalid_data)

        with allure.step("Verify response status code is 400"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"