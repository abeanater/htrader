from abc import ABC, abstractmethod
import dataclasses
from datetime import datetime


@dataclasses.dataclass
class Quote:
    timestamp: datetime
    symbol: str
    security_type: str
    last_trade: float
    change_close: float
    change_close_percent: float
    open_price: float
    previous_close: float
    bid: float
    bid_size: int
    ask: float
    ask_size: int
    low: float
    high: float
    total_volume: int

    def to_json(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "symbol": self.symbol,
            "security_type": self.security_type,
            "last_trade": self.last_trade,
            "change_close": self.change_close,
            "change_close_percent": self.change_close_percent,
            "open_price": self.open_price,
            "previous_close": self.previous_close,
            "bid": self.bid,
            "bid_size": self.bid_size,
            "ask": self.ask,
            "ask_size": self.ask_size,
            "low": self.low,
            "high": self.high,
            "total_volume": self.total_volume
        }

    @staticmethod
    def from_json(self,dict):
        return Quote(
            timestamp = datetime.fromisoformat(dict["timestamp"]),
            symbol = dict["symbol"],
            security_type = dict["security_type"],
            last_trade = dict["last_trade"],
            change_close = dict["change_close"],
            change_close_percent = dict["change_close_percent"],
            open_price = dict["open_price"],
            previous_close = dict["previous_close"],
            bid = dict["bid"],
            bid_size = dict["bid_size"],
            ask = dict["ask"],
            ask_size = dict["ask_size"],
            low = dict["low"],
            high = dict["high"],
            total_volume = dict["total_volume"]
        )


class BaseTradingPlatform(ABC):
    def __init__(self,name):
        self.name = name

    @abstractmethod
    def human_order(self, symbol, quantity, price, order_type) -> bool:
        raise NotImplementedError("human_order method not implemented")

    @abstractmethod
    def limit_order(self, symbol, quantity, price) -> bool:
        raise NotImplementedError("limit_order method not implemented")

    @abstractmethod
    def market_order(self, symbol, quantity) -> bool:
        raise NotImplementedError("market_order method not implemented")

    @abstractmethod
    def get_quote(self, symbol) -> Quote:
        raise NotImplementedError("quote method not implemented")

    @abstractmethod
    def subscribe_quote(self, symbol):
        raise NotImplementedError("subscribe_quote method not implemented")