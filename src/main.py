import streamlit as st
from api import login
from api import client
from api.model import Assignments

# Streamlitのタイトル
st.title("Assignments Viewer")

# ログインセクション
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # ユーザー名とパスワードの入力フィールド
    username = st.text_input("Username", type="default")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            session = login.login_with_password(username=username, password=password)
            st.session_state.session = session  # セッションを保存
            st.session_state.logged_in = True  # ログイン状態を更新
            st.success("Logged in successfully!")
        else:
            st.warning("Please enter both username and password.")
else:
    st.success("You are already logged in.")

# 課題を取得するボタン
if st.session_state.logged_in and st.button("Get Assignments"):
    data: Assignments = client.get_assignmtnts(session=st.session_state.session)
    
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
        st.info("No assignments found.")
