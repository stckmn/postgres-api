from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Docker will setup the environment variables
# No need to specify the .env file

class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    # project settings
    VERSION: str = Field("0.0.1")
    PROJECT_NAME: str = Field("Base FastAPI with Postgresql project")

    # postgres settings
    POSTGRES_DRIVERNAME: str = "postgresql"
    POSTGRES_DBNAME: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int | str = "5432"
    POSTGRES_ECHO: bool = False        # because we will use python logging
    POSTGRES_POOL_SIZE: int = 5
    POSTGRES_POOL_RECYCLE: int = -1


settings = Settings()
    
