from src.crud import UserCRUD
from src.db.models import User
from src.schemas.user import UserIn


class UserService:
    def __init__(self, user_crud: UserCRUD):
        self.user_crud = user_crud

    async def register_user(self, user: UserIn):
        return await self.user_crud.create(User(**user.model_dump()))

    async def get_user_by_identity_provider_id(self, identity_provider_id: str):
        return await self.user_crud.get_by_idp_id(identity_provider_id)

    async def get_user_by_id(self, user_id: int):
        return await self.user_crud.get(user_id)

    async def get_user_by_email(self, email: str):
        return await self.user_crud.get_by_email(email)
