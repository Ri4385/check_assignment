from pydantic_settings import BaseSettings
import streamlit as st


class Settings(BaseSettings):
    debug: bool
    login_url: str


setting = Settings(**st.secrets)

if __name__ == "__main__":
    print(setting)
