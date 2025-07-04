import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = "HS256"
