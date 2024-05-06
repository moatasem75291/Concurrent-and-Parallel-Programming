import time
import threading


def calculate_sum_squares(n):
    sum_squares = 0
    for i in range(n):
        sum_squares += i**2

    print(sum_squares)


def sleep_a_little(n):
    time.sleep(n)


def main():
    starting_time = time.time()

    current_threads = []
    for i in range(5):
        maximum_value = (i + 1) * 1000000
        t = threading.Thread(target=calculate_sum_squares, args=(maximum_value,))
        t.start()
        current_threads.append(t)

    for i in range(len(current_threads)):
        current_threads[i].join()

    print(f"Calculating Time square took: {round(time.time() - starting_time, 2)}")

    starting_time = time.time()

    current_threads = []
    for i in range(1, 6):
        t = threading.Thread(target=sleep_a_little, args=(i,))
        t.start()
        current_threads.append(t)

    for i in range(len(current_threads)):
        current_threads[i].join()

    print(f"Sleeping took: {round(time.time() - starting_time, 2)}")


if __name__ == "__main__":
    main()
