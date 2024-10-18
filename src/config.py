from pydantic_settings import BaseSettings
import streamlit as st

class Settings(BaseSettings):
    # debug: bool
    # username: str
    # password: str
    login_url: str = st.secrets['.env']['LOGIN_URL']

    # class Config:
    #     # env_file = ".env"
    #     env_file = ".env"


setting = Settings()  # pyright: ignore

if __name__ == "__main__":
    print(setting)
