import streamlit as st
from api import login
from api import client
from api.model import Assignments

# Streamlitのタイトル
st.title("Assignments Viewer")


# ユーザー名とパスワードの入力フィールド
username = st.text_input("Username", type="default")
password = st.text_input("Password", type="password")

if st.button("Login and check assignments"):
    if username and password:
        session = login.login_with_password(username=username, password=password)
        st.success("Logged in successfully!")
        data: Assignments = client.get_assignmtnts(session=session)
    
        # 課題のリストを表示
        if data.assignment_collection:
            for ele in data.assignment_collection:
                if ele.status == "DUE":
                    continue
                try:
                    title = ele.get_title(session=st.session_state.session)
                    duetime = ele.get_duetime()
                    st.write(f"**Title:** {title}, **Due Time:** {duetime}")
                except Exception as e:
                    st.error(f"Error retrieving data for assignment: {e}")
    else:
        st.warning("Please enter both username and password.")

