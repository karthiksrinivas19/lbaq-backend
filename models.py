from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str
    aadhar: str
    phone_number: str
    location: str
    is_officer: bool

class News(BaseModel):
    title:str
    description:str
    department:str
    location:str

class Query(BaseModel):
    title:str
    description:str
    department:str
    location:str
