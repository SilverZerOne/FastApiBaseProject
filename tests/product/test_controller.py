import pytest
from fastapi import HTTPException
from app.product.controller import ProductController
from app.product.schema import Product

def test_list_products_empty():
    controller = ProductController()
    controller.products = []  # Limpiamos los products iniciales
    assert len(controller.list_products()) == 0

def test_create_product():
    controller = ProductController()
    controller.products = []  # Limpiamos los products iniciales
    product = Product(name="Test Product", price=10.0)
    created_product = controller.create_product(product)
    assert created_product.name == "Test Product"
    assert created_product.price == 10.0
    assert created_product.id is not None

def test_create_product_duplicate_id():
    controller = ProductController()
    controller.products = []  # Limpiamos los products iniciales
    
    # Creamos el primer product
    product1 = Product(id=1, name="Test Product 1", price=10.0)
    controller.create_product(product1)
    
    # Intentamos crear un segundo product con el mismo ID
    product2 = Product(id=1, name="Test Product 2", price=20.0)
    with pytest.raises(HTTPException) as exc_info:
        controller.create_product(product2)
    assert exc_info.value.status_code == 400

def test_update_product():
    controller = ProductController()
    # Creamos un product inicial
    product = Product(id=1, name="Test Product", price=10.0)
    controller.products = [product]
    
    updated_product = Product(name="Updated Product", price=15.0)
    result = controller.update_product(1, updated_product)
    assert result.name == "Updated Product"
    assert result.price == 15.0

def test_update_nonexistent_product():
    controller = ProductController()
    controller.products = []  # Limpiamos los products iniciales
    product = Product(name="Test Product", price=10.0)
    with pytest.raises(HTTPException) as exc_info:
        controller.update_product(999, product)
    assert exc_info.value.status_code == 404

def test_delete_product():
    controller = ProductController()
    # Creamos un product inicial
    product = Product(id=1, name="Test Product", price=10.0)
    controller.products = [product]
    
    controller.delete_product(1)
    assert len(controller.products) == 0

def test_delete_nonexistent_product():
    controller = ProductController()
    controller.products = []  # Limpiamos los products iniciales
    with pytest.raises(HTTPException) as exc_info:
        controller.delete_product(999)
    assert exc_info.value.status_code == 404 