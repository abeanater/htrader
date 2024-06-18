from GoogleNews import GoogleNews


class GoogleNewsClient():
    def __init__(self):
        self.gnews = GoogleNews()
        self.gnews.set_lang('en')
        self.gnews.set_period('7d')
        self.gnews.set_encode('utf-8')
        self.gnews.set_time_range('02/19/2024','03/02/2024')


    def __call__(self,name):
        self.gnews.get_news(name)
        for r in self.gnews.results():
            yield r