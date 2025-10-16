import os
from functools import lru_cache
class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "production")
    GAS_API_URL: str = os.getenv("GAS_API_URL", "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/")
    DB_USER: str = os.getenv("POSTGRES_USER","postgres")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD","postgres")
    DB_HOST: str = os.getenv("POSTGRES_HOST","127.0.0.1")
    DB_PORT: str = os.getenv("POSTGRES_PORT","5432")
    DB_NAME: str = os.getenv("POSTGRES_DB","gasolineras")
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
@lru_cache
def get_settings() -> Settings: return Settings()
