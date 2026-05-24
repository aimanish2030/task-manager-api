from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Task Manager API",
    description="CRUD API with MongoDB built by Manish Kumar Pandit",
    version="2.0.0"
)

MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["taskmanager"]
collection = db["tasks"]


class Task(BaseModel):
    title: str
    description: Optional[str] = ""
    completed: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "completed": task["completed"]
    }


@app.get("/")
async def home():
    return {
        "message": "Welcome to Task Manager API v2.0!",
        "developer": "Manish Kumar Pandit",
        "github": "aimanish2030",
        "database": "MongoDB Atlas",
        "docs": "Go to /docs to test the API"
    }


@app.post("/tasks", status_code=201)
async def create_task(task: Task):
    task_data = task.dict()
    result = await collection.insert_one(task_data)
    new_task = await collection.find_one({"_id": result.inserted_id})
    return {
        "message": "Task created successfully!",
        "task": task_helper(new_task)
    }


@app.get("/tasks")
async def get_all_tasks():
    tasks = []
    async for task in collection.find():
        tasks.append(task_helper(task))
    if not tasks:
        return {"message": "No tasks found!", "tasks": []}
    return {
        "total_tasks": len(tasks),
        "tasks": tasks
    }


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    try:
        task = await collection.find_one({"_id": ObjectId(task_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID!")
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    return {"task": task_helper(task)}


@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task_update: TaskUpdate):
    try:
        update_data = {k: v for k, v in task_update.dict().items() if v is not None}
        result = await collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID!")
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found!")
    updated_task = await collection.find_one({"_id": ObjectId(task_id)})
    return {
        "message": "Task updated successfully!",
        "task": task_helper(updated_task)
    }


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    try:
        task = await collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found!")
        await collection.delete_one({"_id": ObjectId(task_id)})
    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID!")
    return {
        "message": "Task deleted successfully!",
        "deleted_task": task_helper(task)
    }


@app.get("/tasks/filter/completed")
async def get_completed_tasks():
    tasks = []
    async for task in collection.find({"completed": True}):
        tasks.append(task_helper(task))
    return {"total_completed": len(tasks), "tasks": tasks}


@app.get("/tasks/filter/pending")
async def get_pending_tasks():
    tasks = []
    async for task in collection.find({"completed": False}):
        tasks.append(task_helper(task))
    return {"total_pending": len(tasks), "tasks": tasks}