from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # debug: bool
    # username: str
    # password: str
    login_url: str

    class Config:
        env_file = ".env"


setting = Settings()  # pyright: ignore

if __name__ == "__main__":
    print(setting)
