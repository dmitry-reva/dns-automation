# DNS A-Record Updater for Yandex 360

> Создано для доступа к хосту с динамическим IP‑адресом (без DynDNS и подобного).

Автоматизированное обновление A‑записи домена в Яндекс 360 через API при изменении внешнего IP‑адреса сервера.

Скрипт определяет текущий публичный IP, сравнивает его с текущим значением A‑записи и обновляет запись только при расхождении. Работает в Debian, запускается через cron или systemd.

## Возможности

- Автоматическое определение внешнего IPv4 через несколько публичных API (с fallback).
- Получение текущего значения A‑записи.
- Обновление A‑записи только при изменении IP (минимизация запросов).
- Поддержка имени записи: корень (`@`) или поддомен (например, `www`). Но это не точно.
- Логирование действий и ошибок.
- Конфигурация через `.env` (без хардкода секретов).

## Требования

- ОС: Debian (любая современная версия).
- Python: 3.8 или выше.
- Права: пользователь с доступом к сети и возможностью создания файлов/директорий.
- Зависимости: `requests`, `python-dotenv`, `dns.resolver`.

## Предварительные условия в Яндекс 360

1. **OAuth‑токен** с правом `directory:manage_dns`.
2. **ORG_ID** — идентификатор организации в админ‑панели Яндекс 360.
3. **DOMAIN** — домен, которым управляет организация.
4. **RECORD_ID** — ID существующей A‑записи (получается через API или в админке).

## Установка

### 1. Подготовка системы (Debian)

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip -y
```

### 2. Создание проекта

```bash
cd ~
git clone https://github.com/dmitry-reva/dns-automation
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

Создать .env в папке ~/dns-automation.

```bash
touch ~/dns-automation/.env
```
> Не размещайте ваш .env в публичные репозитории.


### 4. Настройка .env

Пример содержимого .env:
```ini
YANDEX_OAUTH_TOKEN=y0_AgAAAA...
ORG_ID=12345678
DOMAIN=example.com
RECORD_ID=987654321
TTL=3600
NAME=@
```
- NAME=@ — для корневого домена (example.com),
- NAME=www — для поддомена (www.example.com).

> Предположительно для корневого домена нужно исправить определение current_ip в main.py 

### Получение YANDEX_OAUTH_TOKEN

Инструкция: https://yandex.ru/dev/id/doc/ru/register-client

Интерфейс для приложения: https://oauth.yandex.ru/

### Получение ORG_ID

На странице управления организацией выберите актуальную: https://admin.yandex.ru/domains/. ORG_ID в левом меню внизу (ID) или на странице в кнопке "Профиль организации" (ID).

### Получение RECORD_ID

> Использовать ранее полученные YANDEX_OAUTH_TOKEN и ORG_ID, DOMAIN (в скрипте  использовать родительский домен, добавленный в организацию). 

Инструкция: https://yandex.ru/dev/api360/doc/ru/ref/DomainDNSService/DomainDNSService_List 

Шаблон:
```bash
curl -H "Authorization: OAuth <YANDEX_OAUTH_TOKEN>" \
  "https://api360.yandex.net/directory/v1/org/<ORG_ID>/domains/<DOMAIN>/dns"
  ```

Пример с "реальными" данными: 

  ```bash
# Пример с подставленными значениями (ДЛЯ ПОНИМАНИЯ ФОРМАТА)
curl -H "Authorization: OAuth y0_AgAAA..." \
  "https://api360.yandex.net/directory/v1/org/12345678/domains/example.com/dns"
  ```
> Вывод JSON может быть многостраничным, используйте указание на нужную страницу для вашего поддмена.