import os

from dotenv import load_dotenv

load_dotenv(override=True)

if os.getenv("IS_LOCAL").lower() == "true":
    os.environ["CELERY_BROKER_URL"] = os.getenv("CELERY_BROKER_URL_LOCAL")
    os.environ["POSTGRES_HOST"] = "localhost"


