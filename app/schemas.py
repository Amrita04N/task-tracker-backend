from pydantic import BaseModel

# For user operations
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # For Pydantic v2

# For task operations
class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class TaskOut(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


