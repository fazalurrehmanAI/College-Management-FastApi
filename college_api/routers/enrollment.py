# ============================================
#  routers/enrollments.py
#  Enrollment & grade endpoints
# ============================================
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schema
from ..database import get_db

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"],
)


@router.post("/", response_model=schema.EnrollmentResponse, status_code=201)
def enroll_student(enrollment: schema.EnrollmentCreate, db: Session = Depends(get_db)):
    """Enroll a student in a course"""
    result = crud.enroll_student(db, enrollment)
    if not result:
        raise HTTPException(
            status_code=400,
            detail="Student is already enrolled in this course"
        )
    return result


@router.patch("/{enrollment_id}/grade", response_model=schema.EnrollmentResponse)
def update_grade(
    enrollment_id: int,
    grade_data: schema.GradeUpdate,
    db: Session = Depends(get_db)
):
    """Assign or update a student's grade (0.0 to 4.0 scale)"""
    result = crud.update_grade(db, enrollment_id, grade_data)
    if not result:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return result