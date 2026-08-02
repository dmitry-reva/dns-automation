import os
from dotenv import load_dotenv

load_dotenv()

YANDEX_OAUTH_TOKEN = os.getenv("YANDEX_OAUTH_TOKEN")
ORG_ID = os.getenv("ORG_ID")
DOMAIN = os.getenv("DOMAIN")
RECORD_ID = os.getenv("RECORD_ID")
TTL = int(os.getenv("TTL", "3600"))
NAME = os.getenv("NAME", "@")

if not all([YANDEX_OAUTH_TOKEN, ORG_ID, DOMAIN, RECORD_ID]):
    raise ValueError("Не все обязательные переменные заданы в .env")
