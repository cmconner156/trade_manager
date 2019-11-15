import sys
import socket
import logging
import yaml
import re

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from api.models import TGMessage
from api.tg_library import process_new_message, process_deleted_message

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_hash = settings.TELEGRAM['API_HASH']
api_id = settings.TELEGRAM['API_ID']
session = settings.TELEGRAM['SESSION']
client = TelegramClient(StringSession(session), api_id, api_hash)

class Command(BaseCommand):
    help = 'Just testing stuff'

    def add_arguments(self, parser):
        #Positional arg example
        parser.add_argument('nothing', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        print("settings:%s" % settings)
        print("settings.TELEGRAM: %s" % settings.TELEGRAM)
        if api_hash is not None:
            print("api_hash:%s" % api_hash)
        else:
            print("something is broken")
        if api_id is not None:
            print("api_id:%s" % api_id)
        else:
            print("something is broken")

        with client:
            client.run_until_disconnected()



    @client.on(events.MessageDeleted())
    async def deletedMessageHandler(event):
        #THIS IS INCOMING DELETE:
        #DeletedEvent: MessageDeleted.Event(original_update=UpdateDeleteChannelMessages(channel_id=1256178279, messages=[133], pts=135, pts_count=1), deleted_id=133, deleted_ids=[133])
        try:
          process_deleted_message(event)
        except AttributeError as e:
          logging.warning("AttributeError: %s" % e)
          pass
        except Exception as e:
          logging.warning("Caught exception: %s" % e)
          pass


    #@client.on(events.NewMessage(pattern=r'(?is).*(entry|closing|close|buy|sell).*', forwards=False))
    @client.on(events.NewMessage())
    async def my_event_handler(event):
        #THIS IS INCOMING MESSAGE:
        #NewMessage.Event(original_update=UpdateNewChannelMessage(message=Message(id=133, to_id=PeerChannel(channel_id=1256178279), date=datetime.datetime(2019, 11, 4, 20, 22, 46, tzinfo=datetime.timezone.utc), message='USDJPY SELL \nEntry 108.533\nSL 109.150\nTp 107.100', out=True, mentioned=False, media_unread=False, silent=False, post=True, from_scheduled=False, legacy=False, edit_hide=False, from_id=None, fwd_from=None, via_bot_id=None, reply_to_msg_id=None, media=None, reply_markup=None, entities=[], views=1, edit_date=None, post_author=None, grouped_id=None, restriction_reason=[]), pts=134, pts_count=1), pattern_match=<re.Match object; span=(0, 48), match='USDJPY SELL \nEntry 108.533\nSL 109.150\nTp 107.1>, message=Message(id=133, to_id=PeerChannel(channel_id=1256178279), date=datetime.datetime(2019, 11, 4, 20, 22, 46, tzinfo=datetime.timezone.utc), message='USDJPY SELL \nEntry 108.533\nSL 109.150\nTp 107.100', out=True, mentioned=False, media_unread=False, silent=False, post=True, from_scheduled=False, legacy=False, edit_hide=False, from_id=None, fwd_from=None, via_bot_id=None, reply_to_msg_id=None, media=None, reply_markup=None, entities=[], views=1, edit_date=None, post_author=None, grouped_id=None, restriction_reason=[]))
        try:
          process_new_message(event)
        except AttributeError as e:
          logging.warning("AttributeError: %s" % e)
          pass
        except Exception as e:
          logging.warning("Caught exception: %s" % e)
          pass


