from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/latest", response_model=schemas.User)
def get_users(db: Session = Depends(get_db)):
    user = db.query(models.User).first()
    return user

@router.get("/{id}", response_model=schemas.User)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id '{id}' was not found."
        )
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.User)
def update_user(id: int, user: schemas.UserBase, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id)
    old_user = user_query.first()

    if old_user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id '{id}' was not found."
        )

    user_query.update(user.dict(), synchronize_session=False)
    db.commit() 

    return user_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id '{id}' was not found."
        )
    
    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)