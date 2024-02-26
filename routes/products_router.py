from fastapi import APIRouter

products_router = APIRouter(prefix="/products", tags=["products"])


@products_router.get("")
def say_hi_products() -> dict:
    return {"message": "Hello from products"}