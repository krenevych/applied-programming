# T04/t_ap_04_51_fib_process_pool_v2.py

import os
from concurrent.futures import ProcessPoolExecutor
import random
import logging


def fibrecursive(n):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("process %s, n: %s", os.getpid(), n)
    return fib(n)


def fib(n):
    if n <= 1:
        res = 1
    else:
        res = fib(n-1) + fib(n-2)
    return res


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    k = int(input("fibs count: "))

    n_s = [random.randrange(1, 32) for i in range(k)]
    with ProcessPoolExecutor(max_workers=2) as executor:
        results = executor.map(fibrecursive, n_s)
    fibs = list(zip(n_s, results))

    logging.debug("Results: %s", fibs)
