web: gunicorn root.wsgi --log-file -
web: ./entrypoint.sh gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT