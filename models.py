from pydantic import BaseModel, Field
from typing import Optional, List


# Models
class Address(BaseModel):
    city: str
    country: str


class StudentCreate(BaseModel):
    name: str
    age: int
    address: Address


class StudentResponse(BaseModel):
    name: str
    age: int
    address: Address


class StudentShortResponse(BaseModel):
    name: str
    age: int


class StudentListResponse(BaseModel):
    data: List[StudentShortResponse]


class AddressUpdate(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[AddressUpdate] = None
