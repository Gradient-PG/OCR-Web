from fastapi import APIRouter, HTTPException

from ..service.task import TaskService

router = APIRouter(
    prefix='/task',
    tags=['task'],
    responses={404: {'description': 'Not found'}},
)

# Dependency function to provide TaskService
def get_task_service() -> TaskService:
    return TaskService()


@router.get('/status/{task_id}', summary='Task status', description='Returns a task status')
async def status(task_id: str, task_service: TaskService = Depends(get_task_service)):
    """Endpoint to fetch the status of a task.

    in: task_id
    """
    try:
        task = await task_service.get_task(task_id)
        return {'status': task['status'], 'progress': task['progress']}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get('/result/{task_id}', summary='Task result', description='Returns a task result')
async def result(task_id: str):
    """Endpoint to fetch the result of a task."""
    try:
        task = await task_service.get_task(task_id)
        return task['result']
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get('/task/{task_id}', summary='Task result', description='Returns a task result')
async def task(task_id: str):
    """Endpoint to fetch the result of a task."""
    try:
        task = await task_service.get_task(task_id)
        return task
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e