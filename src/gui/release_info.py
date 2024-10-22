import streamlit as st


def main() -> None:
    st.write("## release information")

    st.write("#### Updates")
    st.write("2024/10/22: 授業資料を新しいものから見れるようにしました")
    st.write("")

    st.write("<br>", unsafe_allow_html=True)

    st.write("#### planning for updates")
    st.write("PandAのログインスキップ")
    st.write("授業ごとに授業資料を見れるようにする")
    st.write("課題が提出期限の早いものから表示")
    st.write("課題の取得時間を書きたい")
    st.write("")

    return


if __name__ == "__main__":
    main()
