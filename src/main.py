import streamlit as st
from pydantic import BaseModel
import time
from datetime import datetime

from api import login
from api import client
from api.model import Assignments
from api.model import Assignment
from api.model import Course


class AssignmentCard(BaseModel):
    title: str
    duetime: str
    url: str
    is_submitted: bool

    def card(self) -> None:
        st.markdown(
                f"""
                <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; margin: 10px;">
                    <h6>{self.title}</h6>
                    <p>提出期限: {self.duetime}</p>
                    <a href="{self.url}" target="_blank">提出する</a>
                    <p>{"提提出済み" if self.is_submitted else "未提出"}</p>
                </div>
                """
                ,unsafe_allow_html=True)
        return

def main() -> None:
    
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
        start_time = time.perf_counter()
        # data: Assignments = client.get_all_assignmtnts(session=st.session_state.session)

        # not_submitted_cards: list[AssignmentCard] = []
        # submitted_cards: list[AssignmentCard] = []

        # if data.assignment_collection:
        #     for ele in data.assignment_collection:
        #         if ele.status == "DUE":
        #             continue

        #         title = ele.get_title(session=st.session_state.session)
        #         duetime = ele.get_duetime()
        #         url = ele.get_assignment_url()
        #         is_submitted = ele.is_submitted()

        #         card = AssignmentCard(title=title, duetime=duetime, url=url, is_submitted=is_submitted)

        #         if card.is_submitted:
        #             submitted_cards.append(card)
        #         else:
        #             not_submitted_cards.append(card)
        courses: list[Course] = client.get_cources(session=st.session_state.session)
        not_submitted_cards: list[AssignmentCard] = []
        submitted_cards: list[AssignmentCard] = []

        current_date = datetime.now()
        year_int: int = current_date.year
        if current_date.month < 4:
            year_int -= 1
        year:str = str(year_int)
        if 4 <= current_date.month < 9:
            semester = "前期"
        else:
            semester = "後期"
        
        for course in courses:
            id: str = course.id
            if course.title == "Home":
                print(f"{course.title}skipped")
                continue
            if course.title[1:5] != year:
                print(f"{course.title}skipped")
                continue
            if course.title[5:7] != semester:
                print(f"{course.title}skipped")
                continue
            
            assignment = client.get_assignment(session=st.session_state.session, id=id)
            if not assignment:
                continue
            if assignment.status == "DUE":
                continue
            title = assignment.get_title(st.session_state.session)
            duetime = assignment.get_duetime()
            url = assignment.get_assignment_url()
            is_submitted = assignment.is_submitted()
            card: AssignmentCard = AssignmentCard(title=title, duetime=duetime, url=url, is_submitted=is_submitted)
            if card.is_submitted:
                submitted_cards.append(card)
            else:
                not_submitted_cards.append(card)

        
        # 課題のリストを表示

        st.write("### 未提出の課題")
        if not_submitted_cards:
            for card in not_submitted_cards:
                card.card()
        else:
            st.info("No assignments found.")

        st.write("### 提出済みの課題")
        if submitted_cards:
            for card in submitted_cards:
                card.card()
        else:
            st.info("No assignments found.")

        st.write(f"api time: {int(time.perf_counter() - start_time)}s")

def fast_main():
    session = login.login_with_password(username="a0233232", password="Nagauchi0408")

    start_time = time.perf_counter()

    courses: list[Course] = client.get_cources(session=session)
    assignment_list: list[Assignment] = []
    not_submitted_cards: list[AssignmentCard] = []
    submitted_cards: list[AssignmentCard] = []
    print(courses)
    cards = []

    current_date = datetime.now()
    year_int: int = current_date.year
    if current_date.month < 4:
        year_int -= 1
    year:str = str(year_int)
    if 4 <= current_date.month < 9:
        semester = "前期"
    else:
        semester = "後期"
    
    for course in courses:
        id: str = course.id
        if course.title == "Home":
            print(f"{course.title}skipped")
            continue
        if course.title[1:5] != year:
            print(f"{course.title}skipped")
            continue
        if course.title[5:7] != semester:
            print(f"{course.title}skipped")
            continue
        
        assignment = client.get_assignment(session=session, id=id)
        if not assignment:
            continue
        title = assignment.get_title(session)
        duetime = assignment.get_duetime()
        url = assignment.get_assignment_url()
        is_submitted = assignment.is_submitted()
        card: AssignmentCard = AssignmentCard(title=title, duetime=duetime, url=url, is_submitted=is_submitted)
        # card.card()
        cards.append(card)
    print(cards)
    print(f"api time: {float(time.perf_counter() - start_time)}s")
            


        
if __name__ == "__main__":
    main()
