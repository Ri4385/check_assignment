import time
from datetime import datetime
import pytz

import streamlit as st
from pydantic import BaseModel

from api import client
from api.model import Course
from api.model import Attachment
from api.model import SubmittedAttachment

from gui.util import skip_request, get_year_and_semester


class AssignmentCard(BaseModel):
    title: str
    instructions: str
    duetime: str
    url: str
    is_submitted: bool
    due: bool
    closetime: str
    attachments: list[Attachment]
    submitted_attachments: list[SubmittedAttachment]

    @property
    def remaining_time(self) -> str:
        date_string = self.duetime.split(" (")[0]  # '(火)'を削除
        date_format = "%Y/%m/%d %H:%M"

        target_date = datetime.strptime(date_string, date_format)
        japan_tz = pytz.timezone("Asia/Tokyo")
        target_date = japan_tz.localize(datetime.strptime(date_string, date_format))
        now = datetime.now(japan_tz)
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
        card += f"<h5>{self.title}</h6>"
        card += f"<p>提出期限 : {self.duetime}</p>"
        if self.remaining_time[0] == "-":
            card += f"<p>{self.remaining_time[1:]}経過</p>"
        else:
            card += f"<p>あと{self.remaining_time}</p>"
        card += f"<p>遅延提出期限 : {self.closetime}</p>"
        card += f'<a href="{self.url}" target="_blank">提出する</a>'
        if self.attachments:
            card += f'<p>添付ファイル: <a href="{self.attachments[0].url}" target="_blank">{self.attachments[0].name}</a></p>'
        if self.is_submitted:
            card += "<p>提出済み"
            if self.submitted_attachments[0].name and self.submitted_attachments[0].url:
                card += f': <a href="{self.submitted_attachments[0].url}" target="_blank">{self.submitted_attachments[0].name}</a>'
            card += "</p>"
        else:
            card += "<h6>未提出</h6>"
        card += "<p>説明</p>"
        card += self.instructions
        card += "</div>"

        st.markdown(card, unsafe_allow_html=True)
        return


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
                attachments = assignment.attachments
                instructions = assignment.instructions
                submitted_attachments = assignment.get_submitted_attachments()
                if assignment.status == "DUE":
                    due = True
                else:
                    due = False

                card: AssignmentCard = AssignmentCard(
                    title=title,
                    instructions=instructions,
                    duetime=duetime,
                    url=url,
                    is_submitted=is_submitted,
                    due=due,
                    closetime=closetime,
                    attachments=attachments,
                    submitted_attachments=submitted_attachments,
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
