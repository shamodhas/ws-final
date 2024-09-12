from sqlalchemy import Column, Integer, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class CurrencyType(enum.Enum):
    USD = "USD"
    BTC = "BTC"

class TradeType(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True, index=True)
    usd_amount = Column(Float, default=0.0)
    btc_amount = Column(Float, default=0.0)
    currency = Column(Enum(CurrencyType))
    trade_type = Column(Enum(TradeType))
