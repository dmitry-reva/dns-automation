import requests
from config import YANDEX_OAUTH_TOKEN, ORG_ID, DOMAIN, RECORD_ID, TTL, NAME

BASE_URL = "https://api360.yandex.net"

def get_external_ip():
    """Получает публичный IPv4-адрес машины через несколько сервисов с fallback."""
    services = [
        "https://api.ipify.org",
        "https://icanhazip.com",
        "https://ifconfig.me/ip",
        "https://ipecho.net/plain"
    ]
    for service in services:
        try:
            resp = requests.get(service, timeout=3)
            if resp.status_code == 200:
                ip = resp.text.strip()
                # Простая валидация IPv4
                if len(ip.split(".")) == 4 and all(p.isdigit() for p in ip.split(".")):
                    return ip
        except Exception:
            continue
    raise RuntimeError("Не удалось получить внешний IP ни через один сервис")

def get_current_a_record():
    """Получает текущую A-запись по recordId."""
    url = f"{BASE_URL}/directory/v1/org/{ORG_ID}/domains/{DOMAIN}/dns/{RECORD_ID}"
    headers = {"Authorization": f"OAuth {YANDEX_OAUTH_TOKEN}",  "Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # В ответе API Яндекс 360 для A-записи поле с IP называется "address"
    return data.get("address")

def update_a_record(new_ip):
    """Обновляет A-запись, если нужно."""
    url = f"{BASE_URL}/directory/v1/org/{ORG_ID}/domains/{DOMAIN}/dns/{RECORD_ID}"
    headers = {
        "Authorization": f"OAuth {YANDEX_OAUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "A",
        "name": NAME,
        "ttl": TTL,
        "address": new_ip
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    if resp.status_code == 200:
        print(f"A-запись обновлена на IP: {new_ip}")
        return True
    else:
        print(f"Ошибка API при обновлении: {resp.status_code}")
        print(resp.text)
        return False

if __name__ == "__main__":
    try:
        external_ip = get_external_ip()
        print(f"Текущий внешний IP: {external_ip}")
        update_a_record(external_ip)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
