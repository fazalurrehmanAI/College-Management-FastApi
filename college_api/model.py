# ============================================
#  models.py
#  Each class here = one table in PostgreSQL
#  SQLAlchemy maps Python objects ↔ DB rows
# ============================================

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


# --------------------------------------------
# STUDENTS table
# --------------------------------------------
class Student(Base):
    __tablename__ = "students"

    id         = Column(Integer, primary_key=True, index=True)   # auto-increment PK
    name       = Column(String(100), nullable=False)             # required field
    email      = Column(String(100), unique=True, index=True)    # must be unique
    roll_no    = Column(String(20), unique=True)
    department = Column(String(50))
    is_active  = Column(Boolean, default=True)                   # default value
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # auto timestamp

    # Relationship — one student can have many enrollments
    # 'back_populates' links both sides together
    enrollments = relationship("Enrollment", back_populates="student")

    def __repr__(self):
        return f"<Student {self.name} ({self.roll_no})>"


# --------------------------------------------
# COURSES table
# --------------------------------------------
class Course(Base):
    __tablename__ = "courses"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(150), nullable=False)
    code        = Column(String(20), unique=True, nullable=False)  # e.g. CS101
    description = Column(String(500))
    credits     = Column(Integer, default=3)
    teacher     = Column(String(100))

    # One course can have many enrollments
    enrollments = relationship("Enrollment", back_populates="course")

    def __repr__(self):
        return f"<Course {self.code}: {self.title}>"


# --------------------------------------------
# ENROLLMENTS table  (junction table: Student ↔ Course)
# This is a Many-to-Many relationship handled
# through a separate table with extra fields (grade)
# --------------------------------------------
class Enrollment(Base):
    __tablename__ = "enrollments"

    id         = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)  # FK to students
    course_id  = Column(Integer, ForeignKey("courses.id"),  nullable=False)  # FK to courses
    grade      = Column(Float, nullable=True)      # e.g. 3.5 — null until graded
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())

    # Link back to parent objects
    student = relationship("Student", back_populates="enrollments")
    course  = relationship("Course",  back_populates="enrollments")

    def __repr__(self):
        return f"<Enrollment student={self.student_id} course={self.course_id}>"


# --------------------------------------------
# USERS table
# Stores login credentials. We NEVER store the
# raw password — only its bcrypt hash.
# --------------------------------------------
class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)   # bcrypt hash, never plain text
    is_active       = Column(Boolean, default=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}>"