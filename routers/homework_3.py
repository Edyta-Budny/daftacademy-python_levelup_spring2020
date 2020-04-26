from functools import wraps
from hashlib import sha256
import secrets

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

router = APIRouter()
router.secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
router.session_token = "session_token"
user = {'login': 'trudnY', 'password': 'PaC13Nt'}

security = HTTPBasic()

templates = Jinja2Templates(directory="templates")


def authorized(cookie_key: str):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = request.cookies.get(cookie_key)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                return await f(request, *args, **kwargs)
            else:
                # the user is not authorized.
                return RedirectResponse(url='/', status_code=status.HTTP_401_UNAUTHORIZED)

        return decorated_function

    return decorator


@router.get("/")
@router.get("/welcome")
@authorized(router.session_token)
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
    session_token = sha256(str.encode(f"{credentials.username}{credentials.password}{router.secret_key}")).hexdigest()
    response = RedirectResponse(url="/welcome", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key=router.session_token, value=session_token)

    return response


@router.post("/logout")
@authorized(router.session_token)
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(router.session_token)
    return response
