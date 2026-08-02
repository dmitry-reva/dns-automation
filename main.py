import requests
import dns.resolver
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

def get_current_a_record(domain: str) -> str:
    """
    Делает DNS-запрос и возвращает первый найденный A-адрес для домена.
    Это то, что реально резолвится для домена, без обращения к API Яндекс 360.
    """
    resolver = dns.resolver.Resolver()
    answers = resolver.resolve(domain, "A")
    return str(answers[0])

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
        current_ip = get_current_a_record(NAME+"."+DOMAIN)
        print(f"Текущий IP в DNS: {current_ip}")
        if external_ip == current_ip:
            print("IP не изменился — обновление не требуется.")
        else:
            print("Обнаружено изменение IP — выполняем обновление DNS.")
            update_a_record(external_ip)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
