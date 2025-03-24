from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    name: str
    email: str
    password: str
    aadhar: str
    phone_number: str
    location: str
    is_officer: bool

class LoginData(BaseModel):
    email: str
    password: str

class News(BaseModel):
    email:str
    title:str
    description:str
    department:str
    location:str

class Query(BaseModel):
    email:str
    title:str
    description:str
    department:str
    location:str
    
class Answer(BaseModel):
    query_id: str  # query_id will be assigned when the query is created
    email: str
    response: str


