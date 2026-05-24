from fastapi import FastAPI, HTTPException, Depends
from bson import ObjectId
from database import task_collection
from models import Task, TaskUpdate
from auth import router as auth_router, get_current_user

app = FastAPI(
    title="Task Manager API",
    description="CRUD API with MongoDB + JWT Auth by Manish Kumar Pandit",
    version="3.0.0"
)

app.include_router(auth_router, tags=["Authentication"])


def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "completed": task["completed"]
    }


@app.get("/", tags=["Home"])
async def home():
    return {
        "message": "Welcome to Task Manager API v3.0!",
        "developer": "Manish Kumar Pandit",
        "github": "aimanish2030",
        "database": "MongoDB Atlas",
        "auth": "JWT Authentication",
        "docs": "Go to /docs to test the API"
    }


@app.post("/tasks", status_code=201, tags=["Tasks"])
async def create_task(task: Task, current_user=Depends(get_current_user)):
    task_data = task.dict()
    task_data["owner"] = current_user["email"]
    result = await task_collection.insert_one(task_data)
    new_task = await task_collection.find_one({"_id": result.inserted_id})
    return {"message": "Task created successfully!", "task": task_helper(new_task)}


@app.get("/tasks", tags=["Tasks"])
async def get_all_tasks(current_user=Depends(get_current_user)):
    tasks = []
    async for task in task_collection.find({"owner": current_user["email"]}):
        tasks.append(task_helper(task))
    if not tasks:
        return {"message": "No tasks found!", "tasks": []}
    return {"total_tasks": len(tasks), "tasks": tasks}


@app.get("/tasks/{task_id}", tags=["Tasks"])
async def get_task(task_id: str, current_user=Depends(get_current_user)):
    try:
        task = await task_collection.find_one({"_id": ObjectId(task_id), "owner": current_user["email"]})
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID!")
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    return {"task": task_helper(task)}


@app.put("/tasks/{task_id}", tags=["Tasks"])
async def update_task(task_id: str, task_update: TaskUpdate, current_user=Depends(get_current_user)):
    try:
        update_data = {k: v for k, v in task_update.dict().items() if v is not None}
        result = await task_collection.update_one(
            {"_id": ObjectId(task_id), "owner": current_user["email"]},
            {"$set": update_data}
        )
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID!")
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found!")
    updated_task = await task_collection.find_one({"_id": ObjectId(task_id)})
    return {"message": "Task updated successfully!", "task": task_helper(updated_task)}


@app.delete("/tasks/{task_id}", tags=["Tasks"])
async def delete_task(task_id: str, current_user=Depends(get_current_user)):
    try:
        task = await task_collection.find_one({"_id": ObjectId(task_id), "owner": current_user["email"]})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found!")
        await task_collection.delete_one({"_id": ObjectId(task_id)})
    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID!")
    return {"message": "Task deleted successfully!", "deleted_task": task_helper(task)}


@app.get("/tasks/filter/completed", tags=["Tasks"])
async def get_completed_tasks(current_user=Depends(get_current_user)):
    tasks = []
    async for task in task_collection.find({"completed": True, "owner": current_user["email"]}):
        tasks.append(task_helper(task))
    return {"total_completed": len(tasks), "tasks": tasks}


@app.get("/tasks/filter/pending", tags=["Tasks"])
async def get_pending_tasks(current_user=Depends(get_current_user)):
    tasks = []
    async for task in task_collection.find({"completed": False, "owner": current_user["email"]}):
        tasks.append(task_helper(task))
    return {"total_pending": len(tasks), "tasks": tasks}