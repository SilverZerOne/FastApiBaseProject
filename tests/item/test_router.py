from fastapi.testclient import TestClient

def test_list_items_empty(client: TestClient):
    # Necesitamos una forma de limpiar los items antes de la prueba
    response = client.get("/items/")
    items = response.json()
    for item in items:
        client.delete(f"/items/{item['id']}")
    
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_item(client: TestClient, sample_item):
    # Primero limpiamos los items existentes
    response = client.get("/items/")
    items = response.json()
    for item in items:
        client.delete(f"/items/{item['id']}")
    
    response = client.post("/items/", json=sample_item)
    assert response.status_code == 201
    assert response.json()["name"] == sample_item["name"]
    assert response.json()["price"] == sample_item["price"]
    assert response.json()["is_offer"] == sample_item["is_offer"]

def test_create_item_invalid_price(client: TestClient, sample_item):
    invalid_item = sample_item.copy()
    invalid_item["price"] = 2.0  # Precio menor que 3
    response = client.post("/items/", json=invalid_item)
    assert response.status_code == 422

def test_update_item(client: TestClient, sample_item):
    # Primero limpiamos los items existentes
    response = client.get("/items/")
    items = response.json()
    for item in items:
        client.delete(f"/items/{item['id']}")
    
    # Creamos un nuevo item
    response = client.post("/items/", json=sample_item)
    created_item = response.json()
    
    # Actualizamos el item
    updated_data = sample_item.copy()
    updated_data["name"] = "Updated Item"
    response = client.put(f"/items/{created_item['id']}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Item"

def test_update_nonexistent_item(client: TestClient, sample_item):
    response = client.put("/items/999", json=sample_item)
    assert response.status_code == 404

def test_delete_item(client: TestClient, sample_item):
    # Primero limpiamos los items existentes
    response = client.get("/items/")
    items = response.json()
    for item in items:
        client.delete(f"/items/{item['id']}")
    
    # Creamos un nuevo item
    response = client.post("/items/", json=sample_item)
    created_item = response.json()
    
    # Eliminamos el item
    response = client.delete(f"/items/{created_item['id']}")
    assert response.status_code == 204
    
    # Verificamos que ya no existe
    response = client.get("/items/")
    assert len(response.json()) == 0

def test_delete_nonexistent_item(client: TestClient):
    response = client.delete("/items/999")
    assert response.status_code == 404 