import feedparser
import json
import htrader.news.base as base
from urllib.parse import urlparse
from datetime import datetime
from time import mktime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
rssfeedurl = 'https://feeds.finance.yahoo.com/rss/2.0/headline?s={}&region=US&lang=en-US'

class YahooNewsClient(base.BaseNewsService):
    def __init__(self):
        super().__init__()

    def get_news(self, ticker):
        feed = feedparser.parse(rssfeedurl.format(ticker))
        return [base.NewsArticle(ticker, e.title, e.summary, e.link, datetime.fromtimestamp(mktime(e.published_parsed)), urlparse(e.link).hostname) for e in feed.entries]

    def __call__(self, ticker):
        return self.get_news(ticker)