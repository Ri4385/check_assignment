import streamlit as st

debug = st.secrets["a"]["debug"]
login_url = st.secrets["a"]["login_url"]


print(debug, login_url)
