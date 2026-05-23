# Production-Ready Django Photo Album Management System

A production-oriented Django application for photo album management with Class-Based Views, RBAC, Cloudinary media storage, and Render deployment support.

## Features

- Album and photo CRUD using Django CBVs.
- Regular user registration (`/accounts/signup/`) with Django auth.
- Login and signup password visibility toggle (eye icon).
- Registration success flow redirects to login with alert message.
- RBAC with Django auth + model permissions:
  - `album_admin` group and superusers can access all albums/photos.
  - Standard users are restricted to their own albums/photos.
- Cloudinary-based image upload and delivery.
- PostgreSQL-ready configuration via `DATABASE_URL`.
- Render deployment configuration (`render.yaml`, `build.sh`).
- Responsive custom UI.

## Project Setup (Local)

1. Create virtual environment: `py -m venv venv`
2. Activate environment: `./venv/Scripts/Activate.ps1`
3. Install dependencies: `pip install -r requirements.txt`
4. Create local env file from template:
   - Copy `.env.example` to `.env`
   - Fill values in `.env`:
     - `SECRET_KEY`
     - `DEBUG=true`
     - `ALLOWED_HOSTS=127.0.0.1,localhost`
     - `CLOUDINARY_CLOUD_NAME`
     - `CLOUDINARY_API_KEY`
     - `CLOUDINARY_API_SECRET`
5. Run migrations:
   - `python manage.py makemigrations`
   - `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Start server: `python manage.py runserver`

## Authentication

- Login: `/accounts/login/`
- Logout: `/accounts/logout/`
- Signup: `/accounts/signup/`

After successful signup, users are redirected to login and shown a success message.

## RBAC Configuration

1. Sign in as superuser via `/admin`.
2. Create group named `album_admin`.
3. Assign permissions to `album_admin`:
   - Album: `view`, `add`, `change`, `delete`
   - Photo: `view`, `add`, `change`, `delete`
4. Add admin users into `album_admin`.

Result:
- `album_admin` and superusers have global access.
- Standard users can only manage their own albums/photos.

## Render Deployment (Step-by-Step)

1. Push code to GitHub.
2. In Render, create a PostgreSQL database.
3. Create a web service linked to your repository.
4. Build command: `./build.sh`
5. Start command: `gunicorn photo_album.wsgi:application`
6. Add environment variables in Render:
   - `SECRET_KEY`
   - `DEBUG=false`
   - `ALLOWED_HOSTS=your-app.onrender.com`
   - `DATABASE_URL` (from Render DB)
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
7. Deploy.
8. Open Render shell and run `python manage.py createsuperuser`.
9. Validate login, CRUD, and Cloudinary uploads.

## Submission Deliverables

- Live Application URL (Render)
- GitHub Repository URL
- One document containing repo URL, live URL, and project documentation

## Security

- Never hardcode secrets.
- Keep production `DEBUG=false`.
- Use environment variables for all credentials.
