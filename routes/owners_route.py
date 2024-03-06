from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from starlette import status

from db.DBConnection import SessionLocal
from services import owners_service
from schemas import schemas
from responses import responses

owners_router = APIRouter(prefix="/owners", tags=["Owners"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@owners_router.get("", status_code=status.HTTP_200_OK)
def get_owners(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> responses.OkResponse:
    return responses.OkResponse(owners_service.get_all_owners(db, skip=skip, limit=limit))


@owners_router.get("/{owner_id}", response_model=responses.OkResponse)
def get_owner(owner_id: int, db: Session = Depends(get_db)) -> responses.OkResponse:
    return responses.OkResponse(owners_service.get_owner(db, owner_id).__dict__)


@owners_router.post("/create", response_model=responses.CreatedResponse, status_code=status.HTTP_201_CREATED)
def create_owner(owner: schemas.Owner, db: Session = Depends(get_db)) -> responses.CreatedResponse:
    return responses.CreatedResponse(owners_service.create_owner(db, owner).__dict__)
