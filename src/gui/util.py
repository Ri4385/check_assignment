from datetime import datetime
from api.model import Course


def get_year_and_semester() -> tuple[str, str]:
    """
    Returns:
        (year, semester)
    """
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
