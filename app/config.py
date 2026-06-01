from pydantic_settings import BaseSettings

#Pydantic schema for checking environmental variables
class Settings(BaseSettings):
    database_hostname: str
    database_port: str 
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    #a bit old, there is newer way, read documentation
    class Config:
        env_file = ".env"

settings: Settings = Settings() # type: ignore
