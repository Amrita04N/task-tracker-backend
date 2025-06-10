from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, database
from app.auth import get_current_user  # Assuming you're using JWT for authentication

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/", response_model=schemas.TaskOut)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        new_task = models.Task(**task.dict(), owner_id=current_user.id)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")

@router.get("/", response_model=List[schemas.TaskOut])
def get_tasks(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    updated_task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task.title = updated_task.title
        task.description = updated_task.description
        task.completed = updated_task.completed
        db.commit()
        db.refresh(task)
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        db.delete(task)
        db.commit()
        return {"detail": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")
