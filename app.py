from fastapi import FastAPI

from routers import lecture_1, homework_1, users, patients

app = FastAPI()

app.include_router(lecture_1.router)
app.include_router(homework_1.router)
app.include_router(users.router)
app.include_router(patients.router)
