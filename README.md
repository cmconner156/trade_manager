This is a telegram forex channel watcher designed to cleanup messages and send to a new channel.

Get api_id and api_hash from telegram for your account

Install docker, docker-compose, git.

git clone https://github.com/cmconner156/trade_manager.git  
cd trade_manager  
cp env.env.example env.env  
docker-compose build  
docker rm generate_telegram_token  
docker run -d --name generate_telegram_token -v $(pwd)/app:/app -e TG_API_ID=123456 -e TG_API_HASH=78987323523523 app sleep 10000  
docker exec -it generate_telegram_token python3 /app/generate_telegram_token.py  

You'll see output like:  

cconner@ubuntumt4:~/trade_manager$ docker exec -it generate_telegram_token python3 /app/generate_telegram_token.py  
Please enter your phone (or bot token):  

Enter your phone number where you are asked - US = 15552221234

Then you'll see:

Please enter the code you received:

Enter the code from telegram.

You will now see:  

Signed in successfully as Christopher Conner  
Put this in the TG_SESSION= section of your env.env  
Don't forget to include TG_API_ID= and TG_API_HASH= as well based on same entries from this command  
lkjasdlfkjasdlfkajsdf209872408724SOMEREALLYREALLYREALLYLONGSTRING098720897235==adsflakj  
Your env.env TELEGRAM section should look like:  
TG_API_ID=123456  
TG_API_HASH=78987323523523  
TG_SESSION=lkjasdlfkjasdlfkajsdf209872408724SOMEREALLYREALLYREALLYLONGSTRING098720897235==adsflakj  

Now edit your env.env file, find the TELEGRAM section and add the output from the command

Now we start the app!

docker-compose up -d  

Watch the logs for issues:  

docker-compose logs -f  

Make sure everything is started:  

cconner@ubuntumt4:~/trade_manager$ docker ps
CONTAINER ID        IMAGE                                COMMAND                  CREATED             STATUS              PORTS                                                    NAMES  
939e14208a17        nginx:latest                         "nginx -g 'daemon of…"   4 minutes ago       Up 4 minutes        0.0.0.0:5555->5555/tcp, 80/tcp, 0.0.0.0:8000->8000/tcp   trade_manager_nginx_1  
5edb5de75710        app                                  "bash -c '/wait-for-…"   5 minutes ago       Up 4 minutes        8000/tcp                                                 trade_manager_watcher_1  
90292f07d297        app                                  "bash -c '/wait-for-…"   5 minutes ago       Up 4 minutes        8000/tcp                                                 trade_manager_worker_1  
6c797d080f58        app                                  "bash -c '/wait-for-…"   5 minutes ago       Up 4 minutes        8000/tcp                                                 trade_manager_app_1  
4a754b354b99        zoomeranalytics/flower:0.9.1-4.0.2   "/bin/bash /app/star…"   5 minutes ago       Up 4 minutes        5555/tcp                                                 trade_manager_flower_1  
03b702716a34        mysql:5.7                            "docker-entrypoint.s…"   5 minutes ago       Up 5 minutes        3306/tcp, 33060/tcp                                      trade_manager_db_1  
2e6df3f69671        rabbitmq:3                           "docker-entrypoint.s…"   5 minutes ago       Up 5 minutes        4369/tcp, 5671-5672/tcp, 25672/tcp                       trade_manager_broker_1  

You should have 3 app containers, an nginx container, mysql container, rabbitmq container and flower container.  

Now watch the logs for the telegram watcher:

docker-compose logs -f watcher  

You will see:  

cconner@ubuntumt4:~/trade_manager$ docker-compose logs -f watcher
Attaching to trade_manager_watcher_1
watcher_1  | wait-for-it.sh: waiting 60 seconds for app:8000
watcher_1  | wait-for-it.sh: app:8000 is available after 26 seconds
watcher_1  | [ INFO/2019-11-15 21:33:47,638] telethon.crypto.aes: libssl detected, it will be used for encryption
watcher_1  | [ INFO/2019-11-15 21:33:48,088] telethon.network.mtprotosender: Connecting to 149.154.175.57:443/TcpFull...
watcher_1  | [ INFO/2019-11-15 21:33:48,126] telethon.network.mtprotosender: Connection to 149.154.175.57:443/TcpFull complete!


Now create a private channel in Telegram and send a trade to it like:

EURGBP SELL
ENTRY: 0.86356
TP: 0.86016
SL: 0.86641

You should see a message showing it came through:  

watcher_1  | [ INFO/2019-11-15 21:41:44,481] root: NEW MESSAGE TO DB: NewMessage.Event(original_update=UpdateNewChannelMessage(message=Message(id=173, to_id=PeerChannel(channel_id=1256178279), date=datetime.datetime(2019, 11, 15, 21, 41, 44, tzinfo=datetime.timezone.utc), message='EURGBP SELL\nENTRY: 0.86356\nTP: 0.86016\nSL: 0.86641', out=True, mentioned=False, media_unread=False, silent=False, post=True, from_scheduled=False, legacy=False, edit_hide=False, from_id=None, fwd_from=None, via_bot_id=None, reply_to_msg_id=None, media=None, reply_markup=None, entities=[MessageEntityCode(offset=0, length=50)], views=1, edit_date=None, post_author=None, grouped_id=None, restriction_reason=[]), pts=182, pts_count=1), pattern_match=None, message=Message(id=173, to_id=PeerChannel(channel_id=1256178279), date=datetime.datetime(2019, 11, 15, 21, 41, 44, tzinfo=datetime.timezone.utc), message='EURGBP SELL\nENTRY: 0.86356\nTP: 0.86016\nSL: 0.86641', out=True, mentioned=False, media_unread=False, silent=False, post=True, from_scheduled=False, legacy=False, edit_hide=False, from_id=None, fwd_from=None, via_bot_id=None, reply_to_msg_id=None, media=None, reply_markup=None, entities=[MessageEntityCode(offset=0, length=50)], views=1, edit_date=None, post_author=None, grouped_id=None, restriction_reason=[]))  

Now you should be able to check the database and see that same message:  

docker-compose exec db mysql -h db -u trade_manager --password=password trade_manager -e "select * from api_tgmessage;"

cconner@ubuntumt4:~/trade_manager$ docker-compose exec db mysql -h db -u trade_manager --password=password trade_manager -e "select * from api_tgmessage;"  
mysql: [Warning] Using a password on the command line interface can be insecure.  
+----+------------+----------------+----------------------------+----------------------------+--------------------------------------------+------------+----------------------------------------------------+--------+-----+  
| id | message_id | sender_id      | received_date              | message_date               | channel_name                               | channel_id | raw_text                                           | status | ack |  
+----+------------+----------------+----------------------------+----------------------------+--------------------------------------------+------------+----------------------------------------------------+--------+-----+  
|  1 | 172        | -1001256178279 | 2019-11-15 21:35:26.906524 | 2019-11-15 21:35:26.906573 | ChrisConner - (PREMIUM) CHRIS GROUP1 - 1TP | 1256178279 | EURGBP SELL ENTRY: 0.86356 TP: 0.86016 SL: 0.86641 | NEW    |   0 |  
|  2 | 173        | -1001256178279 | 2019-11-15 21:41:44.482039 | 2019-11-15 21:41:44.482093 | ChrisConner - (PREMIUM) CHRIS GROUP1 - 1TP | 1256178279 | EURGBP SELL ENTRY: 0.86356 TP: 0.86016 SL: 0.86641 | NEW    |   0 |  
+----+------------+----------------+----------------------------+----------------------------+--------------------------------------------+------------+----------------------------------------------------+--------+-----+  








Credit

https://github.com/xlwings/python-celery-dockerize-celery-django
http://nisanthsojan.com/django-mysql-gunicorn-nginx-with-docker%e2%80%8a-a-step-by-step-guide/



Requirements:

- Python 3
- Telegram
- telethon:

pip3 install telethon

- Telegram API Key and Hash Key



