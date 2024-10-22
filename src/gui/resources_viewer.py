from datetime import datetime
import time

import streamlit as st
from pydantic import BaseModel

from api import client
from api.model import Course
from api.model import Resource


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

    start = time.perf_counter()

    if st.button("Get Resources"):
        courses: list[Course] = client.get_cources(session=st.session_state.session)

        year, semester = get_year_and_semester()

        resource_cards: list[ResourceCard] = []
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

        resource_cards.sort(key=lambda res: -res.modified)

        for resource_card in resource_cards:
            resource_card.display()

        st.write(time.perf_counter() - start, "s")

        # resources.sort(key=lambda res: -res.modified)
        # for res in resources:
        #     st.write(res.name, res.modified)
        #     st.write(res.url)
    return


if __name__ == "__main__":
    main()
