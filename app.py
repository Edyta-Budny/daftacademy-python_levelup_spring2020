from fastapi import FastAPI

from routers import homework_1, lecture_1, patients, tracks, users

app = FastAPI()


app.include_router(lecture_1.router)
app.include_router(homework_1.router)
app.include_router(users.router)
app.include_router(patients.router)
app.include_router(tracks.router)
