import multiprocessing
import time


def do_something():

    print('Sleeping 1 second...')
    time.sleep(1)
    print('Done sleeping...')

if __name__ == '__main__':

    start = time.perf_counter()

    processes = []

    for _ in range(10):
        p1 = multiprocessing.Process(target=do_something)
        p1.start()
        processes.append(p1)

    for process in processes:
        process.join()

    finish = time.perf_counter()

    print(f"Finished in {round(finish-start, 2)} second(s)")
