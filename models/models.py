import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.DBConnection import Base


class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String, unique=False, index=False, default="")
    categories = relationship("Category", back_populates="owner")
    products = relationship("Product", back_populates="owner")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, default="")
    description = Column(String, nullable=False, default="")
    owner_id = Column(Integer, ForeignKey("owners.id"))
    owner = relationship(Owner, uselist=False, back_populates="categories")
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    title = Column(String, default="")
    description = Column(String, default="")
    price = Column(Float, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship(Category, uselist=False, back_populates="products")
    owner_id = Column(Integer, ForeignKey("owners.id"))
    owner = relationship(Owner, uselist=False, back_populates="products")
