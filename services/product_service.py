from typing import Type

from sqlalchemy.orm import Session
from models import models


def get_all_products(db: Session) -> list[Type[models.Product]]:
    return db.query(models.Product).all()


def get_product(db: Session, product_id: int) -> models.Product:
    product: models.Product = db.query(models.Product).filter(models.Product.id == product_id).first()
    return product


def create_product(db: Session, product: models.Product) -> models.Product:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
