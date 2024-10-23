import requests
import json
import urllib
from bs4 import BeautifulSoup

from api.model import Assignments
from api.model import Course
from api.model import Resource
from api.model import ResourceSCR


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
    soup = BeautifulSoup(data_response.text, "html.parser")

    # fav-titleクラスのaタグを全て取得
    for div in soup.find_all("div", class_="fav-title"):
        link = div.find("a")
        if link:
            href = link.get("href")
            title = link.get("title")
            course = Course(title=title, url=href)
            courses.append(course)
    return courses


def get_assignments(session: requests.Session, id: str) -> Assignments | None:
    assignment_url = f"https://panda.ecs.kyoto-u.ac.jp/direct/assignment/site/{id}.json"

    try:
        json_data = session.get(assignment_url).json()
        assignments = Assignments(**json_data)
        return assignments
    except Exception as e:
        print(f"no assignments foud {e}")
        return None


def get_resources_by_api(session: requests.Session, id: str) -> list[Resource]:
    resource_url = f"https://panda.ecs.kyoto-u.ac.jp/direct/content/resources/{id}.json"

    json_data = session.get(resource_url).json()
    resources: list[Resource] = []

    if len(json_data["content_collection"]) > 1:
        raise NotImplementedError()

    print("api start")
    resource: Resource = Resource(**json_data["content_collection"][0])

    if resource.resourceChildren:
        for resource_child in resource.resourceChildren:
            resource_child = Resource(**resource_child)
            resources.append(resource_child)
            # if resource_child.type_  == "org.sakaiproject.content.types.folder":
            #     #id はresourceId /group/2024-110-7407-000/第1回（10月4日）/からgroup/, /を除いたもの
            #     id_ = resource_child.resourceId.replace("/group/", "")
            #     if id_.endswith("/"):
            #         id_ = id_[:-1]
            #     resources_ : list[Resource] = get_resources_by_api(session=session, id=id_)
            #     resources.extend(resources_)
            # elif resource_child.type_ == "org.sakaiproject.content.types.fileUpload":
            #     resources.append(resource_child)
            # else:
            #     raise NotImplementedError()

        resource.resourceChildren = []

    return resources


def get_resources_by_scraping_access(
    session: requests.Session, id: str, directory: str | None = None
) -> list[ResourceSCR]:
    resource_url = f"https://panda.ecs.kyoto-u.ac.jp/access/content/group/{id}"

    resources: list[ResourceSCR] = []

    response = session.get(resource_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # liタグのaタグを探す
    li_tags = soup.find_all("li")
    for li in li_tags:
        a_tag = li.find("a")
        if a_tag:
            url = a_tag["href"]
            # 相対パスを絶対パスに変換
            if not url.startswith("http"):
                absolute_url = urllib.parse.urljoin(resource_url, url)

            # liタグのクラス名とaタグのテキストを取得
            li_class = li.get("class")[0]
            title = a_tag.get_text(strip=True)

            if directory:
                title = directory + "/" + title

            if li_class == "folder":
                resources_ = get_resources_by_scraping_access(
                    session=session, id=f"{id}/{url}", directory=title
                )
                resources.extend(resources_)
            elif li_class == "file":
                resource: ResourceSCR = ResourceSCR(title=title, url=absolute_url)
                resources.append(resource)

    return resources


def get_resources_by_scraping(session: requests.Session, id: str) -> list[Resource]:
    resource_url = f"https://panda.ecs.kyoto-u.ac.jp/portal/site/{id}"
    response = session.get(resource_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # navタグを取得
    nav = soup.find("nav", class_="Mrphs-toolsNav__menu")
    if nav:
        # liタグのaタグを探す
        for li in nav.find_all("li"):
            a_tag = li.find("a")
            if a_tag and a_tag["title"].startswith("授業資料"):
                href = a_tag["href"]

                # 指定されたリンクにアクセス
                new_response = session.get(href)
                new_soup = BeautifulSoup(new_response.content, "html.parser")

                # tdタグのクラス名が"specialLink"のものを取得
                special_links = new_soup.find_all("tr")
                for link in special_links:
                    print(link)  # リンクのテキストを表示
    return resources


if __name__ == "__main__":
    # with open("data/assignments.json", "r", encoding="utf-8") as file:
    #     json_data = json.load(file)
    # assignments = Assignments(**json_data)

    # assignments.assignment_collection[0]
    # pass
    import login

    session = login.login_with_password("a0233232", "Nagauchi0408")
    resources = get_resources(session, id="2024-110-7302-000")

    for resource in resources:
        print(resource.name)
