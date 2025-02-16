import pytest
import requests
from utils import generate_seller_id, validate_uuid

BASE_URL = "https://qa-internship.avito.com/api/1"

@pytest.fixture
def created_ad():
    seller_id = generate_seller_id()
    payload = {
        "sellerID": seller_id,
        "name": "Тестовый товар",
        "price": 1000
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(f"{BASE_URL}/item", json=payload, headers=headers)
    response_data = response.json()
    
    status = response_data.get("status", "")
    ad_id = status.split(" - ")[-1] if " - " in status else None
    
    if not ad_id or not validate_uuid(ad_id):
        pytest.fail(f"Не удалось получить ID объявления. Ответ: {response_data}")
    
    return {"seller_id": seller_id, "ad_id": ad_id}

def test_statistics(created_ad):
    ad_id = created_ad["ad_id"]
    response = requests.get(f"{BASE_URL}/statistic/{ad_id}")
    
    print("\n[DEBUG] Ответ статистики:", response.json())
    assert response.status_code == 200, "Ошибка запроса статистики"
    
    stats_data = response.json()
    assert isinstance(stats_data, list), "Ответ должен быть списком"
    assert len(stats_data) > 0, "Список статистики пуст"
    stats = stats_data[0]
    assert stats["viewCount"] >= 0, "Некорректные просмотры"

def test_negative_price():
    payload = {
        "sellerID": generate_seller_id(),
        "name": "Телевизор",
        "price": -5000
    }
    response = requests.post(f"{BASE_URL}/item", json=payload)
    assert response.status_code == 200, "Сервер не обработал запрос"
    print("\n[BUG] Сервер принимает отрицательную цену. Ответ:", response.json())