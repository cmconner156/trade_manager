import sys
import socket
import logging
import yaml
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_base import Base

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

from telethon import TelegramClient, events, sync
from message import TGMessage
from settings import get_settings

global engine
hostname = socket.gethostname()

args = get_settings()
with open(args.settings_file) as settings_yaml:
  settings = yaml.load(settings_yaml, Loader=yaml.FullLoader)

session = settings.get('tg_session', 'FXChannelCopy')
api_id = settings.get('tg_api_id', None)
api_hash = settings.get('tg_api_hash', None)
channel_prefix = settings.get('tg_channel_prefix', "ChrisConner")
dbhost = settings.get("db_host", None)
dbuser = settings.get("db_user", "forex")
dbport = settings.get("db_port", 3306)
dbpass = settings.get("db_pass", "forex")
dbname = settings.get("db_name", "forex")

if api_id is None:
  logging.error("tg_api_id must be set in settings.yaml")
  sys.exit(1)

if api_hash is None:
  logging.error("tg_api_hash must be set in settings.yaml")
  sys.exit(1)

if dbhost is None:
  logging.error("db_host must be set in settings.yaml")
  sys.exit(1)

client = TelegramClient('%s-%s' % (session, hostname), api_id, api_hash)

@client.on(events.MessageDeleted())
async def deletedMessageHandler(event):
  #THIS IS INCOMING DELETE:
  #DeletedEvent: MessageDeleted.Event(original_update=UpdateDeleteChannelMessages(channel_id=1256178279, messages=[133], pts=135, pts_count=1), deleted_id=133, deleted_ids=[133])
  try:
    if hasattr(event.original_update, "channel_id"):
      logging.info("DELETED MESSAGE TO DB: %s" % event)
      channel_id = event.original_update.channel_id
      deleted_id = event.deleted_id
      Session = sessionmaker(bind=engine)
      session = Session()
      tg_message = TGMessage()
      tg_message.channel_id = channel_id
      tg_message.message_id = deleted_id
      tg_message.status = "DELETE"
      session.add(tg_message)
      session.commit()
      session.close()
  except AttributeError as e:
    logging.warning("AttributeError: %s" % e)
    pass
  except Exception as e:
    logging.warning("Caught exception: %s" % e)
    pass


#@client.on(events.NewMessage(pattern=r'(?is).*(entry|closing|close|buy|sell).*', forwards=False))
#@client.on(events.NewMessage(pattern=r'(?is).*(entry|closing|close|buy|sell).*', forwards=False))
@client.on(events.NewMessage())
async def my_event_handler(event):
  try:
    #THIS IS INCOMING MESSAGE:
    #NewMessage.Event(original_update=UpdateNewChannelMessage(message=Message(id=133, to_id=PeerChannel(channel_id=1256178279), date=datetime.datetime(2019, 11, 4, 20, 22, 46, tzinfo=datetime.timezone.utc), message='USDJPY SELL \nEntry 108.533\nSL 109.150\nTp 107.100', out=True, mentioned=False, media_unread=False, silent=False, post=True, from_scheduled=False, legacy=False, edit_hide=False, from_id=None, fwd_from=None, via_bot_id=None, reply_to_msg_id=None, media=None, reply_markup=None, entities=[], views=1, edit_date=None, post_author=None, grouped_id=None, restriction_reason=[]), pts=134, pts_count=1), pattern_match=<re.Match object; span=(0, 48), match='USDJPY SELL \nEntry 108.533\nSL 109.150\nTp 107.1>, message=Message(id=133, to_id=PeerChannel(channel_id=1256178279), date=datetime.datetime(2019, 11, 4, 20, 22, 46, tzinfo=datetime.timezone.utc), message='USDJPY SELL \nEntry 108.533\nSL 109.150\nTp 107.100', out=True, mentioned=False, media_unread=False, silent=False, post=True, from_scheduled=False, legacy=False, edit_hide=False, from_id=None, fwd_from=None, via_bot_id=None, reply_to_msg_id=None, media=None, reply_markup=None, entities=[], views=1, edit_date=None, post_author=None, grouped_id=None, restriction_reason=[]))
#    if hasattr(event.chat, 'title'):
    message_match = re.compile('(?is).*(entry|closing|close|buy|sell).*')
    if hasattr(event, 'raw_text') and (message_match.match(event.raw_text)):
      logging.info("NEW MESSAGE TO DB: %s" % event)
      channel = event.chat.title
      channel_id = event.message.to_id.channel_id
      sender_id = event.sender_id
      message_id = event.id
      event_date = event.date
      raw_text = event.raw_text
      raw_text = ' '.join([line.strip() for line in raw_text.strip().splitlines() if line.strip()])
      Session = sessionmaker(bind=engine)
      session = Session()
      tg_message = TGMessage()
      tg_message.raw_text = raw_text
      tg_message.message_date = event_date
      tg_message.channel_name = channel
      tg_message.channel_id = channel_id
      tg_message.sender_id = sender_id
      tg_message.message_id = message_id
      tg_message.status = "NEW"
      session.add(tg_message)
      session.commit()
      session.close()
    else:
      logging.info("NEW MESSAGE NO DB: %s" % event)

  except AttributeError as e:
    logging.warning("AttributeError: %s" % e)
    pass
  except Exception as e:
    logging.warning("Caught exception: %s" % e)
    pass

with client:
#  engine = create_engine("mysql://%s:%s@%s:%s/%s" % (dbuser, dbpass, dbhost, dbport, dbname), echo=True)
  engine = create_engine("mysql://%s:%s@%s:%s/%s" % (dbuser, dbpass, dbhost, dbport, dbname), echo=False)
  Base.metadata.create_all(engine, checkfirst=True)
  client.run_until_disconnected()

