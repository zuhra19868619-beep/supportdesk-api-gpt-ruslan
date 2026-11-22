# SupportDesk API — WEPRO diploma

Full-stack helpdesk project using Django REST Framework, PostgreSQL, JWT, Swagger, and React (RU/EN).

This repository is being prepared for publication. Do not deploy until all source files, migrations, tests, and Render configuration have been uploaded and verified.

## Required API
- `POST /api/auth/register/`
- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`
- `GET /api/auth/me/`
- `GET|POST /api/tickets/`
- `GET|PATCH|DELETE /api/tickets/{id}/`
- `GET /api/categories/`
- `GET|POST /api/tickets/{id}/comments/`

## Security
Users can access only their own tickets. Only support managers may change ticket status. A ticket author may edit or delete a ticket only while its status is `new`.

## Deployment
Render deployment configuration and application source will be added before deployment.
