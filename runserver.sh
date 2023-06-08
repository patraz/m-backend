python manage.py migrate
python manage.py createsuperuser --no-input
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'patrykprause@gmail.com', 'admin')" | python manage.py shell
gunicorn miejski.wsgi --bind=0.0.0.0:80