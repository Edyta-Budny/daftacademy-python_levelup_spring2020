from hashlib import sha256
import secrets

from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

router = APIRouter()
router.secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

user = {'login': 'trudnY', 'password': 'PaC13Nt'}

security = HTTPBasic()

templates = Jinja2Templates(directory="templates")


async def authorization(token: str = Header(...), secret_key: str = Header(...)):
    if token != "session_token" and secret_key != router.secret_key:
        return True


@router.get("/")
async def welcome_text(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@router.get("/welcome")
async def welcome_text(request: Request):
    if authorization is not True:
        return templates.TemplateResponse("welcome_login.html", {"request": request, 'user': user['login']})
    else:
        return RedirectResponse(url='/', status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, user['login'])
    correct_password = secrets.compare_digest(credentials.password, user['password'])
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
    if authorization is not True:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.delete_cookie("session_token")
        return response
    else:
        return RedirectResponse(url='/', status_code=status.HTTP_401_UNAUTHORIZED)
