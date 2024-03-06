from typing import Optional

from pydantic import BaseModel, EmailStr


# Schemas for owners
class Owner(BaseModel):
    email: EmailStr
    name: str


class OwnerGet(BaseModel):
    id: int
    email: str
    name: str


# Schemas for categories
class Category(BaseModel):
    title: str
    description: str
    owner_id: int


class CategoryGet(BaseModel):
    id: int
    title: str
    description: str
    owner: OwnerGet
