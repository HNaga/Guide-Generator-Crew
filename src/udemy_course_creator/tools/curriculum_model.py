from pydantic import BaseModel
from typing import List

class Lecture(BaseModel):
    title: str
    objective: str
    activity: str

class Section(BaseModel):
    title: str
    lectures: List[Lecture]

class Curriculum(BaseModel):
    title: str
    sections: List[Section]