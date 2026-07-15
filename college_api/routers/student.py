# ============================================
#  routers/students.py
#  All student-related API endpoints
#  Registered in main.py with prefix /students
# ============================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schema
from ..database import get_db

router = APIRouter(
    prefix="/students",       # all routes here start with /students
    tags=["Students"],       # groups them in the Swagger UI docs
)


@router.post("/", response_model=schema.StudentResponse, status_code=201)
def create_student(student: schema.StudentCreate, db: Session = Depends(get_db)):
    """
    Create a new student.
    FastAPI automatically reads JSON body and validates it against StudentCreate.
    """
    # Check if email already exists
    existing = crud.get_student_by_email(db, student.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {student.email} is already registered"
        )
    # Check if roll number already exists
    existing_roll = crud.get_student_by_roll(db, student.roll_no)
    if existing_roll:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Roll number {student.roll_no} already exists"
        )
    return crud.create_student(db, student)


@router.get("/", response_model=List[schema.StudentResponse])
def get_all_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all students with optional pagination.
    Example: GET /students/?skip=0&limit=10
    """
    return crud.get_all_students(db, skip=skip, limit=limit)


@router.get("/search", response_model=List[schema.StudentResponse])
def search_students(keyword: str, db: Session = Depends(get_db)):
    """
    Search students by name or department.
    Example: GET /students/search?keyword=computer
    """
    return crud.search_students(db, keyword)


@router.get("/{student_id}", response_model=schema.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Get a single student by ID"""
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=schema.StudentResponse)
def update_student(
    student_id: int,
    updates: schema.StudentUpdate,
    db: Session = Depends(get_db)
):
    """Update student fields (only send the fields you want to change)"""
    student = crud.update_student(db, student_id, updates)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}", response_model=schema.StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Delete a student permanently"""
    student = crud.delete_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/{student_id}/enrollments", response_model=List[schema.EnrollmentResponse])
def get_student_enrollments(student_id: int, db: Session = Depends(get_db)):
    """Get all courses this student is enrolled in"""
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return crud.get_student_enrollments(db, student_id)