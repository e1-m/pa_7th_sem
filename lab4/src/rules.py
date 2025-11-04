from pydantic_settings import BaseSettings


class Rules(BaseSettings):
    MAX_USERNAME_LENGTH: int = 50
    MIN_USERNAME_LENGTH: int = 3
    MIN_PASSWORD_LENGTH: int = 8
    MAX_PRODUCT_TITLE_LENGTH: int = 30
    MAX_PRODUCT_DESCRIPTION_LENGTH: int = 1000


rules = Rules()
