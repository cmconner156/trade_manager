#from __future__ import print_function
import time
import re
import intrinio_sdk
from intrinio_sdk.rest import ApiException
import logging
import datetime

class Trade():
  def __init__(self, raw_text=None, intrinio_key=None, origin=None, db=None, strategy=None, comment=None, state=None, tg_message_id=None, tg_sender_id=None, tg_date=None, mt4_ticket_id=None, mt4_open_time=None, mt4_magic_number=None):
    self._raw_text = raw_text
    self._raw_text_no_line = ' '.join([line.strip() for line in self._raw_text.strip().splitlines() if line.strip()])
    self._raw_text_no_space = ''.join(self._raw_text_no_line.split())
    self._forex_pair = None
    self._entry = None
    self._action = None
    self._stop_loss1 = None
    self._stop_loss2 = None
    self._stop_loss3 = None
    self._stop_loss4 = None
    self._stop_loss5 = None
    self._stop_loss_count = 1
    self._take_profit = []
    self._take_profit1 = None
    self._take_profit2 = None
    self._take_profit3 = None
    self._take_profit4 = None
    self._take_profit5 = None
    self._take_profit_count = self._raw_text.lower().count('tp')
    self._origin = origin
    self._strategy = strategy
    self._comment = comment
    self._state = state
    self._tg_message_id = tg_message_id
    self._tg_sender_id = tg_sender_id
    self._tg_date = tg_date
    self._mt4_ticket_id = mt4_ticket_id
    self._mt4_open_time = mt4_open_time
    self._mt4_magic_number = mt4_magic_number
    self._db = db

    forex_pairs = self._db.query("select code from forex.pairs;")
    for pair in forex_pairs:
      if pair[0].lower() in self._raw_text.lower():
        self._forex_pair = pair[0]

#    intrinio_sdk.ApiClient().configuration.api_key['api_key'] = intrinio_key
#    self.forex_api = intrinio_sdk.ForexApi()
#    try:
#      self._forex_pairs = self.forex_api.get_forex_pairs()
#    except ApiException as e:
#      logging.exception("Exception calling get_forex_pairs: %s" % e)

#    for pair in self._forex_pairs.pairs:
#      if pair.code.lower() in self._raw_text.lower():
#        self._forex_pair = pair.code

    if 'buy' in self._raw_text_no_space.lower():
      self._action = "BUY"
    if 'sell' in self._raw_text_no_space.lower():
      self._action = "SELL"

    entry_array = re.findall('entry:?\d*\.?\d+|[-+]?\d+', self._raw_text_no_space, re.IGNORECASE)
    for entry in entry_array:
      if 'entry' in entry.lower():
        self._entry = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", entry)[0]

    stop_loss_array = re.findall('sl:?\d*\.?\d+|[-+]?\d+', self._raw_text_no_space, re.IGNORECASE)
    for stop_loss in stop_loss_array:
      if 'sl' in stop_loss.lower():
        self._stop_loss1 = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", stop_loss)[0]

    take_profit_array = re.findall('tp:?\d*\.?\d+|[-+]?\d+', self._raw_text_no_space, re.IGNORECASE)
    for take_profit in take_profit_array:
      if 'tp' in take_profit.lower():
        self._take_profit.append(re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", take_profit)[0])

    if self._take_profit_count > 0:
      self._take_profit1 = self._take_profit[0]
    if self._take_profit_count > 1:
      self._take_profit2 = self._take_profit[1]
    if self._take_profit_count > 2:
      self._take_profit3 = self._take_profit[2]
    if self._take_profit_count > 3:
      self._take_profit4 = self._take_profit[3]
    if self._take_profit_count > 4:
      self._take_profit5 = self._take_profit[4]

  @property
  def forex_pair(self):
    return self._forex_pair

  @property
  def take_profit_count(self):
    return self._take_profit_count

  @property
  def entry(self):
    return self._entry

  @property
  def stop_loss(self):
    return self._stop_loss1

  @property
  def take_profit(self):
    return self._take_profit

  @property
  def take_profit1(self):
    return self._take_profit1

  @property
  def take_profit2(self):
    return self._take_profit2

  @property
  def take_profit3(self):
    return self._take_profit3

  @property
  def take_profit4(self):
    return self._take_profit4

  @property
  def take_profit5(self):
    return self._take_profit5

  @property
  def action(self):
    return self._action

  def get_json(self):
    json_obj = {}
    json_obj["forex_pair"] = self._forex_pair
    json_obj["enntry"] = self._entry
    json_obj["action"] = self._action
    json_obj["stop_loss1"] = self._stop_loss1
    json_obj["stop_loss2"] = self._stop_loss2
    json_obj["stop_loss3"] = self._stop_loss3
    json_obj["stop_loss4"] = self._stop_loss4
    json_obj["stop_loss5"] = self._stop_loss5
    json_obj["stop_loss_count"] = self._stop_loss_count
    json_obj["take_profit1"] = self._take_profit1
    json_obj["take_profit2"] = self._take_profit2
    json_obj["take_profit3"] = self._take_profit3
    json_obj["take_profit4"] = self._take_profit4
    json_obj["take_profit5"] = self._take_profit5
    json_obj["take_profit_count"] = self._take_profit_count
    json_obj["origin"] = self._origin
    json_obj["strategy"] = self._strategy
    json_obj["comment"] = self._comment
    json_obj["state"] = self._state
    json_obj["tg_message_id"] = self._tg_message_id
    json_obj["tg_sender_id"] = self._tg_sender_id
    json_obj["tg_date"] = self._tg_date
    json_obj["mt4_ticket_id"] = self._mt4_ticket_id
    json_obj["mt4_open_time"] = self._mt4_open_time
    json_obj["mt4_magic_number"] = self._mt4_magic_number

    return json_obj


  def insert_db(self):
    base_insert = "INSERT INTO trades("
    insert_query = ""
    if self._forex_pair is not None:
      base_insert = "%sCODE" % base_insert
      insert_query = "\"%s\"" % self._forex_pair
    else:
      return "FAILED NO FOREX PAIR"
    if self._action is not None:
      base_insert = "%s, PURCHASE" % base_insert
      insert_query = "%s, \"%s\"" % (insert_query, self._action)
    else:
      return "FAILED NO BUY or SELL"
    if self._entry is not None:
      base_insert = "%s, ENTRY" % base_insert
      insert_query = "%s, %s" % (insert_query, self._entry)
    if self._stop_loss1 is not None:
      base_insert = "%s, SL1" % base_insert
      insert_query = "%s, %s" % (insert_query, self._stop_loss1)
    if self._stop_loss2 is not None:
      base_insert = "%s, SL2" % base_insert
      insert_query = "%s, %s" % (insert_query, self._stop_loss2)
    if self._stop_loss3 is not None:
      base_insert = "%s, SL3" % base_insert
      insert_query = "%s, %s" % (insert_query, self._stop_loss3)
    if self._stop_loss4 is not None:
      base_insert = "%s, SL4" % base_insert
      insert_query = "%s, %s" % (insert_query, self._stop_loss4)
    if self._stop_loss5 is not None:
      base_insert = "%s, SL5" % base_insert
      insert_query = "%s, %s" % (insert_query, self._stop_loss5)
    if self._stop_loss_count is not None:
      base_insert = "%s, SL_COUNT" % base_insert
      insert_query = "%s, %s" % (insert_query, self._stop_loss_count)
    if self._take_profit1 is not None:
      base_insert = "%s, TP1" % base_insert
      insert_query = "%s, %s" % (insert_query, self._take_profit1)
    if self._take_profit2 is not None:
      base_insert = "%s, TP2" % base_insert
      insert_query = "%s, %s" % (insert_query, self._take_profit2)
    if self._take_profit3 is not None:
      base_insert = "%s, TP3" % base_insert
      insert_query = "%s, %s" % (insert_query, self._take_profit3)
    if self._take_profit4 is not None:
      base_insert = "%s, TP4" % base_insert
      insert_query = "%s, %s" % (insert_query, self._take_profit4)
    if self._take_profit5 is not None:
      base_insert = "%s, TP5" % base_insert
      insert_query = "%s, %s" % (insert_query, self._take_profit5)
    if self._take_profit_count is not None:
      base_insert = "%s, TP_COUNT" % base_insert
      insert_query = "%s, %s" % (insert_query, self._take_profit_count)
    if self._origin is not None:
      base_insert = "%s, ORIGIN" % base_insert
      insert_query = "%s, \"%s\"" % (insert_query, self._origin)
    if self._strategy is not None:
      base_insert = "%s, STRATEGY" % base_insert
      insert_query = "%s, \"%s\"" % (insert_query, self._strategy)
    if self._comment is not None:
      base_insert = "%s, COMMENT" % base_insert
      insert_query = "%s, \"%s\"" % (insert_query, self._comment)
    if self._state is not None:
      base_insert = "%s, STATE" % base_insert
      insert_query = "%s, %s" % (insert_query, self._state)
    if self._tg_message_id is not None:
      base_insert = "%s, TG_MESSAGE_ID" % base_insert
      insert_query = "%s, %s" % (insert_query, self._tg_message_id)
    if self._tg_sender_id is not None:
      base_insert = "%s, TG_SENDER_ID" % base_insert
      insert_query = "%s, %s" % (insert_query, self._tg_sender_id)
    if self._tg_date is not None:
      base_insert = "%s, TG_DATE" % base_insert
      insert_query = "%s, \"%s\"" % (insert_query, self._tg_date)
    if self._mt4_ticket_id is not None:
      base_insert = "%s, MT4_TICKET_ID" % base_insert
      insert_query = "%s, %s" % (insert_query, self._mt4_ticket_id)
    if self._mt4_open_time is not None:
      base_insert = "%s, MT4_OPEN_TIME" % base_insert
      insert_query = "%s, \"%s\"" % (insert_query, self._mt4_open_time)
    if self._mt4_magic_number is not None:
      base_insert = "%s, MT4_MAGIC_NUMBER" % base_insert
      insert_query = "%s, %s" % (insert_query, self._mt4_magic_number)

    insert_query = "%s) VALUES (%s);" % (base_insert, insert_query)
    logging.info("INSERT QUERY: %s" % insert_query)

