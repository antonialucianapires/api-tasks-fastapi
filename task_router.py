from typing import List

import csv
import io

from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette import status
from starlette.responses import Response

from task_model import Task

router = APIRouter()

tasks: list[Task] = [
    Task(id=1, title="Ler documentação"),
    Task(id=2, title="Escrever testes", is_active=True),
]

@router.get("/tasks", response_model=List[Task])
async def list_tasks():
    return tasks

@router.post("/tasks")
async def create_task(task: Task):
    next_id = max((t.id or 0 for t in tasks), default=0) + 1
    task.id = next_id
    tasks.append(task)
    return task

@router.post("/tasks/upload", status_code=status.HTTP_201_CREATED)
async def upload_tasks(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))

    new_tasks = []
    start_id = max((t.id or 0 for t in tasks), default=0) + 1

    for index, row in enumerate(reader):
        title = row["title"]
        is_active = row["is_active"].strip().lower() == "true"

        task = Task(
            id=start_id + index,
            title=title,
            is_active=is_active
        )

        new_tasks.append(task)

    tasks.extend(new_tasks)
    return {"detail": f"{len(new_tasks)} tasks criadas"}

@router.patch("/tasks/{id}/activate")
async def activate_task(id: int):
    for task in tasks:
        if task.id == id:
            task.is_active = True
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
