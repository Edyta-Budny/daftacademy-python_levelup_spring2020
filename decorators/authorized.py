from functools import wraps

from fastapi import Request, status
from fastapi.responses import RedirectResponse


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
