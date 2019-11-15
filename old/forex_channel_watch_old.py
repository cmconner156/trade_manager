#IMNPORTANT FIND OUT IF FORWARDED MESSAGE!!!!
#Install
#/usr/local/bin/pip3 install telethon
#/usr/local/bin/pip3 install intrinio-sdk
#/usr/local/bin/pip3 install mysqlclient

import os
import sys
import time
import socket
import sqlite3
import logging
import datetime
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

from telethon import TelegramClient, events, sync
from telethon.tl.types import InputPeerChat
from telethon.tl.functions.channels import CreateChannelRequest, CheckUsernameRequest, UpdateUsernameRequest
from telethon.tl.types import InputChannel, InputPeerChannel
from trade_old import Trade
from database_old import Database

global db
hostname = socket.gethostname()
session = os.environ.get('TG_SESSION', 'FXChannelCopy')
api_id = os.environ.get('TG_API_ID', None)
api_hash = os.environ.get('TG_API_HASH', None)
intrinio_key = os.environ.get('TG_INTRINIO_KEY', None)
channel_prefix = os.environ.get('TG_CHANNEL_PREFIX', "ChrisConner")
spread_adjustment = os.environ.get("TG_SPREAD", 0)
dbhost = os.environ.get("DBHOST", None)
dbuser = os.environ.get("DBUSER", "forex")
dbport = os.environ.get("DBPORT", 3306)
dbpass = os.environ.get("DBPASS", "forex")
dbname = os.environ.get("DBNAME", "forex")

if api_id is None:
  logging.error("TG_API_ID environment variable must be set")
  sys.exit(1)

if api_hash is None:
  logging.error("TG_API_HASH environment variable must be set")
  sys.exit(1)

if intrinio_key is None:
  logging.error("TG_INTRINIO_KEY environment variable must be set")
  sys.exit(1)

if dbhost is None:
  logging.error("DBHOST environment variable must be set")
  sys.exit(1)

async def get_dest_channel(client, channel):
  dialogs = await client.get_dialogs()
  returnChannel = None
  for dialog in dialogs:
    if hasattr(dialog.entity, 'title'):
      if dialog.entity.title == channel:
        returnChannel = dialog.entity
  if returnChannel is None:
    logging.warn("Channel %s does not exist creating now" % channel)
    try:
      returnChannel = await client(CreateChannelRequest(channel, "Scripted channel create %s" % channel, megagroup=False))
      returnChannel = returnChannel.chats[0]

    except Exception as e:
      logging.error("Failed to create channel %s to send messages to: %s" % (channel, e))

  try:
    await client.send_message(entity=returnChannel, message="%s: Testing %s" % (socket.gethostname(), channel))
  except Exception as e:
    logging.error("Failed to send message to %s: %s" % (channel, e))

  return returnChannel


client = TelegramClient('%s-%s' % (session, hostname), api_id, api_hash)
logging.info("VERSION 11")

@client.on(events.MessageDeleted())
async def deletedMessageHandler(event):
  logging.info("DeletedEvent: %s" % event)

@client.on(events.NewMessage(pattern=r'(?is).*(entry|closing|close|buy|sell).*', forwards=False))
async def my_event_handler(event):
  try:
#    chat = await event.get_chat()
    if hasattr(event.chat, 'title'):
      logging.info("event: %s" % event)
      channel = event.chat.title
      destChannelBaseName = '%s - %s' % (channel_prefix, channel)
      sender_id = event.sender_id
      message_id = event.id
      event_date = event.date
      logging.info("sender_id: %s" % sender_id)
      logging.info("event_id: %s" % message_id)
      logging.info("event_date: %s" % event_date)
      raw_text = event.raw_text
      trade = Trade(raw_text=raw_text, intrinio_key=intrinio_key, origin="TG%s" % channel, db=db, tg_sender_id=sender_id, tg_message_id=message_id, tg_date=event_date)
      trade.insert_db()
      new_message = "%s %s" % (trade.forex_pair, trade.action)
      new_message = "%s\nENTRY %s" % (new_message, trade.entry)
      new_message = "%s\nSL %s" % (new_message, trade.stop_loss)
      for take_profit in trade.take_profit:
        new_message = "%s\nTP %s" % (new_message, take_profit)

      tp_count = trade.take_profit_count

      if tp_count > 0:
        destChannelName = '%s - %sTP' % (destChannelBaseName, tp_count)
        destChannel = await get_dest_channel(client, destChannelName)
        logging.info("TPS: %s : From: %s : To: %s : %s" % (str(tp_count), channel, destChannelName, new_message))
        await client.send_message(entity = destChannel, message = new_message)

      else:
        logging.info("NOTPS: From %s : %s" % (channel, raw_text))

  except AttributeError as e:
    logging.warn("AttributeError: %s" % e)
    pass
  except Exception as e:
    logging.warn("Caught exception: %s" % e)
    pass

with client:
  try:
    logging.debug("dbhost: %s" % dbhost)
    logging.debug("dbuser: %s" % dbuser)
    logging.debug("dbport: %s" % dbport)
    logging.debug("dbpass: %s" % dbpass)
    db = Database(host = dbhost, user = dbuser, password = dbpass, db = dbname)
  except Exception as e:
    logging.exception("Failed to connect to database: %s" % e)
    sys.exit(1)

  client.run_until_disconnected()





###IMPORTANT USE get_message_history to try and see if something is deleted
