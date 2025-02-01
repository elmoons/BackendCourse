from fastapi import APIRouter, Response, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import PlainTextResponse, JSONResponse

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import UserAlreadyExistException, UserEmailAlreadyExistHTTPException, \
    UserEmailNotExistException, UserEmailNotExistHTTPException, UserPasswordIncorrectException, \
    UserPasswordIncorrectHTTPException
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistException:
        raise UserEmailAlreadyExistHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    try:
        access_token = await AuthService(db).login_user(data)
    except UserEmailNotExistException:
        raise UserEmailNotExistHTTPException
    except UserPasswordIncorrectException:
        raise UserPasswordIncorrectHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    return await AuthService(db).get_me(user_id)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
