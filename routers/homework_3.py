from fastapi import APIRouter

router = APIRouter()


@router.get("/welcome")
@router.get("/")
def welcome_text():
    return {"message": "Welcome to the python world!"}
