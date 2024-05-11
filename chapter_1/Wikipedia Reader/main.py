import time
from WikipediaReader import WikipediaReader
from YahooFinanceWorker import YahooFinanceScheduler
from multiprocessing import Queue
import itertools

num_yahoo_finance_worker = 17


def main():
    current_time = time.time()
    symbol_queue = Queue()

    wiki_reader = WikipediaReader()

    yahoo_scheduler_threads = []
    for _ in range(num_yahoo_finance_worker):
        yahooFinanceScheduler = YahooFinanceScheduler(input_queue=symbol_queue)
        yahoo_scheduler_threads.append(yahooFinanceScheduler)

    for symbol in wiki_reader.get_sp_500_companies():
        symbol_queue.put(symbol)

    for _ in range(len(yahoo_scheduler_threads)):
        symbol_queue.put("DONE")

    for i in range(len(yahoo_scheduler_threads)):
        yahoo_scheduler_threads[i].join()

    print(f"Execution time: {time.time() - current_time}")


if __name__ == "__main__":
    main()
