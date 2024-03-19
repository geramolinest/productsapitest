from pydantic import BaseModel, EmailStr, field_validator


# Schemas for owners
class Owner(BaseModel):
    email: EmailStr
    name: str

    @field_validator("name", mode="before")
    @classmethod
    def title_name(cls, name_param: str) -> str:
        return name_param.title()


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


class CategoryGetProduct(BaseModel):
    id: int
    title: str
    description: str


# Schemas for products
class Product(BaseModel):
    title: str
    description: str
    price: float
    category_id: int
    owner_id: int


class ProductGet(BaseModel):
    id: int
    title: str
    description: str
    price: float
    category: CategoryGetProduct
    owner: OwnerGet


# Validation error schema
class ValidationErrorSchema(BaseModel):
    field: str
    error: str
