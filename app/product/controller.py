from typing import List
from fastapi import HTTPException
from app.product.schema import Product

class ProductController:
    def __init__(self):
        self.products = [Product(id=1, name="Foo", price=3.4)]

    def list_products(self) -> List[Product]:
        return self.products

    def create_product(self, product: Product) -> Product:
        if product.id is None:
            product.id = len(self.products) + 1
        else:
            for existing_product in self.products:
                if existing_product.id == product.id:
                    raise HTTPException(status_code=400, detail="Product already exists")
        self.products.append(product)
        return product

    def update_product(self, product_id: int, product: Product) -> Product:
        for existing_product in self.products:
            if existing_product.id == product_id:
                existing_product.name = product.name
                existing_product.price = product.price
                existing_product.is_offer = product.is_offer
                return existing_product
        raise HTTPException(status_code=404, detail="Product not found")

    def delete_product(self, product_id: int) -> None:
        for product in self.products:
            if product.id == product_id:
                self.products.remove(product)
                return
        raise HTTPException(status_code=404, detail="Product not found") 