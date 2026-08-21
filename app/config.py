from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):   # O BaseModel do Pydantic, mas voltado para configurações.
    database_url: str
    biblioteca_json: str         # Para acessar agora é assim: settings.biblioteca_json

    model_config = SettingsConfigDict(
        env_file=".env"
    )

settings = Settings()