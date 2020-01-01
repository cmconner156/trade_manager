import re
import logging

import django.db
from api.models import TGMessage

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

def process_new_message(event):
  message_match = re.compile('(?is).*(entry|closing|close|buy|sell).*')
  if hasattr(event, 'raw_text') and (message_match.match(event.raw_text)):
    logging.info("NEW MESSAGE TO DB: %s" % event)
    kwargs = {'message_id': event.id, \
              'sender_id': event.sender_id, \
              'message_date': event.date, \
              'channel_name': event.chat.title, \
              'channel_id': event.message.to_id.channel_id, \
              'raw_text': event.raw_text, \
              'status': "NEW"}

    django.db.close_old_connections()
    message = TGMessage.objects.create_message(**kwargs)
  else:
    logging.info("NEW MESSAGE NO DB: %s" % event)


def process_deleted_message(event):
  if hasattr(event.original_update, "channel_id"):
    logging.info("DELETED MESSAGE TO DB: %s" % event)
    channel_id = event.original_update.channel_id
    deleted_id = event.deleted_id


