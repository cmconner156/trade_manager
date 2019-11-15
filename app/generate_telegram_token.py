import os
import sys

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_hash = os.environ.get('TG_API_HASH', None)
api_id = os.environ.get('TG_API_ID', None)

if api_hash is None or api_id is None:
    print("TG_API_HASH and TG_API_ID environment variables MUST be set")
    print("Try these commands")
    print("docker run -d --name generate_telegram_token -v $(pwd)/app:/app -e TG_API_ID=123456 -e TG_API_HASH=78987323523523 app sleep 10000")
    print("docker exec -it generate_telegram_token python3 /app/generate_telegram_token.py")
    sys.exit(1)

if os.environ.get('DOCKERCONTAINER', None) is None or 'trade_manager' not in os.environ.get('DOCKERCONTAINER'):
    print("This must be run in the app docker container, try these commands")
    print("docker run -d --name generate_telegram_token -v $(pwd)/app:/app -e TG_API_ID=123456 -e TG_API_HASH=78987323523523 app sleep 10000")
    print("docker exec -it generate_telegram_token python3 /app/generate_telegram_token.py")
    sys.exit(1)

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("Put this in the TG_SESSION= section of your env.env")
    print("Don't forget to include TG_API_ID= and TG_API_HASH= as well based on same entries from this command")
    print(client.session.save())





