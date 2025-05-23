import os

from dotenv import load_dotenv

load_dotenv(override=True)

if os.getenv("IS_LOCAL").lower() == "true":
    os.environ["CELERY_BROKER_URL"] = os.getenv("CELERY_BROKER_URL_LOCAL")
else:
    os.environ["POSTGRES_HOST"] = "hrf_universe_postgres"

print(
    f'{os.getenv("POSTGRES_DRIVER")}://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:5432/{os.getenv("POSTGRES_DB")}'
)
# print(os.getenv("CELERY_BROKER_URL"))
