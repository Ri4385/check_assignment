import time

import streamlit as st

from api import login
from gui import assignment_viewer
from gui import resources_viewer
from gui import release_info


def main() -> None:
    st.set_page_config(
        page_title="PandA for the Lazy",
        layout="wide",
    )

    # Streamlitのタイトル
    st.title("PandA for the Lazy")

    # ログインセクション
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        # ユーザー名とパスワードの入力フィールド
        username = st.text_input("Username", type="default")
        password = st.text_input(
            "Password", autocomplete="current-password", type="password"
        )

        if st.button("Login"):
            # if username:
            session = login.login_with_password(username=username, password=password)
            st.session_state.session = session  # セッションを保存
            st.session_state.logged_in = True  # ログイン状態を更新
            st.success("Logged in successfully!")
            time.sleep(0.8)
            st.rerun()
            # else:
            #     st.warning("Please enter both username and password.")
    else:
        tab_assignment, tab_resources, tab_releases = st.tabs(
            ["assignments", "resources", "releases"]
        )

        with tab_assignment:
            assignment_viewer.main()
        with tab_resources:
            resources_viewer.main()
        with tab_releases:
            release_info.main()


if __name__ == "__main__":
    main()
