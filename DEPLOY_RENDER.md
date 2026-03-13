# Deploy Django Portfolio on Render (Free)

## 1) Push latest code to GitHub
- Make sure your latest local changes are pushed.

## 2) Create account and connect repo
- Go to [https://render.com](https://render.com)
- Sign in with GitHub and connect `portfolio-django` repo.

## 3) Deploy using Blueprint (recommended)
- In Render dashboard, click **New** -> **Blueprint**.
- Select your repo.
- Render will read `render.yaml` and create:
  - Web service (`portfolio-django`)
  - Free PostgreSQL database (`portfolio-db`)

## 4) Set environment values (if needed)
- `DJANGO_CSRF_TRUSTED_ORIGINS` should match your actual Render URL, example:
  - `https://portfolio-django.onrender.com`
- If service name differs, update this env var after first deploy.

## 5) First deploy checks
- Render build runs:
  - `pip install -r requirements.txt`
  - `python manage.py collectstatic --noinput`
  - `python manage.py migrate --noinput`
- App starts with:
  - `gunicorn portfolio.wsgi:application`

## 6) Create admin user (one-time)
- In Render dashboard -> your web service -> **Shell**, run:
  - `python manage.py createsuperuser`

## 7) Media uploads note
- Render free instances use ephemeral disk.
- For persistent uploads, use external storage (Cloudinary/S3).
- Current setup works for testing, but uploads can reset on redeploy/restart.

## 8) Free domain options
- Default free URL: `*.onrender.com` (best/easiest)
- For custom domain, add your domain in Render (paid domain registrar needed).

