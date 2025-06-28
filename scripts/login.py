import streamlit as st


def main():
    st.title("Login Form")

    # フォーム作成
    with st.form("login_form"):
        # 入力フィールド
        username = st.text_input(
            "Username",
        )
        password = st.text_input(
            "Password", type="password", autocomplete="current-password"
        )

        # ボタン
        submitted = st.form_submit_button("Login")

        if submitted:
            # オートコンプリートの値を強制的にセッションに反映
            st.write(f"Username: {username}")
            st.write(f"Password: {password}")


if __name__ == "__main__":
    main()
