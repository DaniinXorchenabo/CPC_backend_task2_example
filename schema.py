from typing import Optional
from pydantic import BaseModel, EmailStr, validator


class BookOutForAuthor(BaseModel):
    id: int
    page_count: int
    name: str
    prise: Optional[float]
    # author: ???

    class Config:
        orm_mode = True


class AuthorOut(BaseModel):
    id: int
    name: Optional[str]
    surname: str
    age: Optional[int]
    email: EmailStr
    login: str
    books: list[BookOutForAuthor]

    @validator('books', pre=True, allow_reuse=True)
    def pony_set_to_list(cls, values):
        new_values = list()
        for v in values:
            if hasattr(v, "to_dict"):
                new_values.append(v.to_dict())
        return new_values

    class Config:
        orm_mode = True


class EditAuthor(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    age: Optional[int]
    email: Optional[EmailStr]
    login: Optional[str]
    books: Optional[list[int]]


class CreateBook(BaseModel):
    id: int
    page_count: int
    name: str
    prise: Optional[float]
    author: int


class CreateAuthor(BaseModel):
    id: int
    name: Optional[str]
    surname: str
    age: Optional[int]
    email: EmailStr
    login: str

    class Config:
        orm_mode = True


class EditBook(BaseModel):
    page_count: Optional[int]
    name: Optional[str]
    prise: Optional[float]
    author: Optional[int]


class AuthorOutForBook(BaseModel):
    id: int
    name: Optional[str]
    surname: str
    age: Optional[int]
    email: EmailStr
    login: str


class OutBookYet(BaseModel):
    id: int
    page_count: int
    name: str
    prise: Optional[float]
    author: AuthorOutForBook

    @validator('author', pre=True, allow_reuse=True)
    def pony_set_to_list(cls, value):
        if hasattr(value, "to_dict"):
            value = value.to_dict()
        return value

    class Config:
        orm_mode = True

