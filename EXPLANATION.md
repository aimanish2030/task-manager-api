# 📖 TASK MANAGER API — CODE EXPLANATION
### By Manish Kumar Pandit | explanation!

---

## 1. IMPORTS — Kya kya mangaya hai?

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
```

**FastAPI** → Yeh main framework hai. Isi se poori API banti hai.

**HTTPException** → Jab koi galti ho (jaise task na mile) toh proper error dene ke liye. 
Jaise: "Task not found!" wala 404 error.

**BaseModel** → Pydantic ka part hai. Isse hum define karte hain ki 
data ka structure kaisa hoga. Matlab user kya kya field bhej sakta hai.

**Optional** → Iska matlab hai "yeh field dena zaroori nahi". 
Jaise description — task mein dena chahte ho toh do, nahi toh mat do.

**uuid** → Unique ID banane ke liye. Har task ko ek alag ID milti hai 
jaise Aadhar card number — kisi ka same nahi hota.

---

## 2. APP INITIALIZE

```python
app = FastAPI(
    title="Task Manager API",
    description="CRUD API built with FastAPI by Manish Kumar Pandit",
    version="1.0.0"
)
```

Yahan FastAPI ka ek object banaya jiska naam `app` hai.
`title`, `description`, `version` — yeh sab /docs page pe dikhta hai.
Jab tune browser mein /docs khola tha — wahan "Task Manager API" likha tha — woh yahan se aaya!

---

## 3. DATABASE (In-Memory)

```python
tasks_db = {}
```

Yeh ek simple Python dictionary hai — yahi hamara "database" hai abhi ke liye.
Tasks isme store hote hain RAM mein.

⚠️ **Important:** Server band karo toh sab data chala jaata hai.
Real projects mein MongoDB ya PostgreSQL use hota hai permanent storage ke liye.

Example mein aise dikhta hai andar:
```python
{
  "abc-123": {"id": "abc-123", "title": "Learn FastAPI", "completed": false},
  "def-456": {"id": "def-456", "title": "Build Project",  "completed": true}
}
```

---

## 4. MODELS — Data ka structure

### Task Model (naya task banane ke liye)
```python
class Task(BaseModel):
    title: str
    description: Optional[str] = ""
    completed: bool = False
```

`title: str` → title string hona chahiye, dena zaroori hai
`description: Optional[str] = ""` → dena zaroori nahi, default empty string
`completed: bool = False` → True ya False, default False (matlab pending)

Agar koi number bheje title mein — FastAPI automatically error dega!
Yeh Pydantic ka kaam hai — validation karna.

### TaskUpdate Model (update karne ke liye)
```python
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
```

Yahan sab Optional hai kyunki update mein sirf woh field bhejo jo change karni hai.
Jaise sirf `completed: true` bheja toh sirf wahi update hoga, baaki same rahega.

---

## 5. ROUTES — Kaunsa URL pe kya hoga

### Decorator kya hota hai?
```python
@app.get("/tasks")
def get_all_tasks():
```

`@app.get("/tasks")` → Yeh decorator hai.
Matlab: "Jab koi /tasks pe GET request bheje, toh neeche wala function chalao."

Yeh ek tarah ka signboard hai — "is raste pe aa toh yeh kaam hoga."

---

## 6. HOME ROUTE

```python
@app.get("/")
def home():
    return {
        "message": "Welcome to Task Manager API!",
        ...
    }
```

Jab koi http://127.0.0.1:8000/ kholta hai toh yeh function chalta hai
aur yeh dictionary JSON banakar wapas bhejta hai.

---

## 7. CREATE TASK (POST)

```python
@app.post("/tasks", status_code=201)
def create_task(task: Task):
    task_id = str(uuid.uuid4())
    tasks_db[task_id] = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }
    return {"message": "Task created successfully!", "task": tasks_db[task_id]}
```

`status_code=201` → 201 ka matlab "Successfully Created" hota hai
`uuid.uuid4()` → Random unique ID generate karta hai
`task.title` → User ne jo title bheja, woh yahan aata hai
`tasks_db[task_id] = {...}` → Dictionary mein save kar diya

---

## 8. READ ALL TASKS (GET)

```python
@app.get("/tasks")
def get_all_tasks():
    if not tasks_db:
        return {"message": "No tasks found!", "tasks": []}
    return {
        "total_tasks": len(tasks_db),
        "tasks": list(tasks_db.values())
    }
```

`if not tasks_db` → Agar dictionary empty hai toh "No tasks found" bolo
`len(tasks_db)` → Kitne tasks hain count karo
`tasks_db.values()` → Dictionary ki saari values (tasks) nikalo

---

## 9. READ ONE TASK (GET by ID)

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found!")
    return {"task": tasks_db[task_id]}
```

`{task_id}` → URL mein jo ID dali, woh yahan aati hai
`if task_id not in tasks_db` → Agar woh ID dictionary mein nahi hai
`raise HTTPException(404)` → 404 error bhejo — "Task not found!"
`tasks_db[task_id]` → Woh specific task nikalo ID se

---

## 10. UPDATE TASK (PUT)

```python
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
    return {"message": "Task updated successfully!", "task": tasks_db[task_id]}
```

Pehle check karo task exist karta hai ya nahi.
Phir `if ... is not None` → Sirf woh field update karo jo user ne bheja.
Agar user ne sirf `completed: true` bheja → sirf wahi badle, title same rahe.

---

## 11. DELETE TASK (DELETE)

```python
@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found!")
    deleted_task = tasks_db.pop(task_id)
    return {"message": "Task deleted successfully!", "deleted_task": deleted_task}
```

`tasks_db.pop(task_id)` → Dictionary se woh task nikaal ke hata deta hai
Aur nikaali hui cheez `deleted_task` mein save ho jaati hai
Phir response mein bhej dete hain — "yeh wala delete hua"

---

## 12. FILTER ROUTES (Bonus)

```python
@app.get("/tasks/filter/completed")
def get_completed_tasks():
    completed = [t for t in tasks_db.values() if t["completed"] == True]
    return {"total_completed": len(completed), "tasks": completed}
```

`[t for t in tasks_db.values() if ...]` → Yeh **List Comprehension** hai.
Matlab: "Saare tasks mein se sirf woh nikalo jinka completed == True hai"

Normal loop mein likhte toh:
```python
completed = []
for t in tasks_db.values():
    if t["completed"] == True:
        completed.append(t)
```
Dono same kaam karte hain — list comprehension short way hai.

---

## 13. STATUS CODES — Server kya bol raha hai?

| Code | Matlab |
|------|--------|
| 200 | OK — sab theek |
| 201 | Created — successfully ban gaya |
| 404 | Not Found — nahi mila |
| 422 | Validation Error — galat data bheja |

---

## 14. FLOW — Ek request aane pe kya hota hai?

```
User /tasks pe POST request bhejta hai
          ↓
FastAPI route dhundta hai (@app.post("/tasks"))
          ↓
Pydantic data validate karta hai (Task model)
          ↓
create_task() function chalta hai
          ↓
UUID generate hoti hai
          ↓
tasks_db dictionary mein save hota hai
          ↓
JSON response wapas jaata hai user ko
```

---

## 15. Uvicorn kya hai?

```bash
uvicorn main:app --reload
```

`uvicorn` → Server jo FastAPI ko run karta hai
`main` → main.py file ka naam
`app` → us file mein FastAPI ka object jiska naam app hai
`--reload` → Code change karo toh automatically restart ho jaata hai (development ke liye)

---

💪*
*— Manish Kumar Pandit (aimanish2030)*
