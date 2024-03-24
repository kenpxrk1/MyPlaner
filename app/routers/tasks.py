from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models,  utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Tasks'],
    prefix="/tasks"
)

@router.get('/', response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    tasks = db.query(models.Tasks).filter(models.Tasks.owner_id == current_user.id).all()

    if tasks is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks does not exits")
    
    return tasks


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    new_task = models.Tasks(owner_id = current_user.id, **task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.put("/{id}", response_model=schemas.Task)
def update_task(id: int, updated_post: schemas.TaskCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    task_query = db.query(models.Tasks).filter(models.Tasks.id == id)
    task = task_query.first()

    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"task with id: {id} does not exist")

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform request action")
    
    task_query.update(updated_post.model_dump(), synchronize_session=False)

    db.commit()

    return task_query.first()



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    task_query = db.query(models.Tasks).filter(models.Tasks.id == id)
    task = task_query.first()

    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"task with id: {id} does not exist")

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform request action")

    task_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)    