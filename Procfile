web: gunicorn c2oss-v2.wsgi --log-file -
worker: python worker.py
release: python manage.py migrate
