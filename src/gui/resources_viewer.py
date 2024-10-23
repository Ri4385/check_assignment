from datetime import datetime
import time

import streamlit as st
from pydantic import BaseModel

from api import client
from api.model import Course
from api.model import ResourceSCR


class ResourceCard(BaseModel):
    title: str
    name: str
    modified: int
    url: str

    def display(self) -> None:
        card = ""
        card += '<div style="border: 1px solid #ccc; border-radius: 15px; padding: 10px; margin: 10px;">'
        card += f"<h6>{self.title}</h6>"
        card += f'<a href="{self.url}" target="_blank">{self.name}</a>'
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
    st.write("## Resources Viewer")

    resource_cards: list[ResourceCard] = []

    if st.button("Get Resources Newest First"):
        courses: list[Course] = client.get_cources(session=st.session_state.session)

        year, semester = get_year_and_semester()

        for course in courses:
            if skip_request(course=course, year=year, semester=semester):
                continue
            resources = client.get_resources_by_api(
                session=st.session_state.session, id=course.id
            )

            for resource in resources:
                resource_card = ResourceCard(
                    title=course.title,
                    name=resource.name,
                    url=resource.url,
                    modified=resource.modified,
                )
                resource_cards.append(resource_card)

    if st.button("Get Resources By Course"):
        courses: list[Course] = client.get_cources(session=st.session_state.session)
        year, semester = get_year_and_semester()

        for course in courses:
            if skip_request(course=course, year=year, semester=semester):
                continue
            resouces_SCP: list[ResourceSCR] = client.get_resources_by_scraping_access(
                session=st.session_state.session, id=course.id
            )

            with st.expander(course.title):
                for res_SCR in resouces_SCP:
                    st.write(
                        f'<a href="{res_SCR.url}" target="_blank">{res_SCR.title}</a>',
                        unsafe_allow_html=True,
                    )

    if resource_cards:
        # rsourcesを表示
        resource_cards.sort(key=lambda res: -res.modified)
        st.write("フォルダの中にあるファイルは表示されていません。")

        for resource_card in resource_cards:
            resource_card.display()
    return


if __name__ == "__main__":
    main()
