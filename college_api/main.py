
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

if __package__ in {None, ""}:
    import sys
    

    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from college_api.database import engine
    from college_api import model
    from college_api.routers import student, courses, enrollment, auth
else:
    from .database import engine
    from . import model
    from .routers import student, courses, enrollment, auth

model.Base.metadata.create_all(bind=engine)

# --------------------------------------------
# Create the FastAPI application
# --------------------------------------------
app = FastAPI(
    title="College Management API",
    description="""
    A complete REST API for managing college data.

    ## Features
    - **Students** — Create, read, update, delete students
    - **Courses**  — Manage all college courses
    - **Enrollments** — Enroll students in courses and assign grades

    ## Database
    Connected to PostgreSQL (college database)
    """,
    version="1.0.0",
)

# templates = Jinja2Templates(directory="templates")
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------
# Register routers
# Each router handles a group of related routes
# --------------------------------------------
app.include_router(auth.router)
app.include_router(student.router)
app.include_router(courses.router)
app.include_router(enrollment.router)

# --------------------------------------------
# Root endpoint — health check
# Visit http://127.0.0.1:8000/ to confirm running
# --------------------------------------------
@app.get("/health")
def health():
    return {"status": "OK"}

# --------------------------------------------

if __name__ == "__main__":
    import uvicorn

    app_target = "main:app" if __package__ in {None, ""} else "college_api.main:app"
    uvicorn.run(app_target, host="127.0.0.1", port=8000, reload=True)