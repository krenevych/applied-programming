# T04/t_ap_04_51_fib_process_pool_v1.py

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


def process_done(fut):
    fibs.append((futs[fut], fut.result()))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    fibs = []
    futs = {}
    executor = ProcessPoolExecutor(max_workers=2)

    k = int(input("fibs count: "))

    for i in range(k):
        n = random.randrange(1, 32)
        logging.debug("starting process for %s", n)
        fut = executor.submit(fibrecursive, n)
        futs[fut] = n
        fut.add_done_callback(process_done)

    executor.shutdown(wait=True)
    logging.debug("Results: %s", fibs)

