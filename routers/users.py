import secrets
from hashlib import sha256

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from credentials_variables import SECRET_ACCESS_KEY, SESSION_TOKEN
from decorators.authorized import authorized

router = APIRouter()
user = {'login': 'trudnY', 'password': 'PaC13Nt'}

security = HTTPBasic()

templates = Jinja2Templates(directory="templates")


@router.get("/")
@router.get("/welcome")
@authorized(SESSION_TOKEN)
async def welcome_text(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request, 'user': user['login']})


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
    session_token = sha256(str.encode(f"{credentials.username}{credentials.password}{SECRET_ACCESS_KEY}")).hexdigest()
    response = RedirectResponse(url="/welcome", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key=SESSION_TOKEN, value=session_token)

    return response


@router.post("/logout")
@authorized(SESSION_TOKEN)
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(SESSION_TOKEN)
    return response
