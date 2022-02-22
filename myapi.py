from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# @app.get("/")
#
# def home():
#     return {"data": "hello"}
#
# @app.get("/about")
#
# def about():
#     return {"about":"About"}

inventory = {
    1: {
        "name": "milk",
        "price": 20
    },
    2: {
        "name": "Fruit",
        "price": 10
    }
}

@app.get("/getitem/{item_id}")

def get_item(item_id: int):
    return inventory[item_id]

@app.get("/get_id/{id}")
def get_id(id: int):
    return {"user id":id}

#query parameters
# like ?limit=,published

@app.get("/blog")
def index(limit, published: bool):
    if published:
        return {"data":f'{limit} published blogs from the db'}
    else:
        return {"data": f'{limit}  blogs from the db'}

# passing default value
@app.get("/blog1")
def index1(limit=10, published: bool=True, sort: Optional[str]=None):
    if published:
        return {"data":f'{limit} published blogs from the db'}
    else:
        return {"data": f'{limit}  blogs from the db'}


class Blog(BaseModel):
    title: str
    body: str
    published: bool

@app.post("/blog2")
def create_blog(request: Blog):
    return {"title":{request.title}, "body": {request.body}, "published": {request.published}}