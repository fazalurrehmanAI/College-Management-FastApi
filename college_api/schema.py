# ============================================
#  schemas.py
#  Pydantic models for request/response validation
#
#  IMPORTANT DIFFERENCE from models.py:
#  models.py  = how data is STORED in PostgreSQL
#  schemas.py = how data TRAVELS through the API
#
#  You often have multiple schemas per table:
#  - Create  (what the user sends in POST body)
#  - Update  (what the user sends in PUT/PATCH body)
#  - Response (what the API sends back to user)
# ============================================

from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime


# ============================================
#  STUDENT SCHEMAS
# ============================================

class StudentCreate(BaseModel):
    """Used when client sends POST /students/ — only these fields required"""
    name:       str   = Field(..., min_length=2, max_length=100, example="Ali Hassan")
    email:      str   = Field(..., example="ali@college.edu")
    roll_no:    str   = Field(..., example="CS-2024-001")
    department: Optional[str] = Field(None, example="Computer Science")


class StudentUpdate(BaseModel):
    """Used for PUT /students/{id} — all fields optional (only send what changed)"""
    name:       Optional[str] = None
    email:      Optional[str] = None
    department: Optional[str] = None
    is_active:  Optional[bool] = None


class StudentResponse(BaseModel):
    """What the API returns — includes auto-generated fields like id, created_at"""
    id:         int
    name:       str
    email:      str
    roll_no:    str
    department: Optional[str]
    is_active:  bool
    created_at: datetime

    class Config:
        orm_mode = True   # allows reading SQLAlchemy objects (not just dicts)


# ============================================
#  COURSE SCHEMAS
# ============================================

class CourseCreate(BaseModel):
    title:       str = Field(..., example="Introduction to Python")
    code:        str = Field(..., example="CS101")
    description: Optional[str] = Field(None, example="Learn Python from scratch")
    credits:     Optional[int] = Field(3, ge=1, le=6)   # between 1 and 6
    teacher:     Optional[str] = Field(None, example="Dr. Ahmed")


class CourseUpdate(BaseModel):
    title:       Optional[str] = None
    description: Optional[str] = None
    credits:     Optional[int] = None
    teacher:     Optional[str] = None


class CourseResponse(BaseModel):
    id:          int
    title:       str
    code:        str
    description: Optional[str]
    credits:     int
    teacher:     Optional[str]

    class Config:
        orm_mode = True


# ============================================
#  ENROLLMENT SCHEMAS
# ============================================

class EnrollmentCreate(BaseModel):
    student_id: int = Field(..., example=1)
    course_id:  int = Field(..., example=1)


class GradeUpdate(BaseModel):
    """Separate schema just for updating grades"""
    grade: float = Field(..., ge=0.0, le=4.0, example=3.7)  # GPA scale 0-4


class EnrollmentResponse(BaseModel):
    id:          int
    student_id:  int
    course_id:   int
    grade:       Optional[float]
    enrolled_at: datetime

    # Nested responses — shows full student/course details inside enrollment
    student:     Optional[StudentResponse]
    course:      Optional[CourseResponse]

    class Config:
        orm_mode = True


# ============================================
#  AUTH SCHEMAS
# ============================================

class UserCreate(BaseModel):
    """Used when client sends POST /auth/register"""
    username: str = Field(..., min_length=3, max_length=50, example="admin")
    password: str = Field(..., min_length=6, example="strongpassword123")


class UserLogin(BaseModel):
    """Used when client sends POST /auth/login"""
    username: str = Field(..., example="admin")
    password: str = Field(..., example="strongpassword123")


class UserResponse(BaseModel):
    """What we send back — note: no password field, ever"""
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    """What /auth/login returns on success"""
    access_token: str
    token_type: str = "bearer"