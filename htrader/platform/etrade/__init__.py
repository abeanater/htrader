
from htrader.platform.base_platform import BaseTradingPlatform, Quote
import requests
import json
from datetime import datetime


class EtradePythonClient(BaseTradingPlatform):
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret
        self.session = None
        self.base_url = "https://api.etrade.com"

    def authenticate(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })

    def get_quote(self,symbol):
        """
            Calls quotes API to provide quote details for equities, options, and mutual funds
        """
        # URL for the API endpoint
        url = self.base_url + "/v1/market/quote/" + symbol + ".json"

        # Make API call for GET request
        response = self.session.get(url)
        if response is  None or response.status_code != 200:
            return None
        parsed = json.loads(response.text)
        data = response.json()
        if data is None or "QuoteResponse" not in data or "QuoteData" not in data["QuoteResponse"]:
            return None

        quotes = []
        for quote_data in data["QuoteResponse"]["QuoteData"]:
            if quote_data is not None:
                quote = Quote(
                    timestamp=datetime.strptime(quote_data.get("dateTime", ""), "%Y-%m-%dT%H:%M:%S.%fZ"),
                    symbol=quote_data.get("Product", {}).get("symbol", ""),
                    security_type=quote_data.get("Product", {}).get("securityType", ""),
                    last_trade=quote_data.get("All", {}).get("lastTrade", 0.0),
                    change_close=quote_data.get("All", {}).get("changeClose", 0.0),
                    change_close_percent=quote_data.get("All", {}).get("changeClosePercentage", 0.0),
                    open_price=quote_data.get("All", {}).get("open", 0.0),
                    previous_close=quote_data.get("All", {}).get("previousClose", 0.0),
                    bid=quote_data.get("All", {}).get("bid", 0.0),
                    bid_size=quote_data.get("All", {}).get("bidSize", 0),
                    ask=quote_data.get("All", {}).get("ask", 0.0),
                    ask_size=quote_data.get("All", {}).get("askSize", 0),
                    low=quote_data.get("All", {}).get("low", 0.0),
                    high=quote_data.get("All", {}).get("high", 0.0),
                    total_volume=quote_data.get("All", {}).get("totalVolume", 0)
                )
                quotes.append(quote)
        return quotes

