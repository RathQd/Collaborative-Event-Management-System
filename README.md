📅 Collaborative Event Management System - FastAPI
A robust and collaborative Event Management System built from scratch using FastAPI, offering secure user authentication, advanced event sharing features, and version-controlled event data — all integrated with a Github Actions CI/CD pipeline for seamless delivery.

📌 Features
🔐 Authentication: Secure login, registration, token-based access (JWT)

🗓️ Event Management: Create, update (with real time update), list, and delete events with full versioning

👥 Collaboration: Share events with users, assign permissions

🔁 Version Control: Track changes, rollback to previous states

🧾 Changelog & Diffs: Audit changes and compare versions

🐳 Dockerized Application

🛠️ CI/CD Pipeline: Integrated using GitHub Actions


🏗️ Tech Stack
FastAPI - Blazing fast web framework

SQLModel - SQLAlchemy-based ORM

Pydantic - Data parsing and validation

Alembic - DB schema migrations

JWT - Token-based authentication

PostgreSQL - Relational DB

Docker - Containerized setup

GitHub Actions - CI/CD pipeline for testing and deployment

🚀 Getting Started
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/RathQd/Collaborative-Event-Management-System.git
cd event-management-system
2️⃣ Setup Environment Variables
Create a .env file at the root:

env
Copy
Edit
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
🛠️ Run Locally
🐍 Without Docker
bash
Copy
Edit
pip install -r requirements.txt
uvicorn app.main:app --reload
🔄 Run Migrations
bash
Copy
Edit
alembic upgrade head
📡 API Documentation
Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

📚 API Endpoints Overview
🔐 Authentication
POST /api/auth/register
Registers a new user with required credentials. Returns success message or validation error.

POST /api/auth/login
Authenticates a user and returns a JWT access token and refresh token.

POST /api/auth/refresh
Accepts a refresh token and returns a new access token to maintain session continuity.

POST /api/auth/logout
Invalidates the current JWT, effectively logging the user out.

📅 Event Management
POST /api/events
Creates a new event. Requires fields like title, description, start_time, end_time, etc.

GET /api/events
Retrieves a list of events the authenticated user has access to. Supports pagination and search by keyword.

GET /api/events/{id}
Fetches details of a specific event by its unique ID.

PUT /api/events/{id}
Updates an existing event with real time update in email. Requires permission to modify. Accepts full data.

DELETE /api/events/{id}
Deletes an event. Only the creator or users with deletion rights can perform this action.

POST /api/events/batch
Creates multiple events in one request by sending an array of event objects.

👥 Collaboration
POST /api/events/{id}/share
Shares an event with specified users. Accepts user_id and permission_level (e.g., editor, viewer).

GET /api/events/{id}/permissions
Lists all collaborators and their permission levels for the given event.

PUT /api/events/{id}/permissions/{userId}
Updates the permission level (editor/viewer) for a specific collaborator.

DELETE /api/events/{id}/permissions/{userId}
Removes a collaborator’s access to the event.

🕒 Version History
GET /api/events/{id}/history/{versionId}
Retrieves a specific historical version of an event by version ID.

POST /api/events/{id}/rollback/{versionId}
Rolls back the event to a previous version, restoring old data and creating a new version entry.

🔍 Changelog & Diff
GET /api/events/{id}/changelog
Returns a chronological list of changes made to the event with timestamps and editors.

GET /api/events/{id}/diff/{versionId1}/{versionId2}
Compares two versions of an event and returns the field-level differences in structured format.

📦 Deployment with GitHub Actions
This project includes a GitHub Actions workflow that:
Builds and deploys the app (can be extended for production environments)

🤝 Contributing
Contributions are welcome!
Open issues, suggest features, or submit PRs to improve this project.

⭐ Star this repo if you found it useful and want to support the project!