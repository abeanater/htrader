
import sqlite3
from htrader.storage.base import BaseStorage


class SQLiteStorage(BaseStorage):
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.conn = sqlite3.connect(dbfile)
        self.cursor = self.conn.cursor()

    def save(self, articles):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, ticker TEXT, title TEXT, summary TEXT, link TEXT UNIQUE, date TIMESTAMP, hostname TEXT)')
        for article in articles:
            self.cursor.execute('SELECT * FROM news WHERE title = ? AND date = ?', (article.title, article.date))
            if self.cursor.fetchone() is None:
                try:
                    self.cursor.execute('INSERT OR IGNORE INTO news(ticker, title, summary, link, date, hostname) VALUES (?, ?, ?, ?, ?, ?)', article.to_sql())
                except sqlite3.IntegrityError:
                    print('Something went wrong with', article.title)
            else:
                print('article already exists')
        self.conn.commit()

    def load(self):
        self.cursor.execute('SELECT * FROM news')
        return self.cursor.fetchall()