import time
from WikipediaReader import WikipediaReader
from YahooFinanceWorker import YahooFinanceScheduler
from PostgresWorker import PostgresMasterScheduler
from multiprocessing import Queue
import itertools


def main():

    symbol_queue = Queue()
    postgres_queue = Queue()
    current_time = time.time()

    wiki_reader = WikipediaReader()

    num_yahoo_finance_worker = 12
    yahoo_scheduler_threads = []
    for _ in range(num_yahoo_finance_worker):
        yahooFinanceScheduler = YahooFinanceScheduler(
            input_queue=symbol_queue, output_queue=postgres_queue
        )
        yahoo_scheduler_threads.append(yahooFinanceScheduler)

    num_postgres_worker = 6
    postgres_scheduler_threads = []
    for _ in range(num_postgres_worker):
        postgress_Scheduler = PostgresMasterScheduler(input_queue=postgres_queue)
        postgres_scheduler_threads.append(postgress_Scheduler)

    for symbol in wiki_reader.get_sp_500_companies():
        symbol_queue.put(symbol)

    for _ in range(len(yahoo_scheduler_threads)):
        symbol_queue.put("DONE")

    for i in range(len(yahoo_scheduler_threads)):
        yahoo_scheduler_threads[i].join()

    print(f"Execution time: {time.time() - current_time}")


if __name__ == "__main__":
    main()
