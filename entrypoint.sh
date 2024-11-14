python manage.py makemigrations --noinput
python manage.py migrate --noinput
# Now start the application
exec "$@"