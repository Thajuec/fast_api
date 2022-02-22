from typing import List

from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str

class Blogchild(Blog):
    class Config():
        orm_mode = True



class User(BaseModel):
    name: str
    email: str
    password: str


class Showuser(BaseModel):
    name: str
    email: str
    blog: List[Blogchild]=[]

    class Config():
        orm_mode = True


class Showblog(BaseModel):
    title: str
    body: str
    author: Showuser

    class Config():
        orm_mode = True