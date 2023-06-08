python manage.py migrate
python manage.py createsuperuser --no-input
gunicorn miejski.wsgi --bind=0.0.0.0:80