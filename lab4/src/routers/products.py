from typing import Annotated

from fastapi import APIRouter, status, Depends, Query

from src.deps import ProductServiceDep
from src.schemas.filtration import PaginationParams
from src.schemas.product import ProductIn, ProductOut, ProductUpdate

router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('', status_code=status.HTTP_200_OK, response_model=list[ProductOut])
async def get_products(product_service: ProductServiceDep, pagination: PaginationParams = Depends()):
    return await product_service.get_products(pagination=pagination, is_active=True)


@router.get('/search', status_code=status.HTTP_200_OK, response_model=list[ProductOut])
async def search_products(product_service: ProductServiceDep, q: str,
                          categories: Annotated[list[int], Query(alias="category")] = None,
                          pagination: PaginationParams = Depends()):
    return await product_service.search_products(q, categories=categories, pagination=pagination)


@router.get('/all', status_code=status.HTTP_200_OK, response_model=list[ProductOut])
async def get_products_admin(product_service: ProductServiceDep,
                             pagination: PaginationParams = Depends(),
                             is_active: bool = None):
    return await product_service.get_products(pagination=pagination, is_active=is_active)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=ProductOut)
async def create_product(product: ProductIn, product_service: ProductServiceDep):
    return await product_service.create_product(product)


@router.patch('/{product_id}', status_code=status.HTTP_200_OK, response_model=ProductOut)
async def update_product(product_id: int, product_update: ProductUpdate, product_service: ProductServiceDep):
    return await product_service.update_product(product_id, product_update)


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, product_service: ProductServiceDep):
    await product_service.delete_product(product_id)
