This is a telegram forex channel watcher designed to cleanup messages and send to a new channel.

Install docker, docker-compose, git.

git clone https://github.com/cmconner156/trade_manager.git
cd trade_manager
cp env.env.example env.env
docker-compose build
docker run -d --name generate_telegram_token -v $(pwd)/app:/app -e TG_API_ID=123456 -e TG_API_HASH=78987323523523 app sleep 10000
docker exec -it generate_telegram_token python3 /app/generate_telegram_token.py



docker-compose up -d
docker-compose logs -f
docker-compose exec db mysql -h db -u trade_manager --password=password trade_manager
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

