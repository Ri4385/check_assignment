from typing import List, Optional, Dict, Any, Union
import json
import requests
from datetime import datetime, timedelta

from pydantic import BaseModel, Field
from bs4 import BeautifulSoup



class CloseTime(BaseModel):
    epochSecond: int
    nano: int

class DropDeadTime(BaseModel):
    epochSecond: int
    nano: int

class DueTime(BaseModel):
    epochSecond: int
    nano: int

class OpenTime(BaseModel):
    epochSecond: int
    nano: int

class TimeCreated(BaseModel):
    epochSecond: int
    nano: int

class TimeLastModified(BaseModel):
    epochSecond: int
    nano: int

class Submitter(BaseModel):
    displayId: str
    displayName: str
    grade: str
    id: str
    sortName: str
    timeSpent: Optional[Any]
    overridden: bool

class SubmittedAttachment(BaseModel):
    name: str
    ref: str
    size: int
    type: str
    url: str

class Submission(BaseModel):
    assignmentCloseTime: CloseTime
    dateSubmitted: str
    dateSubmittedEpochSeconds: int
    feedbackAttachments: List[Any]
    feedbackComment: Optional[str]
    feedbackText: Optional[str]
    gradableId: str
    grade: str
    graded: bool
    groupId: Optional[str]
    id: str
    late: Optional[bool]
    ltiSubmissionLaunch: Optional[Any]
    previewableAttachments: Dict[str, Any]
    privateNotes: Optional[Any]
    returned: bool
    status: str
    submitted: bool
    submittedAttachments: List[SubmittedAttachment]
    submittedText: Optional[str]
    submitters: List[Submitter]
    userSubmission: bool
    canSubmit: bool
    draft: bool
    visible: bool

class Assignment(BaseModel):
    access: str
    allPurposeItemText: Optional[str]
    allowPeerAssessment: bool
    attachments: List[Dict[str, Any]]
    author: str
    authorLastModified: str
    closeTime: CloseTime
    closeTimeString: str
    content: Optional[str]
    context: str
    creator: Optional[str]
    dropDeadTime: DropDeadTime
    dropDeadTimeString: str
    dueTime: DueTime
    dueTimeString: str
    estimate: str
    estimateRequired: bool
    gradeScale: str
    gradeScaleMaxPoints: Optional[str]
    gradebookItemId: Optional[int|str]  # Optionalにし、両方の型を受け入れる
    gradebookItemName: Optional[str]
    groups: List[Any]
    id: str
    instructions: str
    ltiGradableLaunch: Optional[Any]
    maxGradePoint: Optional[str]
    modelAnswerText: Optional[str]
    openTime: OpenTime
    openTimeString: str
    position: int
    privateNoteText: Optional[str]
    section: str
    status: str
    submissionType: str
    submissions: Optional[List[Submission]] = []  # Optionalにし、デフォルト値を空リストに
    timeCreated: TimeCreated
    timeLastModified: TimeLastModified
    title: str
    allowResubmission: bool
    anonymousGrading: bool
    draft: bool
    entityReference: str
    entityURL: str
    entityId: str
    entityTitle: str

    def get_title(self, session: requests.Session) -> str:
        """この関数は非推奨です"""

        target_url = f"https://panda.ecs.kyoto-u.ac.jp/portal/site/{self.context}"
        response = session.get(target_url)

        # BeautifulSoupでタイトルを取得
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title:str = soup.title.string
        if title.startswith("PandA :"):
            title = title.replace("PandA :", "")
        if title.endswith(": 概要"):
            title = title.replace(": 概要", "")
        if " " in title:
            title = title.replace(" ", "")
        return title
    
    @staticmethod
    def convert_UTC_to_JST(timestring: str) -> str:
        # 文字列をdatetimeオブジェクトに変換
        date_object = datetime.fromisoformat(timestring.replace("Z", "+00:00"))

        # 日本時間に変換（UTC+9）
        japan_time = date_object + timedelta(hours=9)

        # 曜日を取得し、省略形に変換
        weekdays = ["月", "火", "水", "木", "金", "土", "日"]
        weekday_short = weekdays[japan_time.weekday()]

        # フォーマットして曜日を追加
        formatted_date = japan_time.strftime(f"%Y/%m/%d %H:%M ({weekday_short})")
        return formatted_date
    
    def get_duetime(self) -> str:
        duetime = self.convert_UTC_to_JST(self.dueTimeString)
        return duetime
    
    def get_closetime(self) -> str:
        closetime = self.convert_UTC_to_JST(self.closeTimeString)
        return closetime
    
    def is_submitted(self) -> bool:
        if not self.submissions:
            return False
        if self.submissions[0].status[:4] == "提出済み":
            return True
        else:
            return False
        
    def get_assignment_url(self) -> str:
        url = f"https://panda.ecs.kyoto-u.ac.jp/portal/site/{self.context}/tool/{self.entityId}"
        return url
    
    def get_assignment_direct_url(self) -> str:
        return self.entityURL

class Assignments(BaseModel):
    entityPrefix: str
    assignment_collection: List[Assignment]

class Course(BaseModel):
    title: str
    url: str

    @property
    def id(self) -> str:
        return self.url.rsplit('/', 1)[-1]
    
class Resource(BaseModel):
    created: int #1727684127863
    creator: str #"9f2f3d86-1ef9-4c71-b39e-160827506e6a"
    description: str|None #null
    hidden: bool #false
    mimeType: str|None #null
    modified: int #1727684127889
    modifiedBy: str #"9f2f3d86-1ef9-4c71-b39e-160827506e6a"
    name: str #"[2024後期木１]化学工学数学Ｉ（化学工学）"
    priority: str|int #"45008"
    # properties: list #{}
    reference: str #"/content/group/2024-110-7302-000/"
    resourceChildren: list #[…]
    resourceId: str	#"/group/2024-110-7302-000/"
    size: int|str|None #null
    type_: str = Field(..., alias="type") #"org.sakaiproject.content.types.folder"
    url: str #"https://panda.ecs.kyoto-u.ac.jp/access/content/group/2024-110-7302-000/"
    # entityReference: str #"/content"
    # entityURL: str #"https://panda.ecs.kyoto-u.ac.jp/direct/content"

# class Resource(BaseModel):
#     title: str
#     url: str
    
        

if __name__ == "__main__":

    with open("data/assignments.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
    assigntments = Assignments(**json_data)

    for assignment in assigntments.assignment_collection:
        duetime = assignment.get_duetime()
        is_submitted = assignment.is_submitted()
        url = assignment.get_assignment_url()
        direct_url = assignment.get_assignment_direct_url()

        print(duetime)
        print(is_submitted)
        print(url)
        print(direct_url)
