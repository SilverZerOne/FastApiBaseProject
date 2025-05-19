from fastapi import APIRouter
from app.product.schema import Product
from typing import List
from app.product.controller import ProductController

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

product_controller = ProductController()

@router.get("/", status_code=200, response_model=List[Product])
def list_products():
    return product_controller.list_products()

@router.post("/", status_code=201, response_model=Product)
def create_product(product: Product):
    return product_controller.create_product(product)

@router.put("/{product_id}", status_code=200, response_model=Product)
def update_product(product_id: int, product: Product):
    return product_controller.update_product(product_id, product)

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int):
    product_controller.delete_product(product_id)
