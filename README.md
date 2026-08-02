# DNS A-Record Updater for Yandex 360

Автоматизированное обновление A‑записи домена в Яндекс 360 через API при изменении внешнего IP‑адреса сервера.

Скрипт определяет текущий публичный IP, сравнивает его с текущим значением A‑записи и обновляет запись только при расхождении. Работает в Debian, запускается через cron или systemd.

## Возможности

- Автоматическое определение внешнего IPv4 через несколько публичных API (с fallback).
- Получение текущего значения A‑записи через API Яндекс 360.
- Обновление A‑записи только при изменении IP (минимизация запросов).
- Поддержка имени записи: корень (`@`) или поддомен (например, `www`).
- Логирование действий и ошибок.
- Конфигурация через `.env` (без хардкода секретов).

## Требования

- ОС: Debian (любая современная версия).
- Python: 3.8 или выше.
- Права: пользователь с доступом к сети и возможностью создания файлов/директорий.
- Зависимости: `requests`, `python-dotenv`.

## Предварительные условия в Яндекс 360

1. **OAuth‑токен** с правом `directory:manage_dns`.
2. **ORG_ID** — идентификатор организации в админ‑панели Яндекс 360.
3. **DOMAIN** — домен, которым управляет организация.
4. **RECORD_ID** — ID существующей A‑записи (получается через API или в админке).

> Важно: сначала нужно получить `RECORD_ID` для целевой A‑записи. Без него обновление невозможно.

## Установка

### 1. Подготовка системы (Debian)

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip -y
```

### 2. Создание проекта

```bash
mkdir -p ~/dns-automation
cd ~/dns-automation
python3 -m venv .venv
source .venv/bin/activate
pip install -r ~/dns-automation/requirements.txt
```
или
```bash
pip install requests python-dotenv dns.resolver
pip freeze > requirements.txt
```

### 3. Создание файлов
Создай файлы config.py, main.py и .env в папке ~/dns-automation (код смотри в разделе «Файлы проекта»).

### 4. Настройка .env

> Не выкладывай .env в публичные репозитории.

Пример содержимого .env:
```ini
YANDEX_OAUTH_TOKEN=y0_AgAAAA...
ORG_ID=12345678
DOMAIN=example.com
RECORD_ID=987654321
TTL=3600
NAME=@
```
NAME=@ — для корневого домена (example.com).

NAME=www — для поддомена (www.example.com).
> Предположительно для корневого домена нужно исправить определение current_ip в main.py 

### Получение RECORD_ID
Если RECORD_ID неизвестен, сделай разовый запрос:
```bash
curl -H "Authorization: OAuth y0_AgAAAA..." \
  "https://api360.yandex.net/directory/v1/org/12345678/domains/example.com/dns"
  ```