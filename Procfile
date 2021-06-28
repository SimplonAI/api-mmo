web: gunicorn --workers=2 'app:create_app()' -b :5000
init: python flask db init
migrate: python flask db migrate
upgrade: python flask db upgrade