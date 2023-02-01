from multiprocessing import Pool, cpu_count, RLock
from time import time
import logging


def factorize(*number):
    result_list = []
    for num in number:
        num_list = []
        for i in range(1, num + 1):
            if num % i == 0:
                num_list.append(i)
        result_list.append(num_list)
    print(result_list)
    return result_list


def single_pr():
    start = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    logging.debug("Single process time: {:10f} sec".format(time() - start))


def multi_pr():
    start = time()
    with Pool(cpu_count()) as pool:
        a, b, c, d = pool.map(factorize, (128, 255, 99999, 10651060))
    pool.close()
    pool.join()
    logging.debug("Multi process time: {:10f} sec".format(time() - start))


if __name__ == "__main__":
    lock = RLock()
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    single_pr()
    print(f"Count CPU: {cpu_count()}")
    multi_pr()
