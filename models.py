from pydantic import BaseModel


class User(BaseModel):
    name:str
    email:str
    phone:str
    is_officer:bool
    department:str
    location:str

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
