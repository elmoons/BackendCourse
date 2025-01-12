from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
import jwt

from src.config import settings
from src.exceptions import (
    IncorrectTokenException,
    ObjectAlreadyExistException,
    UserAlreadyExistException, UserEmailNotExistException, UserPasswordIncorrectException,
)
from src.schemas.users import UserAdd, UserRequestAdd
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_jwt(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException

    async def register_user(self, data: UserRequestAdd):
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistException as e:
            raise UserAlreadyExistException from e

    async def login_user(self, data: UserRequestAdd):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise UserEmailNotExistException
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise UserPasswordIncorrectException
        return AuthService().create_access_token({"user_id": user.id})

    async def get_me(self, user_id: int):
        user = await self.db.users.get_one_or_none(id=user_id)
        return user
