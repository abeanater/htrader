from abc import ABC, abstractmethod
from dataclasses import dataclass

class NewsArticle:
    def __init__(self, ticker,title, content, url, date, source):
        self.ticker = ticker
        self.title = title
        self.content = content
        self.url = url
        self.date = date
        self.source = source

    @staticmethod
    def from_gnews_dict(data,ticker=None):
        return NewsArticle(data['ticker'], data['title'], data['desc'], data['link'], data['datetime'], data['media'])

    def __str__(self):
        return f"{self.title} - {self.date} - {self.source}"

    def __repr__(self):
        return f"{self.title} - {self.date} - {self.source}"

    def to_sql(self):
        return (self.ticker, self.title, self.content, self.url, self.date, self.source)

class BaseNewsService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_news(self):
        raise NotImplementedError

    @abstractmethod
    def __call__(self,name):
        raise NotImplementedError