import threading
import time, random, datetime
import requests
from lxml import etree
from multiprocessing import Queue
from typing import Optional


class YahooFinanceScheduler(threading.Thread):
    def __init__(self, input_queue: Queue, output_queue: Queue, **kwargs) -> None:
        super(YahooFinanceScheduler, self).__init__(**kwargs)
        self._input_queue: Queue = input_queue
        self._output_queue = output_queue
        self.start()

    def run(self) -> None:
        while True:
            val: str = self._input_queue.get()
            if val == "DONE":
                if self._output_queue is not None:
                    self._output_queue.put("DONE")
                break

            yahooFinanceWorker: YahooFinanceWorker = YahooFinanceWorker(symbol=val)
            price: Optional[str] = yahooFinanceWorker.extract_price()
            if self._output_queue is not None:
                output_values = (
                    val,
                    price,
                    datetime.datetime.now(datetime.timezone.utc),
                )
                self._output_queue.put(output_values)

            time.sleep(random.randint(15, 30))


class YahooFinanceWorker:
    def __init__(self, symbol: str) -> None:
        self._symbol: str = symbol
        base_url: str = "https://finance.yahoo.com/quote/"
        self._url: str = f"{base_url}{self._symbol}"

    def extract_price(self) -> Optional[str]:

        response = requests.get(self._url)
        if response.status_code != 200:
            print(f"Couldn't get data for {self._symbol}")
        else:
            try:
                parser = etree.HTMLParser()
                tree = etree.fromstring(response.text, parser)
                xpath_expr = "//*[@id='nimbus-app']/section/section/section/article/section[1]/div[2]/div[1]/section/div/section[1]/div[1]/fin-streamer[1]"
                element = tree.xpath(xpath_expr)[0]
                price = element.find(".//span").text

                float(price.replace(",", ""))
            except:
                return None
            return price
