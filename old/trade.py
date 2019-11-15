import datetime
import uuid
import re
import logging
import decimal
from sqlalchemy import Column, Integer, DateTime, String, Float
from sqlalchemy_base import Base

from forex_pairs import ForexPairs

def check_if_trade_exists(session, raw_text_results,  timeframe = datetime.datetime.now() - datetime.timedelta(hours=1)):

    #Lets check DB based on account ID, PAIR, ACTION, ENTRY over timeframe of last 4 hours
    decimal.getcontext().prec = 13
    entry = decimal.Decimal(float(raw_text_results['entry']))
    entry = entry / 1

    action = raw_text_results['action']
    forex_pair = raw_text_results['forex_pair']

    trades = session.query(Trade).filter(Trade.entry == entry).all()
    print("1: %s" % trades)
    trades = session.query(Trade).filter(Trade.forex_pair.like(forex_pair), Trade.action.like(action)).all()
    print("2: %s" % trades)
    for trade in trades:
        print("entry: %s" % trade.entry)
        print("entry raw: %s" % entry)
        print("entry type: %s" % type(trade.entry))
        print("entry raw type: %s" % type(entry))
        print("created: %s" % trade.created_date)
    trades = session.query(Trade).filter(Trade.created_date > timeframe, Trade.forex_pair.like(forex_pair), Trade.action.like(action), Trade.entry==entry).all()
    print("3: %s" % trades)
    for trade in trades:
        print(trade)

    return trades

def parse_raw_text(raw_text):
    return_dict = {}
    #raw_text and formatting to get entry takeprofit stoploss action and pair
    raw_text_no_line = ' '.join([line.strip() for line in raw_text.strip().splitlines() if line.strip()])
    raw_text_no_space = ''.join(raw_text_no_line.split())

    return_dict['take_profit_count'] = raw_text.lower().count('tp')
    forex_pairs = ForexPairs()
    return_dict['forex_pair'], return_dict['forex_pair_digits'] = forex_pairs.check_string_contains_pair(raw_text)
    if 'buy' in raw_text_no_space.lower():
        return_dict['action'] = "BUY"
    if 'sell' in raw_text_no_space.lower():
        return_dict['action'] = "SELL"

    entry_array = re.findall('entry:?\d*\.?\d+|[-+]?\d+', raw_text_no_space, re.IGNORECASE)
    for entry in entry_array:
        if 'entry' in entry.lower():
            return_dict['entry'] = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", entry)[0]

    stop_loss_array = re.findall('sl:?\d*\.?\d+|[-+]?\d+', raw_text_no_space, re.IGNORECASE)
    for stop_loss in stop_loss_array:
        if 'sl' in stop_loss.lower():
            return_dict['stop_loss1'] = re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", stop_loss)[0]

    return_dict['take_profit'] = []
    take_profit_array = re.findall('tp:?\d*\.?\d+|[-+]?\d+', raw_text_no_space, re.IGNORECASE)
    for take_profit in take_profit_array:
        if 'tp' in take_profit.lower():
            return_dict['take_profit'].append(re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", take_profit)[0])

    return return_dict




class Trade(Base):
    __tablename__ = "trades"
    id  = Column(String(255), primary_key=True)
    forex_account_number = Column(String(255))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    forex_pair = Column(String(10))
    entry = Column(Float(10, 5))
    action = Column(String(10))
    lotsize = Column(Float(10, 2))
    stop_loss1 = Column(Float(10, 5))
    stop_loss2 = Column(Float(10, 5))
    stop_loss3 = Column(Float(10, 5))
    stop_loss4 = Column(Float(10, 5))
    stop_loss5 = Column(Float(10, 5))
    stop_loss_pips_planned = Column(Float(10, 5))
    stop_loss_pips_actual = Column(Float(10, 5))
    stop_loss_count = Column(Integer())

    take_profit1 = Column(Float(10, 5))
    take_profit1_adj = Column(Float(10, 5))
    take_profit1_pips_planned = Column(Float(10, 5))
    take_profit1_pips_actual = Column(Float(10, 5))

    take_profit2 = Column(Float(10, 5))
    take_profit2_adj = Column(Float(10, 5))
    take_profit2_pips_planned = Column(Float(10, 5))
    take_profit2_pips_actual = Column(Float(10, 5))

    take_profit3 = Column(Float(10, 5))
    take_profit3_adj = Column(Float(10, 5))
    take_profit3_pips_planned = Column(Float(10, 5))
    take_profit3_pips_actual = Column(Float(10, 5))

    take_profit4 = Column(Float(10, 5))
    take_profit4_adj = Column(Float(10, 5))
    take_profit4_pips_planned = Column(Float(10, 5))
    take_profit4_pips_actual = Column(Float(10, 5))

    take_profit5 = Column(Float(10, 5))
    take_profit5_adj = Column(Float(10, 5))
    take_profit5_pips_planned = Column(Float(10, 5))
    take_profit5_pips_actual = Column(Float(10, 5))

    take_profit_count = Column(Integer())
    take_profit_total_actual = Column(Float(10, 5))

    total_trades = Column(Integer())
    origin = Column(String(255))
    strategy = Column(String(255))
    comment = Column(String(255))
    state = Column(String(255))
    tg_message_id = Column(String(15))
    tg_sender_id = Column(String(15))
    tg_date = Column(DateTime, default=datetime.datetime.utcnow)
    mt4_ticket_id = Column(String(15))
    mt4_magic_number = Column(String(15))
    mt4_open_time = Column(DateTime)






class TradeWrapper():
#  def __init__(self, trade, lotsize, raw_text, id=None, pip_digits=None, tp_adjust=0, origin=None, strategy=None, comment=None, state=None, tg_message_id=None, tg_sender_id=None, tg_date=None, mt4_ticket_id=None, mt4_open_time=None, mt4_magic_number=None):
#  def __init__(self, trade, session, lotsize, raw_text, **kwargs):
  def __init__(self, trade, lotsize, raw_text, **kwargs):
    #trade references DB object used later
    self._lotsize = lotsize

    #raw_text and formatting to get entry takeprofit stoploss action and pair
    self._raw_text = raw_text

    if kwargs.get('id') is not None:
        self._id = kwargs.get('id')
    else:
        self._id = str(uuid.uuid4())

    self._forex_account_number = kwargs.get('forex_account_number', 123456)
    self._tp_adjust = kwargs.get('tp_adjust', 0)
    self._pip_digits = kwargs.get('pip_digits', 5)
    self._origin = kwargs.get('origin', None)
    self._strategy = kwargs.get('strategy', None)
    self._comment = kwargs.get('comment', None)
    self._state = kwargs.get('state', None)
    self._tg_message_id = kwargs.get('tg_message_id', None)
    self._tg_sender_id = kwargs.get('tg_sender_id', None)
    self._tg_date = kwargs.get('tg_date', None)
    self._mt4_ticket_id = kwargs.get('mt4_ticket_id', None)
    self._mt4_open_time = kwargs.get('mt4_open_time', None)
    self._mt4_magic_number = kwargs.get('mt4_magic_number', None)
    self._forex_pair = kwargs.get('forex_pair')
    self._forex_pair_digits = kwargs.get('forex_pair_digits', None)
    self._entry = kwargs.get('entry')
    self._take_profit_count = kwargs.get('take_profit_count')
    self._take_profit = kwargs.get('take_profit')
    self._action = kwargs.get('action')
    self._stop_loss1 = kwargs.get('stop_loss1')



    #Set here based on raw_data
    #
    self._stop_loss2 = None
    self._stop_loss3 = None
    self._stop_loss4 = None
    self._stop_loss5 = None
    self._stop_loss_pips_planned = None
    self._stop_loss_pips_actual = None
    self._stop_loss_count = 1

    self._take_profit1 = None
    self._take_profit1_adj = None
    self._take_profit1_pips_planned = None
    self._take_profit1_pips_actual = None

    self._take_profit2 = None
    self._take_profit2_adj = None
    self._take_profit2_pips_planned = None
    self._take_profit2_pips_actual = None

    self._take_profit3 = None
    self._take_profit3_adj = None
    self._take_profit3_pips_planned = None
    self._take_profit3_pips_actual = None

    self._take_profit4 = None
    self._take_profit4_adj = None
    self._take_profit4_pips_planned = None
    self._take_profit4_pips_actual = None

    self._take_profit5 = None
    self._take_profit5_adj = None
    self._take_profit5_pips_planned = None
    self._take_profit5_pips_actual = None

    self._take_profit_total_actual = None
    self._total_trades = None

    if self._forex_pair_digits > 2:
        self._multiplier_for_pips = 10000
    else:
        self._multiplier_for_pips = 100
    if self._pip_digits == 5:
        self._multiplier = self._multiplier_for_pips * 10

    if self._take_profit_count > 0:
        self._take_profit1 = self._take_profit[0]
        self._take_profit1_adj = self.modify_tp(self._take_profit1)
        self._take_profit1_pips_planned = self.calculate_takeprofit_pips(self._take_profit1_adj)

    if self._take_profit_count > 1:
        self._take_profit2 = self._take_profit[1]
        self._take_profit2_adj = self.modify_tp(self._take_profit2)
        self._take_profit2_pips_planned = self.calculate_takeprofit_pips(self._take_profit2_adj)

    if self._take_profit_count > 2:
        self._take_profit3 = self._take_profit[2]
        self._take_profit3_adj = self.modify_tp(self._take_profit3)
        self._take_profit3_pips_planned = self.calculate_takeprofit_pips(self._take_profit3_adj)

    if self._take_profit_count > 3:
        self._take_profit4 = self._take_profit[3]
        self._take_profit4_adj = self.modify_tp(self._take_profit4)
        self._take_profit4_pips_planned = self.calculate_takeprofit_pips(self._take_profit4_adj)

    if self._take_profit_count > 4:
        self._take_profit5 = self._take_profit[4]
        self._take_profit5_adj = self.modify_tp(self._take_profit5)
        self._take_profit5_pips_planned = self.calculate_takeprofit_pips(self._take_profit5_adj)

    if self._strategy is None and self._take_profit_count == 1:
        self._strategy = "20_pip_partial_close_rolling_stop_loss"
        self._total_trades = 2
        self._take_profit1_adj = self.modify_tp_20()
        self._take_profit1_pips_planned = self.calculate_takeprofit_pips(self._take_profit1_adj)
        self._take_profit2_adj = self.modify_tp(self._take_profit1)
        self._take_profit2_pips_planned = self.calculate_takeprofit_pips(self._take_profit2_adj)

    if self._strategy is None and self._take_profit_count == 3:
        self._strategy = "take_profit_move_other_trade_stop_loss"
        self._total_trades = 3
        self._take_profit1_adj = self.modify_tp_20()
        self._take_profit1_pips_planned = self.calculate_takeprofit_pips(self._take_profit1_adj)
        self._take_profit2_adj = self.modify_tp(self._take_profit2)
        self._take_profit2_pips_planned = self.calculate_takeprofit_pips(self._take_profit2_adj)
        self._take_profit3_adj = self.modify_tp(self._take_profit3)
        self._take_profit3_pips_planned = self.calculate_takeprofit_pips(self._take_profit3_adj)

    trade.id = self._id
    if self._forex_pair is not None:
        trade.forex_pair = self._forex_pair
    else:
        return "FAILED NO FOREX PAIR"
    if self._action is not None:
        trade.action = self._action
    else:
        return "FAILED NO BUY or SELL"
    trade.entry = self._entry
    trade.lotsize = self._lotsize
    trade.stop_loss1 = self._stop_loss1
    trade.stop_loss2 = self._stop_loss2
    trade.stop_loss3 = self._stop_loss3
    trade.stop_loss4 = self._stop_loss4
    trade.stop_loss5 = self._stop_loss5
    trade.stop_loss_count = int(self._stop_loss_count)

    self._stop_loss_pips_planned = self.calculate_stoploss_pips(self._stop_loss1)
    trade.stop_loss_pips_planned = self._stop_loss_pips_planned
    trade.stop_loss_pips_actual = self._stop_loss_pips_actual

    trade.take_profit1 = self._take_profit1
    trade.take_profit1_adj = self._take_profit1_adj
    trade.take_profit1_pips_planned = self._take_profit1_pips_planned
    trade.take_profit1_pips_actual = self._take_profit1_pips_actual

    trade.take_profit2 = self._take_profit2
    trade.take_profit2_adj = self._take_profit2_adj
    trade.take_profit2_pips_planned = self._take_profit2_pips_planned
    trade.take_profit2_pips_actual = self._take_profit2_pips_actual



    trade.take_profit3 = self._take_profit3
    trade.take_profit3_adj = self._take_profit3_adj
    trade.take_profit3_pips_planned = self._take_profit3_pips_planned
    trade.take_profit3_pips_actual = self._take_profit3_pips_actual

    trade.take_profit4 = self._take_profit4
    trade.take_profit4_adj = self._take_profit4_adj
    trade.take_profit4_pips_planned = self._take_profit4_pips_planned
    trade.take_profit4_pips_actual = self._take_profit4_pips_actual

    trade.take_profit5 = self._take_profit5
    trade.take_profit5_adj = self._take_profit5_adj
    trade.take_profit5_pips_planned = self._take_profit5_pips_planned
    trade.take_profit5_pips_actual = self._take_profit5_pips_actual

    trade.take_profit_count = int(self._take_profit_count)
    trade.take_profit_total_actual = self._take_profit_total_actual
    trade.total_trades = int(self._total_trades)

    trade.forex_account_number = self._forex_account_number
    trade.origin = self._origin
    trade.strategy = self._strategy
    trade.comment = self._comment
    trade.state = self._state
    trade.tg_message_id = self._tg_message_id
    trade.tg_sender_id = self._tg_sender_id
    trade.tg_date = self._tg_date
    trade.mt4_ticket_id = self._mt4_ticket_id
    trade.mt4_magic_number = self._mt4_magic_number
    trade.mt4_open_time = self._mt4_open_time

  def get_id(self):
    return self._id

  def modify_tp(self, tp_price):
      tp_price = float(tp_price)
      if self._pip_digits == 5:
        tp_adjust = self._tp_adjust * 10
      else:
        tp_adjust = self._tp_adjust

      if tp_adjust > 0:
        if self._action.lower() == "buy":
          tp_adjust = -tp_adjust

      tp_price = tp_price * self._multiplier
      tp_price = tp_price + tp_adjust
      tp_price = tp_price / self._multiplier
      return tp_price

  def modify_tp_20(self):
      tp_price = float(self._entry)
      tp_20 = 20
      if self._pip_digits == 5:
          tp_adjust = self._tp_adjust * 10
          tp_20 = tp_20 * 10
      else:
          tp_adjust = self._tp_adjust

      if tp_adjust > 0:
          if self._action.lower() == "buy":
              tp_adjust = -tp_adjust

      if self._action.lower() == "sell":
          tp_20 = -tp_20

      tp_price = tp_price * self._multiplier
      tp_price = tp_price + tp_adjust
      tp_price = tp_price + tp_20
      tp_price = tp_price / self._multiplier
      return tp_price

  def calculate_stoploss_pips(self, stop_loss):
      if stop_loss is not None and self._entry is not None:
        entry = float(self._entry)
        stop_loss = float(stop_loss)
        if self._action.lower() == "buy":
          return float((entry - stop_loss) * self._multiplier_for_pips)
        else:
          return float((stop_loss - entry) * self._multiplier_for_pips)
      else:
        return 0

  def calculate_takeprofit_pips(self, take_profit):
      if take_profit is not None and self._entry is not None:
        take_profit = float(take_profit)
        entry = float(self._entry)
        if self._action.lower() == "buy":
          return float((take_profit - entry) * self._multiplier_for_pips)
        else:
          return float((entry - take_profit) * self._multiplier_for_pips)
      else:
        return 0

  def set_mt4_ticket_id(self, mt4_ticket_id):
    self._mt4_ticket_id = mt4_ticket_id

  def set_mt4_open_time(self, mt4_open_time):
    self._mt4_open_time = mt4_open_time

  def set_mt4_magic_number(self, mt4_magic_number):
    self._mt4_magic_number = mt4_magic_number

  def get_strategy(self):
    return self._strategy

