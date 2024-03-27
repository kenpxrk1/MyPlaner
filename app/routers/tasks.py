import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract
from .. import schemas, database, models,  utils, oauth2
from ..database import get_db

"""CONST DATETIME VARIABLE BLOCK"""

today_date = datetime.datetime.today().strftime('%Y-%m-%d')
current_month_obj = datetime.datetime.strptime(today_date, '%Y-%m-%d')
current_month = current_month_obj.month


"""CONST DATETIME VARIABLE BLOCK"""



router = APIRouter(
    tags=['Tasks'],
    prefix="/tasks"
)

""" TAKE AUTH USER OWN TASKS ONLY (TODAY)) """

@router.get('/today', response_model=List[schemas.Task])
def get_today_tasks(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    tasks = db.query(models.Tasks).filter(models.Tasks.owner_id == current_user.id).filter(models.Tasks.starts_at == today_date).all()

    if tasks is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks does not exits")
    
    return tasks

""" TAKE AUTH USER OWN TASKS (ALL) """

@router.get('/all', response_model=List[schemas.Task])
def get_all_tasks(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    tasks = db.query(models.Tasks).filter(models.Tasks.owner_id == current_user.id).all()

    if tasks is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks does not exits")
    
    return tasks

""" TAKE AUTH USER OWN TASKS (BY CURRENT MONTH) """

@router.get('/current_month', response_model=List[schemas.Task])
def get_current_month_tasks(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    tasks = db.query(models.Tasks).filter(models.Tasks.owner_id == current_user.id).filter(extract(
        'month', models.Tasks.starts_at) == current_month).all()

    if tasks is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks does not exits")
    
    return tasks

""" TAKE AUTH USER OWN TASKS (BY MONTH) """

@router.get('/month', response_model=List[schemas.Task])
def get_month_tasks(date_query: datetime.date, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    query_month_obj = datetime.datetime.strptime(date_query, '%Y-%m-%d')
    query_month = query_month_obj.month
    tasks = db.query(models.Tasks).filter(models.Tasks.owner_id == current_user.id).filter(extract(
        'month', models.Tasks.starts_at) == query_month).all()

    if tasks is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tasks does not exits")
    
    return tasks

""" GET AUTH USER OWN TASKS BY DATE """

@router.get('/tasks_by_date/{date}', response_model=List[schemas.Task])
def get_tasks_by_date(date: datetime.date, db: Session = Depends(get_db), 
                      current_user: int = Depends(oauth2.get_current_user)):
    
    tasks = db.query(models.Tasks).filter(models.Tasks.owner_id == current_user.id).filter(
        models.Tasks.starts_at == date)
    
    if tasks is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tasks for {date} does not exist")
    
    return tasks


"""CREATES TASKS BY ONLY AUTH USER AND AUTOMATICALLY CONNECTED TO HIMSELF"""

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
    new_task = models.Tasks(owner_id = current_user.id, **task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

"""UPDATES TASK BY PATH PARAMETER"""

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

""" DELETE TASK BY PATH PARAMETERS """

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



""" SEARCHING """


@router.get('/search/{query}', response_model=List[schemas.Task])
def search(query: str, db: Session = Depends(get_db), 
           current_user: int = Depends(oauth2.get_current_user)):
    search_result = db.query(models.Tasks).filter(models.Tasks.owner_id == current_user.id).filter(models.Tasks.title.ilike(f"%{query}%")).all()
    return search_result