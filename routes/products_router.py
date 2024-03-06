from fastapi import APIRouter
from controllers import products_controller

products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.get("")
def get_all_products() -> dict:
    return products_controller.get_products()
