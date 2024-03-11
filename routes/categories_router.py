from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.DBConnection import SessionLocal
from services import categories_service
from schemas import schemas
from responses import responses

categories_router = APIRouter(prefix="/categories", tags=["Categories"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@categories_router.get("", status_code=200, response_model=responses.OkResponse)
def get_all_categories(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> responses.OkResponse:
    return responses.OkResponse(categories_service.get_all_categories(db, skip=skip, limit=limit))


@categories_router.get("/{category_id}", status_code=200, response_model=responses.OkResponse)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)) -> responses.OkResponse:
    return responses.OkResponse(categories_service.get_category_by_id(db, category_id).__dict__)


@categories_router.post("/create", status_code=201, response_model=responses.CreatedResponse)
def create_category(category: schemas.Category, db: Session = Depends(get_db)) -> responses.CreatedResponse:
    return responses.CreatedResponse(categories_service.create_category(db, category).__dict__)


@categories_router.put("/update/{category_id}", status_code=200, response_model=responses.OkResponse)
def update_category(category_id: int, category: schemas.Category,
                    db: Session = Depends(get_db)) -> responses.OkResponse:
    return responses.OkResponse(categories_service.update_category(db, category_id, category).__dict__)


@categories_router.delete("/delete/{category_id}", status_code=200, response_model=responses.OkResponse)
def delete_category(category_id: int, db: Session = Depends(get_db)) -> responses.OkResponse:
    deleted_categroy: dict = {'category_id': categories_service.delete_category(db, category_id)}
    return responses.OkResponse(deleted_categroy)
