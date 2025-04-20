from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    
    def get_auth_data():
        return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()