from pydantic import BaseModel
from typing import List, Optional  # ← Add Optional here

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

class CourseState(BaseModel):
    course_title: str = ""
    course_subtitle: str = ""
    description_points: List[str] = []
    target_audience: str = ""
    course_goal: str = ""
    curriculum: Optional[Curriculum] = None  # ✅ Now accepts None