from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


# The pydantic BaseSettings model lets you define settings
# that can have default values and values defined in .env
# will override them
class Settings(BaseSettings):
    KAFKA_SERVICE_URI: str
    KAFKA_CLIENT_ID: str
    USER_ANALYTICS_KAFKA_TOPIC: str

    class Config:
        case_sensitive = True


settings = Settings()
