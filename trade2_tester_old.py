from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy_base import Base
from trade import Trade, TradeWrapper
import datetime

engine = create_engine("mysql://forex:forex@192.168.21.151:3306/test", echo=True)

Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

channel = "(PREMIUM) CHRIS GROUP1"
sender_id = "1232352352"
message_id = "45"
event_date=datetime.datetime(2019, 11, 1, 15, 20, 54, tzinfo=datetime.timezone.utc)
raw_text = 'AUDUSD BUY:\n\nENTRY: 0.69156\n\nTP: 0.69564\n\nSL: 0.68785'
trade = Trade()
trade_wrapper = TradeWrapper(trade, raw_text=raw_text, origin="TG%s" % channel, tg_sender_id=sender_id,
              tg_message_id=message_id, tg_date=event_date, state="receieved")
last_trade_id = trade_wrapper.get_id()
print(last_trade_id)

session.add(trade)
session.commit()
session.close()

session = Session()
trades = session.query(Trade).all()
for trade in trades:
    print("%s: %s: %s" % (trade.id, trade.forex_pair, trade.action))

session.close()


