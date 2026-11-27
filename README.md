# Alan Shaju portfolio

## Local development

Use Python 3.12. From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DJANGO_DEBUG=1
python manage.py migrate
python manage.py test
python manage.py runserver
```

## Deploy to Render

In the Render dashboard, create a **Blueprint**, connect the GitHub repository, and select the branch containing `render.yaml`. Render installs dependencies, collects static files, generates the Django secret key, and starts Gunicorn. The default Render hostname is allowed automatically. For a custom domain, add it to the service in Render and set `DJANGO_ALLOWED_HOSTS` to the hostname without a scheme or port.

SQLite on the free plan is ephemeral. The portfolio and contact form do not store messages in SQLite. If you need persistent Django admin data, use persistent storage before creating admin accounts.

### Contact form

In the Render service's **Environment** settings, add `RESEND_API_KEY`, `CONTACT_FROM_EMAIL` (a verified Resend sender), and `CONTACT_TO_EMAIL` (your inbox). The form sends a single message to your inbox with the visitor's address as Reply-To. It displays a temporary-unavailable message until a sender and recipient are configured. After adding the values, submit a message on the deployed site and verify that it reaches the inbox.

If any mail credentials previously committed to this repository are still active, revoke or rotate them with the mail provider. Historical commits still contain the old values.
