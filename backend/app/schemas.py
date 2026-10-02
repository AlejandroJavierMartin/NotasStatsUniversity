from pydantic import BaseModel
from typing import Optional, List


class GroupCreate(BaseModel):
    name: str
    academic_year: str
    degree: str
    description: Optional[str] = None


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    academic_year: Optional[str] = None
    degree: Optional[str] = None
    description: Optional[str] = None


class GroupRead(BaseModel):
    id: int
    name: str
    academic_year: str
    degree: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class StudentCreate(BaseModel):
    name: str
    surname: str
    carnet: str
    email: Optional[str] = None
    group_id: int


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    carnet: Optional[str] = None
    email: Optional[str] = None
    group_id: Optional[int] = None


class StudentRead(BaseModel):
    id: int
    name: str
    surname: str
    carnet: str
    email: Optional[str] = None
    group_id: int

    class Config:
        orm_mode = True


class SubjectCreate(BaseModel):
    name: str
    code: str
    credits: Optional[int] = None
    group_id: int
    description: Optional[str] = None


class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    group_id: Optional[int] = None
    description: Optional[str] = None


class SubjectRead(BaseModel):
    id: int
    name: str
    code: str
    credits: Optional[int] = None
    group_id: int
    description: Optional[str] = None

    class Config:
        orm_mode = True


class GradeCreate(BaseModel):
    student_id: int
    subject_id: int
    grade: float
    status: str = "pending"
    evaluation_type: Optional[str] = None
    academic_year: str
    notes: Optional[str] = None


class GradeUpdate(BaseModel):
    student_id: Optional[int] = None
    subject_id: Optional[int] = None
    grade: Optional[float] = None
    status: Optional[str] = None
    evaluation_type: Optional[str] = None
    academic_year: Optional[str] = None
    notes: Optional[str] = None


class GradeRead(BaseModel):
    id: int
    student_id: int
    subject_id: int
    grade: float
    status: str
    evaluation_type: Optional[str] = None
    academic_year: str
    notes: Optional[str] = None

    class Config:
        orm_mode = True


class DashboardStats(BaseModel):
    total_students: int
    total_groups: int
    total_subjects: int
    total_grades: int
    average_grade: float
    approved: int
    failed: int
    pending: int
