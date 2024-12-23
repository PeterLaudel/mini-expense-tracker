import os

from dotenv import load_dotenv

load_dotenv(f".env.{os.environ['ENV']}")
load_dotenv(f".env.{os.environ['ENV']}.local", override=True)


def postgres_url() -> str:
    return os.environ["POSTGRES_URL"]


def environment() -> str:
    return os.environ["ENVIRONMENT"]
