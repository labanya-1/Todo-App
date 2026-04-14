from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter,Path,HTTPException, Depends
from starlette import status
from ..models import Todos
from ..models import Users, Todos
from ..database import SessionLocal
from typing import Annotated
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin'])

# models.Base.metadata.create_all(bind=engine)

# app.include_router(auth.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/todo", status_code= status.HTTP_200_OK)
async def read_all(user:user_dependency, db:db_dependency):
    if user is None or user.get('user_role')!= 'admin':
        raise HTTPException(status_code=401, detail='authentication Failed')
    return db.query(Todos).all()

# @router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(user:user_dependency, db:db_dependency,todo_id: int = Path(gt=0)):
#     if user is None or user.get('user_role')!='admin':
#         raise HTTPException(status_code=401, detail= 'Authentication Failed')
#     todo_model =db.query(Todos).filter(Todos.id ==todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404,detail='Todo not found')
#     db.query(Todos).filter(Todos.id == todo_id).delete()
#     db.commit()

@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    current_user: user_dependency,
    db: db_dependency,
    user_id: int = Path(gt=0)
):
    if current_user is None or current_user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user_id).first()

    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(Todos).filter(Todos.owner_id == user_id).delete()
    db.delete(user_model)
    db.commit()