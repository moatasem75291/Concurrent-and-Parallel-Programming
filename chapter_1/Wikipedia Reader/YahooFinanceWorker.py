import threading
import time, random
import requests
from lxml import etree


class YahooFinanceWorker(threading.Thread):
    def __init__(self, symbol, **kwargs):
        super(YahooFinanceWorker, self).__init__(**kwargs)
        self._symbol = symbol
        base_url = "https://finance.yahoo.com/quote/"
        self._url = f"{base_url}{self._symbol}"
        self.start()

    def _extract_price(self):
        time.sleep(random.randint(30, 60))
        response = requests.get(self._url)
        if response.status_code != 200:
            print(f"Couldn't get data for {self._symbol}")
        else:
            parser = etree.HTMLParser()
            tree = etree.fromstring(response.text, parser)
            xpath_expr = "//*[@id='nimbus-app']/section/section/section/article/section[1]/div[2]/div[1]/section/div/section[1]/div[1]/fin-streamer[1]"
            element = tree.xpath(xpath_expr)[0]
            price = element.find(".//span").text

            print(f"{self._symbol}: {price}")

    def run(self):
        self._extract_price()
