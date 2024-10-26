from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CustomerContactInfoSchema(BaseModel):
    contact_number: str
    email_address: str
    address: str


class CustomerSchema(BaseModel):
    name: str
    age: int
    contact_info: List[CustomerContactInfoSchema]
    is_disabled: bool
    medical_conditions: Optional[List[str]] = None


class CustomerResponseSchema(BaseModel):
    id: int
    created_at: datetime
    name: str
    age: int
    contact_info: List[CustomerContactInfoSchema]
    is_disabled: bool
    medical_conditions: Optional[List[str]] = None


class CustomerRentalsSchema(BaseModel):
    customer_id: int
    shoe_size: int
    rental_fee: float


class CustomerRentalsResponseSchema(BaseModel):
    id: int
    created_at: datetime
    customer_id: int
    rental_fee: str
    shoe_size: int
    rental_fee: float
    discount: int
    total_fee: float
