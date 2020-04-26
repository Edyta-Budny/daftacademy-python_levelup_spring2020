from hashlib import sha256
import secrets

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter()
router.secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

security = HTTPBasic()


async def verify_token(token: str = Header(...)):
    if token != "session_token":
        return True


async def verify_key(secret_key: str = Header(...)):
    if secret_key != router.secret_key:
        return True


@router.get("/welcome")
@router.get("/")
async def welcome_text():
    return {"message": "Welcome to the python world!"}


@router.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    session_token = sha256(str.encode(f"{credentials.username}{credentials.password}{router.secret_key}")).hexdigest()
    response = RedirectResponse(url="/welcome", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="session_token", value=session_token)

    return response


@router.post("/logout")
async def logout():
    if verify_token and verify_key is not True:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.delete_cookie("session_token")
        return response
    else:
        response = RedirectResponse(url='/', status_code=status.HTTP_401_UNAUTHORIZED)
        return response

