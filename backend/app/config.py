from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Acepta variables extra en .env sin fallar
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:5173"  # CSV
    energia_base: str = "https://energia.serviciosmin.gob.es/ServiciosRestCarburantes/PreciosCarburantes"

    def cors_list(self):
        return [s.strip() for s in self.cors_origins.split(",") if s.strip()]

settings = Settings()
