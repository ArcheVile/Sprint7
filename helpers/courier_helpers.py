import requests
import random
import string


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_courier_data():
    return {
        "login": f"test_{generate_random_string(5)}_{random.randint(1, 10000)}",
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }


def create_test_courier():
    courier_data = generate_courier_data()
    requests.post("https://qa-scooter.praktikum-services.ru/api/v1/courier", json=courier_data)

    login_response = requests.post(
        "https://qa-scooter.praktikum-services.ru/api/v1/courier/login",
        json={"login": courier_data["login"], "password": courier_data["password"]}
    )
    courier_data["id"] = login_response.json()["id"]
    return courier_data


def delete_courier(login, password):
    login_data = {"login": login, "password": password}
    auth_response = requests.post(
        "https://qa-scooter.praktikum-services.ru/api/v1/courier/login",
        json=login_data
    )
    if auth_response.status_code == 200:
        courier_id = auth_response.json()["id"]
        requests.delete(f"https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}")