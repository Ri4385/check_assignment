import streamlit as st

updates: list[str] = [
    "2024/10/22: 授業資料を新しいものから見れるようにしました。",
    "2024/10/23: 未提出の課題が提出期限の早いものから表示されるようにしました。",
    "2024/10/24: 課題の添付ファイルを見れるようにしました。",
    "2024/10/24: 授業ごとに授業資料を見れるようにしました。",
]

planning_for_updates: list[str] = [
    "PandAのログインスキップ",
    "課題の取得時間を書きたい",
    "新しい順に課題を取得する際、フォルダの中のファイルも取得できるようにする",
]


def main() -> None:
    st.write("## release information")

    st.write("#### Updates")
    for ele in updates:
        st.write(ele)
    st.write("")

    st.write("<br>", unsafe_allow_html=True)

    st.write("#### planning for updates")
    for ele in planning_for_updates:
        st.write(ele)

    return


if __name__ == "__main__":
    main()
