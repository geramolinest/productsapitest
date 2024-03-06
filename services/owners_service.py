from fastapi import HTTPException
from sqlalchemy import asc
from sqlalchemy.orm import Session
from typing import Type
from automapper import mapper

from models import models
from schemas import schemas


def get_all_owners(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.OwnerGet]:

    owners_db: list[Type[models.Owner]] = db.query(models.Owner).order_by(asc(models.Owner.id)).offset(skip).limit(limit).all()

    owners_mapped: list[schemas.OwnerGet] = []

    for owner_db in owners_db:
        owners_mapped.append(mapper.to(schemas.OwnerGet).map(owner_db))

    return owners_mapped


def get_owner(db: Session, owner_id: int) -> schemas.OwnerGet:

    owner_db: Type[models.Owner] = db.query(models.Owner).filter(models.Owner.id == owner_id).first()

    if owner_db is None:
        raise HTTPException(status_code=404, detail="Owner doesn't exists")

    owner_mapped: schemas.OwnerGet = mapper.to(schemas.OwnerGet).map(owner_db)

    return owner_mapped


def create_owner(db: Session, owner: schemas.Owner) -> schemas.OwnerGet:

    owner_mapped = mapper.to(models.Owner).map(owner)

    db.add(owner_mapped)
    db.commit()
    db.refresh(owner_mapped)

    owner_mapped_saved: schemas.OwnerGet = mapper.to(schemas.OwnerGet).map(owner_mapped)

    return owner_mapped_saved
