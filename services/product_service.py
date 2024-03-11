from typing import Type
from automapper import mapper

from sqlalchemy import asc
from sqlalchemy.orm import Session
from models import models
from schemas import schemas
from exceptions import exceptions


def get_all_products(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.ProductGet]:
    products_from_db: list[Type[models.Product]] = db.query(models.Product).order_by(asc(models.Product.id)).offset(
        skip).limit(limit).all()

    products_mapped: list[schemas.ProductGet] = []

    for product in products_from_db:
        product_dict: dict = product.__dict__

        product_dict["category"] = product.category.__dict__
        product_dict["owner"] = product.owner.__dict__

        products_mapped.append(mapper.to(schemas.ProductGet).map(product_dict))

    return products_mapped


def get_product(db: Session, product_id: int) -> schemas.ProductGet:
    product: models.Product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if product is None:
        raise exceptions.HTTPNotFoundException(detail="Product does not exists")

    product_db_dict: dict = product.__dict__
    product_db_dict["owner"] = product.owner.__dict__
    product_db_dict["category"] = product.category.__dict__

    product_schema: schemas.ProductGet = mapper.to(schemas.ProductGet).map(product_db_dict)

    return product_schema


def create_product(db: Session, product: schemas.Product) -> schemas.ProductGet:
    category_exists: Type[models.Category] = db.query(models.Category).filter(
        models.Category.id == product.category_id).first()

    if category_exists is None:
        raise exceptions.HTTPExceptionBadRequest(detail="Invalid category")

    owner_exists: Type[models.Owner] = db.query(models.Owner).filter(models.Owner.id == product.owner_id).first()

    if owner_exists is None:
        raise exceptions.HTTPExceptionBadRequest(detail="Invalid Owner")

    product_to_be_added = mapper.to(models.Product).map(product)

    db.add(product_to_be_added)
    db.commit()
    db.refresh(product_to_be_added)

    product_dict: dict = product_to_be_added.__dict__

    product_dict["category"] = product_to_be_added.category.__dict__
    product_dict["owner"] = product_to_be_added.owner.__dict__

    product_saved_mapped = mapper.to(schemas.ProductGet).map(product_dict)

    return product_saved_mapped
