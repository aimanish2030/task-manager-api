from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(
    title="Task Manager API",
    description="CRUD API built with FastAPI by Manish Kumar Pandit",
    version="1.0.0"
)

tasks_db = {}


class Task(BaseModel):
    title: str
    description: Optional[str] = ""
    completed: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


@app.get("/")
def home():
    return {
        "message": "Welcome to Task Manager API!",
        "developer": "Manish Kumar Pandit",
        "github": "aimanish2030",
        "docs": "Go to /docs to test the API"
    }


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    task_id = str(uuid.uuid4())
    tasks_db[task_id] = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }
    return {
        "message": "Task created successfully!",
        "task": tasks_db[task_id]
    }


@app.get("/tasks")
def get_all_tasks():
    if not tasks_db:
        return {"message": "No tasks found!", "tasks": []}
    return {
        "total_tasks": len(tasks_db),
        "tasks": list(tasks_db.values())
    }


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found!")
    return {"task": tasks_db[task_id]}


@app.put("/tasks/{task_id}")
def update_task(task_id: str, task_update: TaskUpdate):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found!")
    existing_task = tasks_db[task_id]
    if task_update.title is not None:
        existing_task["title"] = task_update.title
    if task_update.description is not None:
        existing_task["description"] = task_update.description
    if task_update.completed is not None:
        existing_task["completed"] = task_update.completed
    tasks_db[task_id] = existing_task
    return {
        "message": "Task updated successfully!",
        "task": tasks_db[task_id]
    }


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found!")
    deleted_task = tasks_db.pop(task_id)
    return {
        "message": "Task deleted successfully!",
        "deleted_task": deleted_task
    }


@app.get("/tasks/filter/completed")
def get_completed_tasks():
    completed = [t for t in tasks_db.values() if t["completed"] == True]
    return {
        "total_completed": len(completed),
        "tasks": completed
    }


@app.get("/tasks/filter/pending")
def get_pending_tasks():
    pending = [t for t in tasks_db.values() if t["completed"] == False]
    return {
        "total_pending": len(pending),
        "tasks": pending
    }