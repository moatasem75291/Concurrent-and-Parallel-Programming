import time
from WikipediaReader import WikipediaReader
from YahooFinanceWorker import YahooFinanceWorker
import itertools


def main():
    current_time = time.time()

    wiki_reader = WikipediaReader()
    wiki_workers = []
    symbols = wiki_reader.get_sp_500_companies()
    for symbol in itertools.islice(symbols, 100):
        worker = YahooFinanceWorker(symbol)
        wiki_workers.append(worker)

    for worker in wiki_workers:
        worker.join()

    print(f"Execution time: {time.time() - current_time}")


if __name__ == "__main__":
    main()
