from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import CartItemCRUD, ProductCRUD, OrderCRUD, RefreshTokenCRUD, RecoveryTokenCRUD
from src.crud.users import UserCRUD
from src.db import models
from src.db.db import get_db
from src.service.cart import CartService
from src.service.order import OrderService
from src.service.product import ProductService
from src.service.token import TokenService
from src.service.user import UserService
from src.utils import get_user_id_from_jwt

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

TokenDep = Annotated[str, Depends(oauth2_schema)]

SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_cart_service(db: SessionDep):
    return CartService(CartItemCRUD(db), ProductCRUD(db))


CartServiceDep = Annotated[CartService, Depends(get_cart_service)]


def get_order_service(db: SessionDep):
    return OrderService(OrderCRUD(db), CartItemCRUD(db), ProductCRUD(db))


OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]


def get_product_service(db: SessionDep):
    return ProductService(ProductCRUD(db))


ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]


def get_user_service(db: SessionDep):
    return UserService(UserCRUD(db))


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_token_service(db: SessionDep):
    return TokenService(RefreshTokenCRUD(db), RecoveryTokenCRUD(db))


TokenServiceDep = Annotated[TokenService, Depends(get_token_service)]


async def get_current_user(token: TokenDep, user_service: UserServiceDep):
    user_id = get_user_id_from_jwt(token)
    return await user_service.get_user_by_id(user_id)


CurrentUserDep = Annotated[models.User, Depends(get_current_user)]
