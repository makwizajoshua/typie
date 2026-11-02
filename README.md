# Typie

Hobby WhatsApp-style chat app. FastAPI + PostgreSQL backend, React frontend **(not started)**.

```
typie/
  backend/    FastAPI API + auth (register / login / me)
  frontend/   empty, React stuff thingies will goes here
```

## Run the backend

1. Create the database (once):
   `& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -c "CREATE DATABASE typie;"`
2. In `backend/`:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   copy .env.example .env     # then edit the password + SECRET_KEY + TOKEN_HOURS
   uvicorn app.main:app --reload
   ```
3. Open http://localhost:8000/docs and try register -> login -> Authorize -> /auth/me.
