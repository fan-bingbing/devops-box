import multiprocessing
import time
import concurrent.futures


def do_something(seconds):

    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return 'Done sleeping...'

if __name__ == '__main__':

    start = time.perf_counter()

    processes = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        
        results = [executor.submit(do_something, 1) for _ in range(10)]

        for f in concurrent.futures.as_completed(results):
            print(f.result())

    finish = time.perf_counter()

    print(f"Finished in {round(finish-start, 2)} second(s)")
