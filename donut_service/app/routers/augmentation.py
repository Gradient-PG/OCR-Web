from fastapi import APIRouter, HTTPException, Depends, Body
import os

from ..services.task import TaskService

from ..repository.redis.task import TaskRepository

from ..model.task import TaskRequest
from typing import List

router = APIRouter(
    prefix='/augmentation',
    tags=['augmentation'],
    responses={404: {'description': 'Not found'}},
)

def get_task_repository() -> TaskRepository:
    return TaskRepository(os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0'))

# Dependency function to provide TaskService
def get_task_service(task_repository: TaskRepository = Depends(get_task_repository)) -> TaskService:
    return TaskService(task_repository)

@router.post('/task', summary='Task creation', description='Creates a new task')
async def create_task(
    requests: List[TaskRequest] = Body(...),
    task_service: TaskService = Depends(get_task_service)
):
    """Endpoint to create a new task."""
    try:
        task_id = await task_service.create_task('augmentation', requests)
        return {'task_id': task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@router.get('/status/{task_id}', summary='Task status', description='Returns a task status')
async def status(task_id: str, task_service: TaskService = Depends(get_task_service)):
    """Endpoint to fetch the status of a task.

    in: task_id
    """
    try:
        task = await task_service.get_task(task_id)
        if task.task_type != 'augmentation':
            raise HTTPException(status_code=400, detail='Task type is not augmentation')
        return {'status': task.status}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

