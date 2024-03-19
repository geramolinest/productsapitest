from sqlalchemy import asc
from sqlalchemy.orm import Session
from typing import Type
from automapper import mapper

from models import models
from schemas import schemas
from exceptions import exceptions


def get_all_owners(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.OwnerGet]:
    owners_db: list[Type[models.Owner]] = db.query(models.Owner).order_by(asc(models.Owner.id)).offset(skip).limit(
        limit).all()

    owners_mapped: list[schemas.OwnerGet] = []

    for owner_db in owners_db:
        owners_mapped.append(mapper.to(schemas.OwnerGet).map(owner_db))

    return owners_mapped


def get_owner(db: Session, owner_id: int) -> schemas.OwnerGet:
    owner_db: Type[models.Owner] = db.query(models.Owner).filter(models.Owner.id == owner_id).first()

    if owner_db is None:
        raise exceptions.HTTPNotFoundException(detail="Owner does not exists")

    owner_mapped: schemas.OwnerGet = mapper.to(schemas.OwnerGet).map(owner_db)

    return owner_mapped


def create_owner(db: Session, owner: schemas.Owner) -> schemas.OwnerGet:
    owner_mapped: models.Owner = mapper.to(models.Owner).map(owner)

    db.add(owner_mapped)
    db.commit()
    db.refresh(owner_mapped)

    owner_mapped_saved: schemas.OwnerGet = mapper.to(schemas.OwnerGet).map(owner_mapped)

    return owner_mapped_saved


def update_owner(db: Session, owner_id: int, owner: schemas.Owner) -> schemas.OwnerGet:
    owner_from_db: Type[models.Owner] = db.query(models.Owner).filter(models.Owner.id == owner_id).first()

    if owner_from_db is None:
        raise exceptions.HTTPExceptionBadRequest(detail="Invalid owner")

    owner_from_db.email = owner.email
    owner_from_db.name = owner.name.title()

    db.commit()
    db.refresh(owner_from_db)

    owner_mapped_saved: schemas.OwnerGet = mapper.to(schemas.OwnerGet).map(owner_from_db)

    return owner_mapped_saved


def delete_owner(db: Session, owner_id: int) -> int:
    owner_from_db: Type[models.Owner] = db.query(models.Owner).filter(models.Owner.id == owner_id).first()

    if owner_from_db is None:
        raise exceptions.HTTPExceptionBadRequest(detail="Invalid owner")

    has_category: Type[models.Category] = db.query(models.Category).filter(models.Category.owner_id == owner_id).first()

    if has_category is not None:
        raise exceptions.HTTPExceptionBadRequest(detail="Owner has a an assigned category")

    has_product: Type[models.Product] = db.query(models.Product).filter(models.Product.owner_id == owner_id).first()

    if has_product is not None:
        raise exceptions.HTTPExceptionBadRequest(detail="Owner has a an assigned product")

    db.delete(owner_from_db)
    db.commit()

    return owner_id
