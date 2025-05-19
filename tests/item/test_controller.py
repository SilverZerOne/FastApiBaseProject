import pytest
from fastapi import HTTPException
from app.item.controller import ItemController
from app.item.schema import Item

def test_list_items_empty():
    controller = ItemController()
    controller.items = []  # Limpiamos los items iniciales
    assert len(controller.list_items()) == 0

def test_create_item():
    controller = ItemController()
    controller.items = []  # Limpiamos los items iniciales
    item = Item(name="Test Item", price=10.0)
    created_item = controller.create_item(item)
    assert created_item.name == "Test Item"
    assert created_item.price == 10.0
    assert created_item.id is not None

def test_create_item_duplicate_id():
    controller = ItemController()
    controller.items = []  # Limpiamos los items iniciales
    
    # Creamos el primer item
    item1 = Item(id=1, name="Test Item 1", price=10.0)
    controller.create_item(item1)
    
    # Intentamos crear un segundo item con el mismo ID
    item2 = Item(id=1, name="Test Item 2", price=20.0)
    with pytest.raises(HTTPException) as exc_info:
        controller.create_item(item2)
    assert exc_info.value.status_code == 400

def test_update_item():
    controller = ItemController()
    # Creamos un item inicial
    item = Item(id=1, name="Test Item", price=10.0)
    controller.items = [item]
    
    updated_item = Item(name="Updated Item", price=15.0)
    result = controller.update_item(1, updated_item)
    assert result.name == "Updated Item"
    assert result.price == 15.0

def test_update_nonexistent_item():
    controller = ItemController()
    controller.items = []  # Limpiamos los items iniciales
    item = Item(name="Test Item", price=10.0)
    with pytest.raises(HTTPException) as exc_info:
        controller.update_item(999, item)
    assert exc_info.value.status_code == 404

def test_delete_item():
    controller = ItemController()
    # Creamos un item inicial
    item = Item(id=1, name="Test Item", price=10.0)
    controller.items = [item]
    
    controller.delete_item(1)
    assert len(controller.items) == 0

def test_delete_nonexistent_item():
    controller = ItemController()
    controller.items = []  # Limpiamos los items iniciales
    with pytest.raises(HTTPException) as exc_info:
        controller.delete_item(999)
    assert exc_info.value.status_code == 404 