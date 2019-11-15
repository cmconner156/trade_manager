import socket
import logging
import time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_hash = settings.TELEGRAM['API_HASH']
api_id = settings.TELEGRAM['API_ID']

class Command(BaseCommand):
    help = 'Get authenticated session string for telegram'

    def handle(self, *args, **options):
        with TelegramClient(StringSession(), api_id, api_hash) as client:
            print(client.session.save())





