from fastapi import FastAPI, Request,status
from starlette.status import HTTP_302_FOUND

from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
# from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)
# templates = Jinja2Templates(directory="todoApp/templates")
app.mount("/static", StaticFiles(directory="todoApp/static"),name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=HTTP_302_FOUND)

    # return templates.TemplateResponse(
    #     request=request,
    #     name="home.html",
    #     context={"request": request}
    # )


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# db_dependency = Annotated[Session, Depends(get_db)]
#
# class TodoRequest(BaseModel):
#     title: str = Field(min_length=3)
#     description: str = Field(min_length=3,max_length=100)
#     priority: int = Field(gt=0,lt=6)
#     complete: bool
#
# @app.get("/todos",status_code=status.HTTP_200_OK)
# async def read_all(db: db_dependency):
#     # return db.execute(select(Todos)).scalars().all()
#     return db.query(Todos).all()
#
# @app.get("/todoo/{todo_id}", status_code=status.HTTP_200_OK)
# async def read_todo(db:db_dependency, todo_id : int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is not None:
#         return todo_model
#     raise HTTPException(status_code=404,detail='Todo not found.')
#
#
# @app.post("/todo", status_code=status.HTTP_201_CREATED)
# async def create_todo(db:db_dependency, todo_request: TodoRequest):
#     todo_model = Todos(**todo_request.model_dump())
#     db.add(todo_model)
#     db.commit()
#
# @app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def update_todo(db:db_dependency,todo_request: TodoRequest,todo_id: int =Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail= 'Todo not found.')
#
#     todo_model.title = todo_request.title
#     todo_model.description = todo_request.description
#     todo_model.priority = todo_request.priority
#     todo_model.complete = todo_request.complete
#
#     db.add(todo_model)
#     db.commit()
#
#
# @app.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(db: db_dependency, todo_id: int= Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail= 'Todo not found.')
#     db.query(Todos).filter(Todos.id == todo_id).delete()
#     db.commit()
