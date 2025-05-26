# 📅 Collaborative Event Management System - FastAPI

A **Collaborative Event Management System** built from scratch using **FastAPI**, enabling secure event creation, sharing, versioning, and real-time updates via email. Features include a scalable backend with GitHub Actions CI/CD pipeline integration.


## 📌 Features
- **🔗 RESTful API** with FastAPI
- **💾 Database**: PostgreSQL with SQLModel ORM
- **✅ Data Validation**: Pydantic
- **🔄 Database Migrations**: Alembic
- **🔐 Secure Endpoints**: JWT Authentication
- **🐳 Dockerized Application**
- **🛠️ Continuous Integration**: GitLab CI/CD Pipeline

## 🏗️ Tech Stack
- **FastAPI** - High-performance web framework
- **SQLModel** - ORM for database interactions
- **Pydantic** - Data validation and settings management
- **Alembic** - Database migration tool
- **JWT Tokens** - Secure authentication & authorization
- **PostgreSQL** - Relational database
- **Docker** - Containerized deployment
- **Github Actions CI/CD** - Continuous integration and deployment

## 🚀 Getting Started
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/RathQd/Collaborative-Event-Management-System.git
cd python_fastapi
```

### 2️⃣ Setup Environment Variables
Create a `.env` file in the root directory and configure your database & JWT settings.
```env
# PostgreSQL Database Configuration
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_database_name
DATABASE_USERNAME=your_database_user
DATABASE_PASSWORD=your_database_password

# JWT Authentication Configuration
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email SMTP Configuration
EMAIL_ID=your-email@example.com
EMAIL_PASSWORD=your-email-password
```

#### 🖥️ Without Docker (Local Environment)
```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations and App
```bash
alembic upgrade head
uvicorn app.main:app 
```

## 📡 API Documentation
FastAPI provides interactive API docs:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔐 Authentication Endpoints

- **POST** `/api/auth/register` — Register a new user  
- **POST** `/api/auth/login` — Login and receive an authentication token  
- **POST** `/api/auth/refresh` — Refresh an authentication token  
- **POST** `/api/auth/logout` — Invalidate the current token  

## 📅 Event Management Endpoints

- **POST** `/api/events` — Create a new event  
- **GET** `/api/events` — List all events the user has access to with pagination and filtering  
- **GET** `/api/events/{id}` — Get a specific event by ID  
- **PUT** `/api/events/{id}` — Update an event by ID (💡 Sends real-time email updates to collaborators)  
- **DELETE** `/api/events/{id}` — Delete an event by ID  
- **POST** `/api/events/batch` — Create multiple events in a single request  

## 👥 Collaboration Endpoints

- **POST** `/api/events/{id}/share` — Share an event with other users  
- **GET** `/api/events/{id}/permissions` — List all permissions for an event  
- **PUT** `/api/events/{id}/permissions/{userId}` — Update permissions for a user  
- **DELETE** `/api/events/{id}/permissions/{userId}` — Remove access for a user  

## 🕒 Version History Endpoints

- **GET** `/api/events/{id}/history/{versionId}` — Get a specific version of an event  
- **POST** `/api/events/{id}/rollback/{versionId}` — Rollback to a previous version  

## 📜 Changelog & Diff Endpoints

- **GET** `/api/events/{id}/changelog` — Get a chronological log of all changes to an event  
- **GET** `/api/events/{id}/diff/{versionId1}/{versionId2}` — Get a diff between two versions  

## 📦 Deployment with Github actions CI/CD
This project integrates a **Github actions CI/CD pipeline** for automated testing and deployment.

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or submit PRs.

---
**Star ⭐ the repo if you found it useful!**

