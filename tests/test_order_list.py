import requests


class TestOrderList:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/orders"

    def test_get_order_list_default(self):
        """Проверка получения списка заказов без параметров"""
        response = requests.get(self.BASE_URL)

        assert response.status_code == 200
        assert isinstance(response.json()["orders"], list)

    def test_get_order_list_with_limit(self):
        """Проверка получения списка заказов с лимитом"""
        limit = 5
        response = requests.get(f"{self.BASE_URL}?limit={limit}")

        assert response.status_code == 200
        assert len(response.json()["orders"]) <= limit