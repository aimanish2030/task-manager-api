# 📋 Task Manager API

A RESTful CRUD API built with **Python + FastAPI** by [Manish Kumar Pandit](https://github.com/aimanish2030)

---

## 🚀 Tech Stack

- **Python 3.11+**
- **FastAPI** — Modern, fast web framework
- **Pydantic** — Data validation
- **Uvicorn** — ASGI server

---

## ⚙️ Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the server
```bash
uvicorn main:app --reload
```

### 3. Open API docs
```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get task by ID |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/tasks/filter/completed` | Get completed tasks |
| GET | `/tasks/filter/pending` | Get pending tasks |

---

## 📝 Example Usage

### Create a Task
```json
POST /tasks
{
  "title": "Learn FastAPI",
  "description": "Build a CRUD API project",
  "completed": false
}
```

### Update a Task
```json
PUT /tasks/{id}
{
  "completed": true
}
```

---

## 👨‍💻 Developer

**Manish Kumar Pandit**  
BCA Student | Aspiring LLM & GenAI 


GitHub: [aimanish2030](https://github.com/aimanish2030)  
LinkedIn: [Manish Kumar Pandit](https://www.linkedin.com/in/manish-kumar-pandit-99977538a)
