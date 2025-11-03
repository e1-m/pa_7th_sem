from sqlalchemy import and_

from src.crud.base import Retrievable, Updatable, Deletable, Creatable
from src.db import models
from src.schemas.filtration import PaginationParams


class ProductCRUD(Creatable, Retrievable, Updatable, Deletable):
    model = models.Product
    key = models.Product.id

    async def get_all(self, ids: list[int] = None, *,
                      pagination: PaginationParams = None,
                      is_active: bool | None = None,
                      order_by=None,
                      for_update=False) -> list[models.Product] | None:
        return await self._get_all(and_(
            models.Product.id.in_(ids) if ids is not None else True,
            models.Product.is_active == is_active if is_active is not None else True
        ), pagination=pagination, order_by=order_by or self.__class__.key, for_update=for_update)
