from src.config import rules
from src.crud import ProductCRUD
from src.custom_exceptions import LimitExceededError, ResourceDoesNotExistError
from src.db.models import Product
from src.schemas.filtration import PaginationParams
from src.schemas.product import ProductUpdate, ProductIn


class ProductService:
    def __init__(self, product_crud: ProductCRUD):
        self.product_crud = product_crud

    async def get_products(self, pagination: PaginationParams = None, is_active: bool = None):
        return await self.product_crud.get_all(pagination=pagination, is_active=is_active)

    async def search_products(self, q: str,
                              categories: list[int] = None,
                              pagination: PaginationParams = None):
        return await self.product_crud.search(q, category_ids=categories, pagination=pagination)

    async def create_product(self, product: ProductIn):
        return await self.product_crud.create(Product(
            **product.model_dump()
        ))

    async def update_product(self, product_id: int, product_update: ProductUpdate):
        return await self.product_crud.update(product_id, product_update)

    async def delete_product(self, product_id: int):
        await self.product_crud.delete(product_id)
