from fastapi import HTTPException
from sqlalchemy import asc
from sqlalchemy.orm import Session
from typing import Type
from automapper import mapper

from models import models
from schemas import schemas
from exceptions import exceptions


def get_all_categories(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Category]:
    categories_db: list[Type[models.Category]] = db.query(models.Category).order_by(asc(models.Category.id)).offset(
        skip).limit(limit).all()

    categories_db_mapped: list[schemas.Category] = []

    for c in categories_db:
        dict_cat = c.__dict__
        dict_cat["owner"] = c.owner.__dict__
        categories_db_mapped.append(mapper.to(schemas.CategoryGet).map(dict_cat))

    return categories_db_mapped


def get_category_by_id(db: Session, category_id: int) -> schemas.Category:
    category_db: Type[models.Category] = db.query(models.Category).filter(models.Category.id == category_id).first()

    if category_db is None:
        raise HTTPException(status_code=404, detail="Category doesn't exists")
    category_dict = category_db.__dict__

    category_dict["owner"] = category_db.owner.__dict__

    category_mapped = mapper.to(schemas.CategoryGet).map(category_dict)

    return category_mapped


def create_category(db: Session, category: schemas.Category) -> schemas.CategoryGet:
    owner_from_db = db.query(models.Owner).filter(models.Owner.id == category.owner_id).first()

    if owner_from_db is None:
        raise exceptions.BadRequestException(status_code=400, detail="Invalid owner", status_text="test")

    category_save: models.Category = mapper.to(models.Category).map(category)

    db.add(category_save)
    db.commit()
    db.refresh(category_save)

    dict_category: dict = category_save.__dict__

    dict_category["owner"] = category_save.owner.__dict__

    category_saved_mapped: schemas.CategoryGet = mapper.to(schemas.CategoryGet).map(dict_category)

    return category_saved_mapped
