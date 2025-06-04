import models
from database import engine


models.Base.metadata.create_all(bind=engine)



from fastapi import FastAPI

app = FastAPI()

 
@app.get("/")
def read_root():
    return {"message": "Task Tracker API is working!"}
