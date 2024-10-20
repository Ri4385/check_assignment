import requests
import json

from bs4 import BeautifulSoup

from api.model import Assignments
from api.model import Assignment
from api.model import Course


def get_all_assignmtnts(session: requests.Session) -> Assignments:
    
    url = "https://panda.ecs.kyoto-u.ac.jp/direct/assignment/my.json"

    json_data = session.get(url).json()

    
    # with open("data/assignments.json", "w", encoding="utf-8") as file:
    #     json.dump(json_data,file,indent=2,ensure_ascii=False)

    data: Assignments = Assignments(**json_data)
    return data

def get_cources(session: requests.Session) -> list[Course]:
    courses_url = "https://panda.ecs.kyoto-u.ac.jp/portal"

    courses: list[Course] = []
    data_response = session.get(courses_url)
    soup = BeautifulSoup(data_response.text, 'html.parser')

    # fav-titleクラスのaタグを全て取得
    for div in soup.find_all('div', class_='fav-title'):
        link = div.find('a')
        if link:
            href = link.get('href')
            title = link.get('title')
            course = Course(title=title, url=href)
            courses.append(course)
    return courses

def get_assignments(session: requests.Session, id: str) -> Assignments|None:
    assignment_url = f"https://panda.ecs.kyoto-u.ac.jp/direct/assignment/site/{id}.json"

    try:
        json_data = session.get(assignment_url).json()
        assignments = Assignments(**json_data)
        return assignments
    except Exception as e:
        print(f"no assignments foud {e}")
        return None


if __name__ == '__main__':
    
    with open("data/assignments.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
    assignments = Assignments(**json_data)

    assignments.assignment_collection[0]
    pass