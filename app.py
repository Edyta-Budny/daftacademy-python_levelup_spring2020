from fastapi import FastAPI

from routers import lecture_1, homework_1, homework_3

app = FastAPI()

app.include_router(lecture_1.router)
app.include_router(homework_1.router)
app.include_router(homework_3.router)
