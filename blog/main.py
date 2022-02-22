from typing import List

from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models
from .database import engine, SessionLocal
from .schemas import Showblog, Showuser
from .hashing import Hash

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(engine)


@app.post('/create', status_code=status.HTTP_201_CREATED, tags=['Blog'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/view', tags=['Blog'])
def create(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/view/{id}', status_code=200, response_model=Showblog, tags=['Blog'])
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"details of the given id {id} is not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"details of the given id {id} is not found")
    return blog


@app.delete('/delete/{id}', status_code=200, tags=['Blog'])
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with this id {id} is not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Deleted Successfully"


@app.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with this id {id} is not found")
    blog.update(request.dict())
    db.commit()
    return "Updated successfully"


@app.post('/user', status_code=status.HTTP_201_CREATED, tags=['User'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.encrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/view_user',status_code=status.HTTP_302_FOUND, response_model=List[Showuser], tags=['User'])
def view_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user


@app.get('/view_user/{id}', status_code=status.HTTP_302_FOUND, response_model=Showuser, tags=['User'])
def view_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"details of the given id {id} is not found")
    return user