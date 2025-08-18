from fastapi import APIRouter, Query
from models import Product
from typing import  Optional

product_router = APIRouter()

sample_product_1 = Product(product_id=123, name="Smartphone", category="Electronics", price=599.99)
sample_product_2 = Product(product_id=456, name="Phone Case", category="Accessories", price=19.99)
sample_product_3 = Product(product_id=789, name="Iphone", category="Electronics", price=1299.99)
sample_product_4 = Product(product_id=101, name="Headphones", category="Accessories", price=99.99)
sample_product_5 = Product(product_id=202, name="Smartwatch", category="Electronics", price=299.99)

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]





@product_router.get("/product/search", tags=["product,"])
def search_product(keyword: str, category: Optional[str] = Query(None), limit: Optional[int] = Query(10,gt=1, lt=50)):

    print(keyword)
    result_array = []
    for product in sample_products:
        if keyword.lower() in product.name:
            result_array.append(product)

    if category:
        result_array = [product for product in result_array if product.category.lower() == category.lower()]

    if len(result_array) > 0:
        return result_array[:limit]
    else:
        return {"message": "No products by this filter"}


@product_router.get("/product/{product_id}", tags=["product,"])
def get_product_by_id(product_id: int):
    for product in sample_products:
        if product.product_id == product_id:
            return product
    return {"message": "No product"}