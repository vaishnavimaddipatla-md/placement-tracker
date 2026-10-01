
# Placement Tracker

A full-stack web application that helps students track job applications across every stage of the hiring process: Wishlist, Applied, Online Test, Interview, Offer and Rejected.

Built with a FastAPI backend, a React frontend and secure JWT authentication.

> **Status:** backend API and login are complete. The applications dashboard, pipeline board, analytics and deployment are in progress (see the roadmap below).

## Features

**Completed**
- User signup and login with bcrypt password hashing and JWT tokens
- Protected REST API where every user can only see and edit their own data
- Full CRUD for job applications (company, role, location, link, notes, status)
- Search by company or role, filter by status, and pagination
- Stage history: every status change is recorded, which will power the analytics
- React login and signup page connected to the API, with token-based sessions

**In progress**
- Applications list and add/edit form in the React UI
- Pipeline board to move applications between stages
- Analytics dashboard (applications per stage, response rate)
- Email reminders for interviews and follow-ups
- Automated tests and live deployment

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database / ORM | SQLite (development), SQLAlchemy |
| Authentication | JWT (PyJWT), bcrypt |
| Validation | Pydantic |
| Frontend | React (Vite), JavaScript, CSS |
| Version control | Git, GitHub |

## Project structure

```
Placement_Tracker/
├── backend/
│   ├── main.py            # app setup, CORS, signup/login/me routes
│   ├── auth.py            # password hashing, JWT, current-user dependency
│   ├── applications.py    # applications CRUD, search, filter, pagination
│   ├── models.py          # database tables
│   ├── schemas.py         # request and response models
│   └── database.py        # database connection
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── Login.jsx      # login and signup page
│       ├── api.js         # API helper that attaches the token
│       └── index.css
└── README.md
```

## Database design

- **users**: id, name, email, password_hash, created_at
- **applications**: id, user_id, company, role, job_link, location, status, applied_date, notes, created_at, updated_at
- **stage_history**: id, application_id, from_status, to_status, changed_at
- **reminders**: id, application_id, remind_at, message, is_sent

## API endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/signup` | Create an account | No |
| POST | `/login` | Get an access token | No |
| GET | `/me` | Current user details | Yes |
| POST | `/applications` | Add an application | Yes |
| GET | `/applications` | List applications (`status`, `search`, `skip`, `limit`) | Yes |
| GET | `/applications/{id}` | Get one application | Yes |
| PATCH | `/applications/{id}` | Update fields or change status | Yes |
| DELETE | `/applications/{id}` | Delete an application | Yes |

Interactive API docs are available at `http://127.0.0.1:8000/docs` when the backend is running.

## Getting started (Windows)

**Prerequisites:** Python 3.10+, Node.js (LTS) and Git.

**1. Clone the repository**
```
git clone <your-repository-url>
cd Placement_Tracker
```

**2. Run the backend**
```
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy bcrypt pyjwt email-validator
uvicorn main:app --reload
```
The API runs at `http://127.0.0.1:8000`. The SQLite database file is created automatically on first run.

**3. Run the frontend** (in a second terminal)
```
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

## Security notes

- Passwords are stored only as bcrypt hashes, never as plain text.
- Every application query is filtered by the logged-in user's id, so users cannot access each other's data.
- The JWT secret in `auth.py` is a development placeholder. Move it to an environment variable before deploying.

## Screenshots


## Roadmap

- [x] Authentication (signup, login, JWT)
- [x] Applications API with search, filters and pagination
- [x] Stage history tracking
- [x] React login and signup
- [ ] Applications list and add/edit form
- [ ] Pipeline board
- [ ] Analytics dashboard
- [ ] Email reminders
- [ ] Automated tests (pytest)
- [ ] Deployment with PostgreSQL

## Author

**Your Name**
Vaishnavi Maddipatla

