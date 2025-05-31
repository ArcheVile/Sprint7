import requests
import random


def generate_order_data():
    return {
        "firstName": "Тест",
        "lastName": "Тестов",
        "address": "Москва, ул. Тестовая, 1",
        "metroStation": random.randint(1, 10),
        "phone": f"+7999{random.randint(1000000, 9999999)}",
        "rentTime": random.randint(1, 7),
        "deliveryDate": "2023-06-06",
        "comment": "Тестовый заказ"
    }


def create_test_order():
    order_data = generate_order_data()
    response = requests.post(
        "https://qa-scooter.praktikum-services.ru/api/v1/orders",
        json=order_data
    )
    order_data["track"] = response.json()["track"]

    # Получаем ID заказа
    track_response = requests.get(
        f"https://qa-scooter.praktikum-services.ru/api/v1/orders/track?t={order_data['track']}"
    )
    order_data["id"] = track_response.json()["order"]["id"]
    return order_data