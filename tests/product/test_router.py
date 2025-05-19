from fastapi.testclient import TestClient

def test_list_products_empty(client: TestClient):
    # Necesitamos una forma de limpiar los products antes de la prueba
    response = client.get("/products/")
    products = response.json()
    for product in products:
        client.delete(f"/products/{product['id']}")
    
    response = client.get("/products/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_product(client: TestClient, sample_product):
    # Primero limpiamos los products existentes
    response = client.get("/products/")
    products = response.json()
    for product in products:
        client.delete(f"/products/{product['id']}")
    
    response = client.post("/products/", json=sample_product)
    assert response.status_code == 201
    assert response.json()["name"] == sample_product["name"]
    assert response.json()["price"] == sample_product["price"]
    assert response.json()["is_offer"] == sample_product["is_offer"]

def test_create_product_invalid_price(client: TestClient, sample_product):
    invalid_product = sample_product.copy()
    invalid_product["price"] = 2.0  # Precio menor que 3
    response = client.post("/products/", json=invalid_product)
    assert response.status_code == 422

def test_update_product(client: TestClient, sample_product):
    # Primero limpiamos los products existentes
    response = client.get("/products/")
    products = response.json()
    for product in products:
        client.delete(f"/products/{product['id']}")
    
    # Creamos un nuevo product
    response = client.post("/products/", json=sample_product)
    created_product = response.json()
    
    # Actualizamos el product
    updated_data = sample_product.copy()
    updated_data["name"] = "Updated product"
    response = client.put(f"/products/{created_product['id']}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated product"

def test_update_nonexistent_product(client: TestClient, sample_product):
    response = client.put("/products/999", json=sample_product)
    assert response.status_code == 404

def test_delete_product(client: TestClient, sample_product):
    # Primero limpiamos los products existentes
    response = client.get("/products/")
    products = response.json()
    for product in products:
        client.delete(f"/products/{product['id']}")
    
    # Creamos un nuevo product
    response = client.post("/products/", json=sample_product)
    created_product = response.json()
    
    # Eliminamos el product
    response = client.delete(f"/products/{created_product['id']}")
    assert response.status_code == 204
    
    # Verificamos que ya no existe
    response = client.get("/products/")
    assert len(response.json()) == 0

def test_delete_nonexistent_product(client: TestClient):
    response = client.delete("/products/999")
    assert response.status_code == 404 