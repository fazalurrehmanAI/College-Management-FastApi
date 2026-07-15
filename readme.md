# College Management API
## FastAPI + PostgreSQL — Complete Project

---

## Project Structure

```
college_api/
│
├── __init__.py
├── main.py          ← Entry point, app setup, register routers
├── database.py      ← DB connection, engine, session, get_db()
├── models.py        ← SQLAlchemy table definitions (Student, Course, Enrollment)
├── schemas.py       ← Pydantic request/response validation
├── crud.py          ← All database query functions
├── .env             ← Your secret credentials (never commit this!)
├── requirements.txt ← Python package list
│
└── routers/
    ├── __init__.py
    ├── students.py    ← /students endpoints
    ├── courses.py     ← /courses endpoints
    └── enrollments.py ← /enrollments endpoints
```

---

## Setup Steps

### 1. Install packages
```bash
pip install -r requirements.txt
```

### 2. Make sure PostgreSQL is running and the database exists
```bash
psql -U postgres -c "CREATE DATABASE college;"
```

### 3. Run the server
```bash
uvicorn main:app --reload
```

### 4. Open the interactive docs
Visit: http://127.0.0.1:8000/docs

---

## API Endpoints

### Students
| Method | URL | Description |
|--------|-----|-------------|
| POST   | /students/ | Create a new student |
| GET    | /students/ | Get all students |
| GET    | /students/{id} | Get one student |
| GET    | /students/search?keyword=ali | Search students |
| PUT    | /students/{id} | Update student |
| DELETE | /students/{id} | Delete student |
| GET    | /students/{id}/enrollments | Student's courses |

### Courses
| Method | URL | Description |
|--------|-----|-------------|
| POST   | /courses/ | Create a course |
| GET    | /courses/ | Get all courses |
| GET    | /courses/{id} | Get one course |
| PUT    | /courses/{id} | Update course |
| DELETE | /courses/{id} | Delete course |
| GET    | /courses/{id}/students | Course's students |

### Enrollments
| Method | URL | Description |
|--------|-----|-------------|
| POST   | /enrollments/ | Enroll student in course |
| PATCH  | /enrollments/{id}/grade | Update a grade |

---

## Example Requests

### Create a student
```json
POST /students/
{
  "name": "Ali Hassan",
  "email": "ali@college.edu",
  "roll_no": "CS-2024-001",
  "department": "Computer Science"
}
```

### Create a course
```json
POST /courses/
{
  "title": "Introduction to Python",
  "code": "CS101",
  "credits": 3,
  "teacher": "Dr. Ahmed"
}
```

### Enroll student in course
```json
POST /enrollments/
{
  "student_id": 1,
  "course_id": 1
}
```

### Assign a grade
```json
PATCH /enrollments/1/grade
{
  "grade": 3.7
}
```