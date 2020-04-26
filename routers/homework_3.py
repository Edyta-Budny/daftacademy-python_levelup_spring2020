from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}


@router.get("/welcome")
def welcome_text():
    return {"message": "Welcome to the python world!"}
