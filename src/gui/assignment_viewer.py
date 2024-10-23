import time
from datetime import datetime
import pytz

import streamlit as st
from pydantic import BaseModel

from api import client
from api.model import Course


class AssignmentCard(BaseModel):
    title: str
    duetime: str
    url: str
    is_submitted: bool
    due: bool
    closetime: str

    @property
    def remaining_time(self) -> str:
        date_string = self.duetime.split(" (")[0]  # '(火)'を削除
        date_format = "%Y/%m/%d %H:%M"

        # 日付文字列を解析
        target_date = datetime.strptime(date_string, date_format)

        # タイムゾーンを日本時間に設定
        japan_tz = pytz.timezone("Asia/Tokyo")

        # 日付文字列を解析し、タイムゾーンを付与
        target_date = japan_tz.localize(datetime.strptime(date_string, date_format))

        # 現在の日付を日本時間で取得
        now = datetime.now(japan_tz)

        # 日付の差を計算
        time_difference = abs(target_date - now)

        # 日数、時間、分を取得
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes = remainder // 60

        remaining = ""
        if now > target_date:
            remaining += "-"

        remaining += f"{days}日{hours}時間{minutes}分"

        return remaining

    def display(self) -> None:
        card = ""
        card += '<div style="border: 1px solid #ccc; border-radius: 15px; padding: 10px; margin: 10px;">'
        card += f"<h6>{self.title}</h6>"
        card += f"<p>提出期限 : {self.duetime}</p>"
        if self.remaining_time[0] == "-":
            card += f"<p>{self.remaining_time[1:]}経過</p>"
        else:
            card += f"<p>あと{self.remaining_time}</p>"
        card += f"<p>遅延提出期限 : {self.closetime}</p>"
        card += f'<a href="{self.url}" target="_blank">提出する</a>'
        card += f'<p>{"提出済み" if self.is_submitted else "未提出"}</p>'
        card += "</div>"

        st.markdown(card, unsafe_allow_html=True)
        return


def get_year_and_semester() -> tuple[str, str]:
    current_date = datetime.now()
    year_int: int = current_date.year
    if current_date.month < 4:
        year_int -= 1
    year: str = str(year_int)
    if 4 <= current_date.month < 9:
        semester = "前期"
    else:
        semester = "後期"
    return year, semester


def skip_request(course: Course, year: str, semester: str) -> bool:
    if course.title == "Home":
        print(f"{course.title}skipped")
        return True
    if course.title[1:5] != year:
        print(f"{course.title}skipped")
        return True
    if course.title[5:7] != semester:
        print(f"{course.title}skipped")
        return True
    return False


def main() -> None:
    # Streamlitのタイトル
    st.write("## Assignments Viewer")

    # 課題を取得するボタン
    if st.session_state.logged_in and st.button("Get Assignments"):
        start_time = time.perf_counter()

        courses: list[Course] = client.get_cources(session=st.session_state.session)
        not_submitted_cards: list[AssignmentCard] = []
        submitted_cards: list[AssignmentCard] = []

        year, semester = get_year_and_semester()

        for course in courses:
            id: str = course.id

            if skip_request(course=course, year=year, semester=semester):
                continue

            assignments = client.get_assignments(
                session=st.session_state.session, id=id
            )
            if not assignments:
                continue
            if not assignments.assignment_collection:
                continue

            for assignment in assignments.assignment_collection:
                title = course.title
                duetime = assignment.get_duetime()
                url = assignment.get_assignment_url()
                is_submitted = assignment.is_submitted()
                closetime = assignment.get_closetime()
                if assignment.status == "DUE":
                    due = True
                else:
                    due = False

                card: AssignmentCard = AssignmentCard(
                    title=title,
                    duetime=duetime,
                    url=url,
                    is_submitted=is_submitted,
                    due=due,
                    closetime=closetime,
                )
                if card.is_submitted:
                    submitted_cards.append(card)
                else:
                    not_submitted_cards.append(card)

        st.write("遅延提出期限は予測段階です。正しいとは限りません。")
        not_submitted_cards.sort(key=lambda card: card.duetime.split(" (")[0])

        # 課題のリストを表示

        st.write("### 未提出の課題")
        if not_submitted_cards:
            for card in not_submitted_cards:
                card.display()
        else:
            st.info("No assignments found.")

        st.write("<br><br>", unsafe_allow_html=True)
        st.write("### 提出済みの課題")
        if submitted_cards:
            for card in submitted_cards:
                card.display()
        else:
            st.info("No assignments found.")

        st.write(f"api time: {(time.perf_counter() - start_time):.02f}s")


if __name__ == "__main__":
    main()
