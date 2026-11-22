# SupportDesk API — WEPRO diploma
Django REST Framework + PostgreSQL + JWT + Swagger + React (RU/EN).

## API
- POST /api/auth/register/
- POST /api/auth/token/
- POST /api/auth/token/refresh/
- GET /api/auth/me/
- GET, POST /api/tickets/
- GET, PATCH, DELETE /api/tickets/{id}/
- GET /api/categories/
- GET, POST /api/tickets/{id}/comments/
- GET /api/stats/
- Swagger: /api/docs/

## Local backend
Create a Python 3.12 virtual environment, install `backend/requirements.txt`, set `DATABASE_URL`, `SECRET_KEY`, and `DEBUG=true`, then run:
```bash
cd backend
python manage.py migrate
python manage.py seed_categories
python manage.py runserver
```
For frontend:
```bash
cd frontend
npm install
npm run dev
```
Run tests: `cd backend && python manage.py test`.

## Permissions
Ordinary users see only their own tickets; manager users (is_staff, created via Django Admin) see all. Only managers change status. Users can edit/delete only their own new tickets.

## Deployment
Render Blueprint `render.yaml` provisions free-tier Postgres, Docker API, and static frontend. Free database has limited lifetime. Set production secrets through Render, never commit .env. Confirm actual service URLs and CORS after provision. Attachments are not included in this initial release.

## Demo
Register a user, obtain JWT, create ticket, verify cross-user access denied, log in as manager, update status, comment, filter/search, inspect Swagger.
