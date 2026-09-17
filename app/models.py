from pydantic import BaseModel, field_validator


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float


class ProductRequest(BaseModel):
    name: str
    description: str
    price: float

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("name is required")
        return value

    @field_validator("price")
    @classmethod
    def price_must_not_be_negative(cls, value: float) -> float:
        if value < 0:
            raise ValueError("price cannot be negative")
        return value
