import pytest
import requests
from helpers.order_helpers import generate_order_data


class TestOrderCreation:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"

    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order_with_different_colors(self, color):
        """Проверка создания заказа с разными вариантами цветов"""
        order_data = generate_order_data()
        if color:
            order_data["color"] = color

        response = requests.post(self.BASE_URL, json=order_data)

        assert response.status_code == 201
        assert "track" in response.json()

    def test_create_order_without_required_field(self):
        """Проверка создания заказа без обязательного поля"""
        invalid_data = generate_order_data()
        del invalid_data["firstName"]

        response = requests.post(self.BASE_URL, json=invalid_data)

        assert response.status_code == 400
        assert "Недостаточно данных для создания заказа" in response.json()["message"]