import requests
import json
from api.model import Assignments


def get_assignmtnts(session: requests.Session) -> Assignments:
    
    url = "https://panda.ecs.kyoto-u.ac.jp/direct/assignment/my.json"

    json_data = session.get(url).json()

    
    # with open("data/assignments.json", "w", encoding="utf-8") as file:
    #     json.dump(json_data,file,indent=2,ensure_ascii=False)

    data: Assignments = Assignments(**json_data)
    return data


if __name__ == '__main__':
    
    with open("data/assignments.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
    assignments = Assignments(**json_data)

    assignments.assignment_collection[0]
    pass