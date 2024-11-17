import pandas as pd
import yfinance as yf
from htrader.news.gnews import GoogleNewsClient
from htrader.news.ynews import YahooNewsClient
import json
import Path

def read_tickers(data_dir):
    with open(Path(data_dir) / "tickers.txt", 'r') as f:
        tickers = f.read().split('\n')
    return tickers

if __name__ == '__main__':
    p = Path(__file__).parent / 'config.json'
    config = json.load(p)
    data_dir = config['data_dir']

    download = False
    df = None
    if download:
        data = []
        tickers = read_tickers(data_dir)
        total_tickers = len(tickers)
        for i, ticker in enumerate(tickers):
            print(f"Processing {i}/{total_tickers} - {ticker}")
            df = yf.Ticker(ticker).history(period='5y',interval='1d')
            df['ticker'] = ticker
            data.append(df)
        df = pd.concat(data)
        df.to_parquet(Path(data_dir) / "historical_data.parquet")
    else:
        df = pd.read_parquet(Path(data_dir) / "historical_data.parquet")
    df['pct_change'] = (df.Close - df.Open)/df.Open*100
    df['Date'] = pd.to_datetime(df['Date'])
    df.dropna(subset=['pct_change'], inplace=True)
    df.dropna(subset=['Date'], inplace=True)
    top_pct_changes = df.loc[df.groupby(df.Date)['pct_change'].idxmax()]
    # for each date, get the top 10 pct changes
    top_10_pct_changes = df.groupby('Date').apply(lambda x: x.nlargest(10, 'pct_change')).reset_index(drop=True)
    for date, group in top_10_pct_changes.groupby('Date'):
        for ticker in group['ticker']:
            start_date = end_date = date.strftime('%Y-%m-%d')
            news_client = GoogleNewsClient(start_date=start_date, end_date=end_date)
            y_news_client = YahooNewsClient()
            news = news_client.get_news(ticker)
            y_news = y_news_client.get_news(ticker)
            
            print(f"News for {ticker} on {date}: {news}")