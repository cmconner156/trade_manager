This is a telegram forex channel watcher designed to cleanup messages and send to a new channel.


docker-compose build
docker-compose up -d
docker-compose logs -f
docker-compose exec db mysql -h db -u root --password=password
docker-compose exec db mysql -h db -u trade_manager --password=password
docker-compose exec app python3 /app/manage.py makemigrations
docker-compose exec app python3 /app/manage.py migrate --no-input

Credit

https://github.com/xlwings/python-celery-dockerize-celery-django
http://nisanthsojan.com/django-mysql-gunicorn-nginx-with-docker%e2%80%8a-a-step-by-step-guide/



Requirements:

- Python 3
- Telegram
- telethon:

pip3 install telethon

- Intrinio forex subscription $20.  Temporary for now.

pip3 install intrinio-sdk

- Intrinio API Key
- Telegram API Key and Hash Key


docker-compose build
docker-compose up -d
docker-compose ps
docker-compose logs
docker-compose logs [service_name] -f --tail=10
docker-compose exec -it web /bin/bash


#Install
#/usr/local/bin/pip3 install telethon
#/usr/local/bin/pip3 install intrinio-sdk
#/usr/local/bin/pip3 install mysqlclient
#/usr/local/bin/pip3 install sqlalchemy
#/usr/local/bin/pip3 install pyyaml

