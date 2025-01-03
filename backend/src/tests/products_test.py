import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime
from ..routers.products import ProductDAL, CreateProductRequest, CreateStockRequest, RoshidError
from ..utils.uuid import simple_uuid
@pytest.fixture
def mock_collections():
    product_collection = AsyncMock()
    stock_collection = AsyncMock()
    inventory_collection = AsyncMock()
    return product_collection, stock_collection, inventory_collection

@pytest.fixture
def product_dal(mock_collections):
    product_collection, stock_collection, inventory_collection = mock_collections
    return ProductDAL(product_collection, stock_collection, inventory_collection)

@pytest.mark.asyncio
async def test_create_product(product_dal, mock_collections):
    product_collection, _, _ = mock_collections
    product_collection.insert_one.return_value = None

    product = CreateProductRequest(
        availability=True,
        price=100.0,
        content={"name": "Test Product", "description": "Test Description", "images": ["image1.jpg"]},
        delivery_method="standard"
    )
    store_id = "store123"
    product_id = await product_dal.create_product(product, store_id)

    assert product_id is not None
    product_collection.insert_one.assert_called_once()

@pytest.mark.asyncio
async def test_get_product(product_dal, mock_collections):
    product_collection, _, _ = mock_collections
    product_collection.find_one.return_value = {"_id": "product123", "name": "Test Product"}

    product_id = "product123"
    product = await product_dal.get_product(product_id)

    assert product["_id"] == "product123"
    product_collection.find_one.assert_called_once_with({"_id": product_id})

@pytest.mark.asyncio
async def test_add_stock(product_dal, mock_collections):
    _, stock_collection, inventory_collection = mock_collections
    stock_collection.insert_one.return_value.inserted_id = "stock123"
    stock_collection.update_one.return_value = None
    inventory_collection.insert_one.return_value = None

    stock = CreateStockRequest(quantity=10, minimum_quantity=2)
    product_id = "product123"
    stock_id = await product_dal.add_stock(product_id, stock)

    assert stock_id == "stock123"
    stock_collection.insert_one.assert_called_once()
    stock_collection.update_one.assert_called_once()
    inventory_collection.insert_one.assert_called_once()

@pytest.mark.asyncio
async def test_get_stock(product_dal, mock_collections):
    _, stock_collection, _ = mock_collections
    stock_collection.find_one.return_value = {"_id": "stock123", "product_id": "product123"}

    product_id = "product123"
    stock = await product_dal.get_stock(product_id)

    assert stock["_id"] == "stock123"
    stock_collection.find_one.assert_called_once_with({"product_id": product_id})

@pytest.mark.asyncio
async def test_update_stock(product_dal, mock_collections):
    _, stock_collection, inventory_collection = mock_collections
    stock_collection.find_one.return_value = {"product_id": "product123", "quantity": 5}
    stock_collection.update_one.return_value.modified_count = 1
    inventory_collection.insert_one.return_value = None

    product_id = "product123"
    quantity = 10
    success = await product_dal.update_stock(product_id, quantity)

    assert success is True
    stock_collection.find_one.assert_called_once_with({"product_id": product_id})
    stock_collection.update_one.assert_called_once()
    inventory_collection.insert_one.assert_called_once()