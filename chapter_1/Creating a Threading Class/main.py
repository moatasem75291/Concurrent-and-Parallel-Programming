import time
from SleepyWorkers import SleepyWorker
from SquaredSumWorkers import SquaredSumWorker


def main():
    starting_time = time.time()

    current_workers = []
    for i in range(5):
        maximum_value = (i + 1) * 1000000
        squared_sum_worker = SquaredSumWorker(n=maximum_value)
        current_workers.append(squared_sum_worker)

    for i in range(len(current_workers)):
        current_workers[i].join()

    print(f"Calculating Time square took: {round(time.time() - starting_time, 2)}")

    starting_time = time.time()

    current_workers = []
    for i in range(1, 6):
        sleepy_worker = SleepyWorker(seconds=i)
        current_workers.append(sleepy_worker)

    for i in range(len(current_workers)):
        current_workers[i].join()

    print(f"Sleeping took: {round(time.time() - starting_time, 2)}")


if __name__ == "__main__":
    main()
