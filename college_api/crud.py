# ============================================
#  crud.py
#  All database operations live here.
#  CRUD = Create, Read, Update, Delete
#
#  Routes call these functions — they never
#  touch the DB directly. This keeps routes
#  clean and this file easy to test.
#
#  Every function receives a 'db' Session
#  injected by FastAPI's Depends(get_db)
# ============================================

from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import model
from . import schema


# ============================================
#  STUDENT CRUD
# ============================================

def get_student(db: Session, student_id: int):
    """Get one student by their ID"""
    return db.query(model.Student).filter(model.Student.id == student_id).first()


def get_student_by_email(db: Session, email: str):
    """Get one student by email — used to check duplicates before creating"""
    return db.query(model.Student).filter(model.Student.email == email).first()


def get_student_by_roll(db: Session, roll_no: str):
    """Get one student by roll number"""
    return db.query(model.Student).filter(model.Student.roll_no == roll_no).first()


def get_all_students(db: Session, skip: int = 0, limit: int = 100):
    """
    Get a list of all students with pagination.
    skip=0, limit=100 means: start from row 0, return max 100 rows.
    Example: skip=10, limit=10 → page 2 of results
    """
    return db.query(model.Student).offset(skip).limit(limit).all()


def search_students(db: Session, keyword: str):
    """Search students by name or department (case-insensitive)"""
    return db.query(model.Student).filter(
        or_(
            model.Student.name.ilike(f"%{keyword}%"),
            model.Student.department.ilike(f"%{keyword}%")
        )
    ).all()


def create_student(db: Session, student: schema.StudentCreate):
    """
    Insert a new student row.
    Steps: create object → add to session → commit → refresh to get auto fields
    """
    db_student = model.Student(**student.dict())  # unpack schema into model
    db.add(db_student)       # stage it (like git add)
    db.commit()              # save to DB (like git commit)
    db.refresh(db_student)   # reload from DB to get id, created_at etc.
    return db_student


def update_student(db: Session, student_id: int, updates: schema.StudentUpdate):
    """Update only the fields that were provided (partial update)"""
    db_student = get_student(db, student_id)
    if not db_student:
        return None

    # .dict(exclude_unset=True) only gives fields the user actually sent
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)   # e.g. db_student.name = "new name"

    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    """Delete a student permanently"""
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    db.delete(db_student)
    db.commit()
    return db_student


# ============================================
#  COURSE CRUD
# ============================================

def get_course(db: Session, course_id: int):
    return db.query(model.Course).filter(model.Course.id == course_id).first()


def get_course_by_code(db: Session, code: str):
    return db.query(model.Course).filter(model.Course.code == code).first()


def get_all_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Course).offset(skip).limit(limit).all()


def create_course(db: Session, course: schema.CourseCreate):
    db_course = model.Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, course_id: int, updates: schema.CourseUpdate):
    db_course = get_course(db, course_id)
    if not db_course:
        return None
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int):
    db_course = get_course(db, course_id)
    if not db_course:
        return None
    db.delete(db_course)
    db.commit()
    return db_course


# ============================================
#  ENROLLMENT CRUD
# ============================================

def enroll_student(db: Session, enrollment: schema.EnrollmentCreate):
    """Enroll a student in a course"""
    # Check if already enrolled
    existing = db.query(model.Enrollment).filter(
        model.Enrollment.student_id == enrollment.student_id,
        model.Enrollment.course_id  == enrollment.course_id
    ).first()
    if existing:
        return None   # already enrolled

    db_enrollment = model.Enrollment(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


def get_student_enrollments(db: Session, student_id: int):
    """Get all courses a student is enrolled in"""
    return db.query(model.Enrollment).filter(
        model.Enrollment.student_id == student_id
    ).all()


def get_course_enrollments(db: Session, course_id: int):
    """Get all students enrolled in a course"""
    return db.query(model.Enrollment).filter(
        model.Enrollment.course_id == course_id
    ).all()


def update_grade(db: Session, enrollment_id: int, grade_data: schema.GradeUpdate):
    """Assign or update a grade for an enrollment"""
    db_enrollment = db.query(model.Enrollment).filter(
        model.Enrollment.id == enrollment_id
    ).first()
    if not db_enrollment:
        return None
    db_enrollment.grade = grade_data.grade
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment