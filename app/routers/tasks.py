from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models,  utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Tasks'],
    prefix="/tasks"
)

@router.get('/', response_model=List[schemas.TaskBase])
def get_task(db: Session = Depends(get_db)):
    tasks = db.query(models.Tasks).all()

    if tasks is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks does not exits")
    
    return tasks


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    new_task = models.Tasks(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task