# T04/t_ap_04_41_fact_process_v1.py
import os
from multiprocessing import Process
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG)

def fact(n):
    p = 1
    pid = os.getpid()
    for i in range(1, n + 1):
        logging.debug('factorial process pid %s, i=%s, p=%s', pid, i, p)
        p *= i

    logging.debug('%s! = %s', n, p)
    logging.debug('process finishing')

if __name__ == '__main__':
    pid = os.getpid()
    n = int(input('n=? '))

    ps = Process(target=fact, args=(n, ))
    ps.start()

    for k in range(20):
        logging.debug("Pid: %s. Tick %s", pid, k)
        sleep(0)
