from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    title: str

class Task(BaseModel):
    id: int
    title: str
    done: bool

    class Config:
        orm_mode = True
