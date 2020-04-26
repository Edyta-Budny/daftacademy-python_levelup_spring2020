from hashlib import sha256
import secrets

from fastapi import APIRouter, Depends, HTTPException, status, Header, Request, Response, Cookie
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

router = APIRouter()
router.secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
router.session = {}
user = {'login': 'trudnY', 'password': 'PaC13Nt'}

security = HTTPBasic()

templates = Jinja2Templates(directory="templates")


# async def verify_token(token: str = Header(...)):
#     if token != "session_token":
#         return True
#
#
# async def verify_key(secret_key: str = Header(...)):
#     if secret_key != router.secret_key:
#         return True

def authentication(session_token: str = Cookie(None)):
    if session_token not in router.session:
        session_token = None
    return session_token


@router.get("/")
async def welcome_text(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@router.get("/welcome")
async def welcome_text(request: Request, session_token: str = Depends(authentication)):
    # if verify_token and verify_key is not True:
    if session_token is not None:
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
    # response.set_cookie(key="session_token", value=session_token)
    router.session[session_token] = credentials.username

    return response


@router.post("/logout")
async def logout(session_token: str = Depends(authentication)):
    # if verify_token and verify_key is not True:
    if session_token is not None:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        router.sessions.pop("session_token")
        return response
    else:
        return RedirectResponse(url='/', status_code=status.HTTP_401_UNAUTHORIZED)
