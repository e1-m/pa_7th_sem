from datetime import timedelta, datetime, UTC
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from src.config import settings
from src.custom_exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,

)
from src.deps import TokenDep, TokenServiceDep, UserServiceDep
from src.schemas.message import Message
from src.schemas.token import Token
from src.schemas.user import UserIn, UserOut
from src.service.token import TokenService
from src.utils import create_jwt_token, get_user_id_from_jwt, verify_password

router = APIRouter(
    prefix='/auth',
    tags=["Authentication"]
)


async def _handle_user_tokens(user_id: int, response: Response, token_service: TokenService):
    access_token = create_jwt_token(user_id=user_id,
                                    expires_in=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES))
    refresh_token = create_jwt_token(user_id=user_id,
                                     expires_in=timedelta(days=settings.REFRESH_TOKEN_EXPIRATION_DAYS))
    await token_service.upsert_refresh_token(user_id, refresh_token)

    response.set_cookie(key="refresh_token",
                        value=refresh_token,
                        httponly=True,
                        secure=False,  # should be True in production
                        expires=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRATION_DAYS),
                        samesite=settings.SAME_SITE_COOKIE)
    return {'access_token': access_token, "token_type": "bearer"}


@router.post('/register', status_code=status.HTTP_200_OK, response_model=UserOut)
async def register(user: UserIn, user_service: UserServiceDep):
    return await user_service.register_user(user)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
                res: Response,
                user_service: UserServiceDep,
                token_service: TokenServiceDep):
    user = await user_service.get_user_by_email(user_credentials.username)
    if user is not None and user.password is None:
        raise InvalidCredentialsError("Account is registered with an external provider")

    if not (user and verify_password(user_credentials.password, user.password)):
        raise InvalidCredentialsError("No account with the given email exists or the password is wrong")

    return await _handle_user_tokens(user.id, res, token_service)


@router.post('/refresh', status_code=status.HTTP_200_OK, response_model=Token)
async def refresh(req: Request, res: Response, token_service: TokenServiceDep):
    token = req.cookies.get('refresh_token')
    if not token:
        raise InvalidTokenError("No token found")
    user_id = get_user_id_from_jwt(token)

    if not (await token_service.is_refresh_token_valid(user_id, token)):
        raise InvalidTokenError("Invalid refresh token")

    return await _handle_user_tokens(user_id, res, token_service)


@router.post('/logout', status_code=status.HTTP_200_OK, response_model=Message)
async def logout(token: TokenDep, res: Response, token_service: TokenServiceDep):
    user_id = get_user_id_from_jwt(token)
    await token_service.revoke_refresh_token(user_id)
    res.delete_cookie('refresh_token')
    return Message(message='logged out')
