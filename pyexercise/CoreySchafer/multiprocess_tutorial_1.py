import multiprocessing
import time


def do_something():

    print('Sleeping 1 second...')
    time.sleep(1)
    print('Done sleeping...')

if __name__ == '__main__': # must be covered by this statement in windows

    start = time.perf_counter()

    p1 = multiprocessing.Process(target=do_something)
    p2 = multiprocessing.Process(target=do_something)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    finish = time.perf_counter()

    print(f"Finished in {round(finish-start, 2)} second(s)")
