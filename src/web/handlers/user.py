from config import Config
from user.models import UserDB
from user.auth import validate_jwt_token
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Response, Request, status
from user.auth import check_user_password, get_jwt_token


class UserLogin(BaseModel):
    name: str
    password: str


class UserResponse(BaseModel):
    name: str
    is_admin: bool


def create_user_router(config: Config):
    router = APIRouter()

    @router.post("/login")
    def login(login_user: UserLogin, response: Response) -> UserResponse:
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

        response.set_cookie(
            key="authToken",
            value=jwt_token,
            httponly=True,
            secure=True,
            samesite="none",
        )
        return UserResponse(name=user.name, is_admin=user.is_admin)

    @router.post("/logout")
    def logout(request: Request, response: Response):
        token = request.cookies.get("authToken")

        if not token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Auth token missing",
            )

        try:
            _ = validate_jwt_token(token, config.secret_key)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Issue with JWT Token: {e}",
            )
        # Todo - add user process (invalidate stored token?)

        response.delete_cookie(
            key="authToken",
            httponly=True,
            secure=True,
            samesite="none",
        )

    # @router.get("/users/me")
    # async def read_users_me(
    #     current_user: Annotated[User, Depends(get_current_active_user)],
    # ):
    #     return current_user

    return router
