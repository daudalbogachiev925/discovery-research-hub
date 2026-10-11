from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@db:5432/discovery"
    EMBED_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    N_CLUSTERS: int = 8

    class Config:
        env_file = ".env"

settings = Settings()
