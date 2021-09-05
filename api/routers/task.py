from fastapi import APIRouter, Depends, HTTPException

import api.cruds.task as task_crud
from api.db import get_db, AsyncSession

from typing import List
import api.schemas.task as task_schema

router = APIRouter()


# @router.get("/tasks", response_model= List[task_schema.Task])
# async def list_task():
#     return [task_schema.Task(id=1, title="1つ目のタスク")]

@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return await task_crud.get_tasks_with_done(db)

# @router.post("/tasks", response_model = task_schema.TaskCreateResponse)
# #task_bodyがリクエストボディ
# async def create_task(task_body: task_schema.TaskCreate):
#     # dict インスタンスに対して先頭に ** をつけることで、title=task_body.title, done=task_body.done
#     return task_schema.TaskCreateResponse(id=1, **task_body.dict())

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create_task(
    task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    return await task_crud.create_task(db, task_body)


# @router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
# async def update_task(task_id: int, task_body: task_schema.TaskCreate):
#     return task_schema.TaskCreateResponse(id = task_id, **task_body.dict())
    

@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.update_task(db, task_body, original=task)



# @router.delete("/tasks/{task_id}", response_model=None)
# async def delete_task(task_id: int):
#     return

@router.delete("/tasks/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete_task(db, original=task)