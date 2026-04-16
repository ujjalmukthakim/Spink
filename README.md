# RealLike System

RealLike System is a lightweight Instagram engagement exchange built for low-cost deployment. It stores only text metadata, rewards real users with credits for completed likes, and includes manual verification plus admin controls for moderation.

## Stack

- Backend: Django + Django REST Framework + Simple JWT
- Frontend: React + Vite
- Database: SQLite for local development, Render PostgreSQL via `DATABASE_URL` for deployment
- Deployment targets: Render for backend, Vercel for frontend

## Local setup

### Backend

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `backend/.env.example` to `backend/.env`.
4. Keep `USE_SQLITE=True` for the easiest local setup.
5. Run `python manage.py migrate`.
6. Seed the admin account with `python manage.py seed_admin`.
7. Start the API with `python manage.py runserver`.

### Frontend

1. Copy `frontend/.env.example` to `frontend/.env`.
2. Set `VITE_API_BASE_URL` to your backend API base, usually `http://127.0.0.1:8000/api`.
3. Install dependencies with `npm install`.
4. Start the frontend with `npm run dev`.

## Deployment

### Render backend

1. Create a PostgreSQL database on Render.
2. Create a Render web service rooted at `backend/`.
3. Use build command `pip install -r requirements.txt`.
4. Use start command `gunicorn config.wsgi:application`.
5. Set `DATABASE_URL` from the Render PostgreSQL service connection string.
6. Set production env vars such as `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and admin credentials.
6. Run `python manage.py migrate` and `python manage.py seed_admin` after first deploy.

### Vercel frontend

1. Import the repo and set the project root to `frontend/`.
2. Set `VITE_API_BASE_URL` to your Render backend URL plus `/api`.
3. Build command: `npm run build`.
4. Output directory: `dist`.

## Notes

- No images or videos are uploaded or stored.
- The frontend retries requests and shows a wake-up message for Render cold starts.
- Verified users are prioritized in the exchange system, and each confirmed like updates credits immediately.
- Local testing does not require MySQL or PostgreSQL because SQLite is the default fallback.
