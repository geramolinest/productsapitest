from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.DBConnection import SessionLocal
from schemas import schemas
from responses import responses
from services import product_service


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.get("", status_code=200, response_model=responses.OkResponse)
def get_all_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> responses.OkResponse:
    return responses.OkResponse(product_service.get_all_products(db, skip, limit))


@products_router.get("/{product_id}", status_code=200, response_model=responses.OkResponse)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)) -> responses.OkResponse:
    return responses.OkResponse(product_service.get_product(db, product_id).__dict__)


@products_router.post("/create", status_code=201, response_model=responses.CreatedResponse)
def create_product(product: schemas.Product, db: Session = Depends(get_db)) -> responses.CreatedResponse:
    return responses.CreatedResponse(product_service.create_product(db, product).__dict__)


@products_router.put("/update/{product_id}", status_code=200, response_model=responses.OkResponse)
def update_product(product_id: int, product: schemas.Product, db: Session = Depends(get_db)) -> responses.OkResponse:
    return responses.OkResponse(product_service.update_product(db, product, product_id).__dict__)


@products_router.delete("/delete/{product_id}", status_code=200, response_model=responses.OkResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> responses.OkResponse:
    response_dict: dict = {'product_id': product_service.delete_product(db, product_id)}
    return responses.OkResponse(response_dict)
