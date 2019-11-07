import os
import sys
import time
import socket
import logging
import random
import datetime
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy_base import Base
from message import TGMessage
from settings import get_settings

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

from trade import Trade, TradeWrapper, check_if_trade_exists, parse_raw_text

global engine

hostname = socket.gethostname()

args = get_settings()
with open(args.settings_file) as settings_yaml:
  settings = yaml.load(settings_yaml, Loader=yaml.FullLoader)

dbhost = settings.get("db_host", None)
dbuser = settings.get("db_user", "forex")
dbport = settings.get("db_port", 3306)
dbpass = settings.get("db_pass", "forex")
dbname = settings.get("db_name", "forex")
lotsize = settings.get("lot_size", .03)
forex_account_number = settings.get("forex_account_number", None)
spreadmod = settings.get("spread_mod", 3)
pipdigits = settings.get("pip_digits", 5)

if dbhost is None:
  logging.error("db_host must be set in settings.yaml")
  sys.exit(1)

if forex_account_number is None:
  logging.error("forex_account_number must be set in settings.yaml")
  sys.exit(1)

def process_trade(message):
    message_id = message.id
    message_channel_id = message.channel_id
    message_sender_id = message.sender_id
    message_date = message.message_date
    message_channel_name = message.channel_name
    message_status = message.status
    message_raw_text = message.raw_text
    logging.info("%s:%s:%s:%s:%s:%s" % (
    message_id, message_channel_id, message_date, message_channel_name, message_status, message_raw_text))

    raw_text_results = parse_raw_text(message_raw_text)
#    test = check_if_trade_exists(session, raw_text_results,
#                                 timeframe=datetime.datetime.now() - datetime.timedelta(hours=1))
    trade = Trade()

    kwargs = {'forex_account_number': forex_account_number, \
              'tp_adjust': spreadmod, \
              'pip_digits': pipdigits, \
              'origin': "TG%s" % message_channel_name, \
              'tg_sender_id': message_sender_id, \
              'tg_message_id': message_id, \
              'tg_date': message_date, \
              'state': "received", \
              'action': raw_text_results['action'], \
              'entry': raw_text_results['entry'], \
              'take_profit_count': raw_text_results['take_profit_count'], \
              'forex_pair': raw_text_results['forex_pair'], \
              'forex_pair_digits': raw_text_results['forex_pair_digits'], \
              'stop_loss1': raw_text_results['stop_loss1'], \
              'take_profit': raw_text_results['take_profit']
              }

#    trade_wrapper = TradeWrapper(trade, session, lotsize, message_raw_text, **kwargs)
    trade_wrapper = TradeWrapper(trade, lotsize, message_raw_text, **kwargs)
    last_trade_id = trade_wrapper.get_id()

    if trade_wrapper.get_strategy() == "20_pip_partial_close_rolling_stop_loss":
        group_magic_number = random.randint(10000, 2000000000)
        trade_wrapper.set_mt4_magic_number(group_magic_number)
    if trade_wrapper.get_strategy() == "take_profit_move_other_trade_stop_loss":
        group_magic_number = random.randint(10000, 2000000000)
        trade_wrapper.set_mt4_magic_number(group_magic_number)

    session = Session()
    session.add(trade)
    session.commit()
    session.close()
    return last_trade_id


engine = create_engine("mysql://%s:%s@%s:%s/%s" % (dbuser, dbpass, dbhost, dbport, dbname), pool_size=20, max_overflow=100, echo=False)
Base.metadata.create_all(engine, checkfirst=True)

while(True):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        messages = session.query(TGMessage).filter(TGMessage.ack.like("FALSE"))
        session.close()
        for message in messages:
            if message.status == "NEW":
                last_trade_id = process_trade(message)
                logging.info("Acknowledging message id: %s" % message.id)
                session = Session()
                update_message = session.query(TGMessage).filter(TGMessage.id == int(message.id)).one()
                update_message.ack = "TRUE"
                session.commit()
                session.close()

                session = Session()
                trades = session.query(Trade).all()
                session.close()
                for trade in trades:
                    if trade.id == last_trade_id:
                        logging.info("PAIR: %s : ACTION: %s : ENTRY: %s : TP1: %s : TP1ADJ: %s" % (trade.forex_pair, trade.action, trade.entry, trade.take_profit1, trade.take_profit1_adj))
                        logging.info("TP1 over ENTRY: %s" % str(trade.take_profit1_pips_planned))
                        if trade.take_profit2_adj is not None:
                            logging.info("PAIR: %s : ACTION: %s : ENTRY: %s : TP2: %s : TP2ADJ: %s" % (trade.forex_pair, trade.action, trade.entry, trade.take_profit2, trade.take_profit2_adj))
                            logging.info("TP2 over ENTRY: %s" % str(trade.take_profit2_pips_planned))
                        if trade.take_profit3_adj is not None:
                            logging.info("PAIR: %s : ACTION: %s : ENTRY: %s : TP3: %s : TP3ADJ: %s" % (trade.forex_pair, trade.action, trade.entry, trade.take_profit3, trade.take_profit2_adj))
                            logging.info("TP3 over ENTRY: %s" % str(trade.take_profit3_pips_planned))
                        logging.info("SL1 below ENTRY: %s" % str(trade.stop_loss_pips_planned))


        time.sleep(1)
    except Exception as e:
        logging.warning("Caught exception: %s" % e)
        pass


