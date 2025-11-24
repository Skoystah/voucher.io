from config import Config
from user.models import UserDB
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Response, status
from user.auth import check_user_password, get_jwt_token


class UserLogin(BaseModel):
    name: str
    password: str


class UserResponse(BaseModel):
    name: str
    is_admin: bool
    token: str


def create_user_router(config: Config):
    router = APIRouter()

    @router.post("/login")
    def login(login_user: UserLogin, response: Response) -> UserResponse:
        print("LOGIN", login_user.name, login_user.password)
        userDB = UserDB(config)

        # TEMP FOR TESTING
        user = userDB.get_user(login_user.name)

        if not check_user_password(login_user.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password is incorrect",
            )

        jwt_token = get_jwt_token(user.name, config.secret_key, 60)
        if not jwt_token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error generating token",
            )

        return UserResponse(name=user.name, is_admin=user.is_admin, token=jwt_token)

    return router
