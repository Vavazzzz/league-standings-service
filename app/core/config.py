from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Standings Service"
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
