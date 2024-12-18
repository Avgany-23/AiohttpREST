from datetime import timedelta
import pydantic_settings
import dotenv
import os


dotenv.load_dotenv()


class JWTConfig(pydantic_settings.BaseSettings):
    SECRET_KEY: str = '321'
    ALGORITHM: str = "HS256"
    AUTH_HEADER_TYPES: str = 'Bearer '
    ACCESS_TOKEN_LIFETIME: timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_LIFETIME: timedelta = timedelta(days=30)
    PAYLOAD: tuple = ('user_id', 'user_name', 'exp', 'refresh')


jwt_conf = JWTConfig(SECRET_KEY=os.getenv('SECRET_KEY'))
