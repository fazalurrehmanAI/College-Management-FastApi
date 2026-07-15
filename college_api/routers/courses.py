# ============================================
#  routers/courses.py
#  All course-related API endpoints
# ============================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schema
from ..database import get_db

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.post("/", response_model=schema.CourseResponse, status_code=201)
def create_course(course: schema.CourseCreate, db: Session = Depends(get_db)):
    existing = crud.get_course_by_code(db, course.code)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Course code {course.code} already exists"
        )
    return crud.create_course(db, course)


@router.get("/", response_model=List[schema.CourseResponse])
def get_all_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_courses(db, skip=skip, limit=limit)


@router.get("/{course_id}", response_model=schema.CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.put("/{course_id}", response_model=schema.CourseResponse)
def update_course(
    course_id: int,
    updates: schema.CourseUpdate,
    db: Session = Depends(get_db)
):
    course = crud.update_course(db, course_id, updates)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.delete("/{course_id}", response_model=schema.CourseResponse)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.delete_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/{course_id}/students", response_model=List[schema.EnrollmentResponse])
def get_course_students(course_id: int, db: Session = Depends(get_db)):
    """Get all students enrolled in this course"""
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.get_course_enrollments(db, course_id)