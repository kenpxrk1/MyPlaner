import datetime
from repositories.task import TaskRepository
from schemas.task import TaskCreate, TaskRead


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    
    async def create_task(self, request: TaskCreate, user_id):
        new_task = await self.repository.create_task(request, user_id)
        return new_task
    

    async def get_all_tasks(self, user_id: int) -> TaskRead:
        all_tasks = await self.repository.get_all_tasks(user_id)
        return all_tasks
    

    async def get_tasks_by_date(self, user_id: int, date: datetime.date) -> TaskRead:
        all_tasks = await self.repository.get_tasks_by_date(user_id, date)
        return all_tasks
    

