import pytest
from src.db.models import User, Product, CartItem
from src.schemas.base import ObjUpdate
from src.custom_exceptions import (
                                   ResourceAlreadyExistsError,
                                   DependentEntityExistsError)
from src.schemas.filtration import PaginationParams
from src.crud import UserCRUD, ProductCRUD, CartItemCRUD

from tests.fixtures import *


# region --- UserCRUD Tests ---
@pytest.mark.asyncio(loop_scope="session")
async def test_user_create_and_get(user_crud: UserCRUD):
    new_user = User(
        email="test_user@example.com",
        password="hashed_password",
        name="Test User Name"
    )
    created_user = await user_crud.create(new_user)

    assert created_user.id is not None
    assert created_user.email == "test_user@example.com"

    fetched_user = await user_crud.get(created_user.id)
    assert fetched_user.name == "Test User Name"


@pytest.mark.asyncio(loop_scope="session")
async def test_user_create_duplicate_email_raises_error(user_crud: UserCRUD):
    user_crud.db.add(User(email="unique@example.com", name="U1"))
    await user_crud.db.flush()

    duplicate_user = User(email="unique@example.com", name="U2")

    with pytest.raises(ResourceAlreadyExistsError, match="User with the given email already exists"):
        await user_crud.create(duplicate_user)


@pytest.mark.asyncio(loop_scope="session")
async def test_user_get_by_email_found(user_crud: UserCRUD):
    existing_user = User(email="findme_by_email@example.com", name="Finder")
    await user_crud.create(existing_user)

    found_user = await user_crud.get_by_email("findme_by_email@example.com")
    assert found_user is not None
    assert found_user.name == "Finder"


# endregion


# region --- ProductCRUD Tests ---


@pytest.mark.asyncio(loop_scope="session")
async def test_product_update_with_predicate_failure(product_crud: ProductCRUD):
    """Test update when predicate fails."""
    product = Product(title="Expensive Item", description="Desc", quantity=1, full_price=2000)
    await product_crud.create(product)

    # Predicate: Only allow update if price is less than 1500
    update_data = ObjUpdate(title="Too Expensive")

    updated_product = await product_crud.update(
        product.id,
        update_data,
        predicate=lambda p: p.full_price < 1500  # This will fail
    )

    assert updated_product is None  # No update should have happened


@pytest.mark.asyncio(loop_scope="session")
async def test_product_delete_with_dependent_cart_item_raises_error(
        user_crud: UserCRUD, product_crud: ProductCRUD, cart_item_crud: CartItemCRUD):
    user = User(email="user_dep@test.com", name="U1")
    product = Product(title="Protected Product", description="Desc", quantity=1, full_price=10)
    await user_crud.create(user)
    await product_crud.create(product)

    # Create a dependent entity (CartItem)
    cart_item = CartItem(user_id=user.id, product_id=product.id, quantity=1)
    await cart_item_crud.create(cart_item)

    with pytest.raises(DependentEntityExistsError,
                       match="There is some other entity in relation cart_items that depends on Product"):
        await product_crud.delete(product.id)


@pytest.mark.asyncio(loop_scope="session")
async def test_product_get_all_with_filters(product_crud: ProductCRUD):
    """Test get_all with custom filters, pagination, and ordering."""
    await product_crud.create(
        Product(title="Z Active", description="Desc", quantity=1, full_price=100, is_active=True))
    await product_crud.create(
        Product(title="A Inactive", description="Desc", quantity=1, full_price=50, is_active=False))
    await product_crud.create(
        Product(title="B Active", description="Desc", quantity=1, full_price=200, is_active=True))

    # Test filter for is_active=True, ordered by title descending, limited to 1
    active_products = await product_crud.get_all(
        is_active=True,
        pagination=PaginationParams(limit=1, offset=0)
    )

    assert len(active_products) == 1
    assert active_products[0].title == "Z Active"


# endregion

# region --- CartItemCRUD Tests ---


@pytest.mark.asyncio(loop_scope="session")
async def test_cartitem_get_and_delete(
        user_crud: UserCRUD, product_crud: ProductCRUD, cart_item_crud: CartItemCRUD):
    """Test composite key retrieval and deletion."""
    user = User(email="composite@test.com", name="Composite User")
    product = Product(title="Single Item", description="Desc", quantity=10, full_price=100)
    await user_crud.create(user)
    await product_crud.create(product)

    item = CartItem(user_id=user.id, product_id=product.id, quantity=3)
    await cart_item_crud.create(item)

    # 1. Test get (composite key: user_id, product_id)
    fetched_item = await cart_item_crud.get(user.id, product.id)
    assert fetched_item is not None
    assert fetched_item.quantity == 3
    # Check hybrid property
    assert fetched_item.total_price == 300  # 3 * 100

    # 2. Test delete
    await cart_item_crud.delete(user.id, product.id)

    deleted_item = await cart_item_crud.get(user.id, product.id)
    assert deleted_item is None


@pytest.mark.asyncio(loop_scope="session")
async def test_cartitem_delete_all_by_user_id(
        user_crud: UserCRUD, product_crud: ProductCRUD, cart_item_crud: CartItemCRUD):
    """Test custom method to delete all cart items for a specific user."""
    user1 = User(email="cart1@test.com", name="User 1")
    user2 = User(email="cart2@test.com", name="User 2")
    p1 = Product(title="P1", description="Desc", quantity=1, full_price=1)
    p2 = Product(title="P2", description="Desc", quantity=1, full_price=1)
    await user_crud.create(user1)
    await user_crud.create(user2)
    await product_crud.create(p1)
    await product_crud.create(p2)

    # User 1 has two items
    await cart_item_crud.create(CartItem(user_id=user1.id, product_id=p1.id, quantity=1))
    await cart_item_crud.create(CartItem(user_id=user1.id, product_id=p2.id, quantity=1))
    # User 2 has one item
    await cart_item_crud.create(CartItem(user_id=user2.id, product_id=p1.id, quantity=1))

    # Delete all items for User 1
    await cart_item_crud.delete_all_by_user_id(user1.id)

    # Verify User 1's items are gone
    items_user1 = await cart_item_crud.get_all_by_user_id(user1.id)
    assert len(items_user1) == 0

    # Verify User 2's item remains
    items_user2 = await cart_item_crud.get_all_by_user_id(user2.id)
    assert len(items_user2) == 1

# endregion
