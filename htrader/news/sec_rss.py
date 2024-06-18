import requests
import xmltodict
import logging
from dataclasses import dataclass
from typing import Generator
from datetime import datetime

@dataclass
class DocumentData:
    document_link: str
    pubDate: datetime
    company_name: str
    cik_number: int

    def __str__(self):
        return f"DocumentData(document_link={self.document_link}, pubDate={self.pubDate}, company_name={self.company_name}, cik_number={self.cik_number})"


class SecRssClient():
    def __init__(self):
        self.REQUEST_INTERVAL = 0.3
        self.logger = logging.getLogger()

    def get_ticker_symbol(self, cik_number):
        url = f"https://data.sec.gov/submissions/CIK{cik_number}.json"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            ticker_symbol = data.get('tickers', [])[0] if data.get('tickers') else None
            return ticker_symbol
        else:
            return None

    def __call__(self) -> Generator[DocumentData, None, None]:
        rss_url = 'https://www.sec.gov/Archives/edgar/xbrlrss.all.xml'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(rss_url, headers=headers)
        if response.status_code == 200:
            feed = xmltodict.parse(response.content)
            for item in feed['rss']['channel']['item']:
                xbrlFiling = item['edgar:xbrlFiling']
                form_type = xbrlFiling['edgar:formType']
                pubDate = item['pubDate']
                if form_type in ['8-K', '8-K/A', '6-K']:
                    company_name = xbrlFiling['edgar:companyName']
                    cik_number = xbrlFiling['edgar:cikNumber']
                    document_links = [xbrlFile['@edgar:url'] for xbrlFile in xbrlFiling['edgar:xbrlFiles']['edgar:xbrlFile'] if xbrlFile['@edgar:url'].endswith(('.htm', '.html'))]

                    for document_link in document_links:
                        yield DocumentData(document_link, pubDate, company_name, cik_number)