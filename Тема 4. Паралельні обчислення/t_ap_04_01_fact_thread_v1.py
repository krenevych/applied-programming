# T04/t_ap_04_01_fact_thread_v1.py
from threading import Thread
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG)

def fact(n):
    p = 1
    for i in range(1, n + 1):
        logging.debug('factorial thread i=%s, p=%s', i, p)
        sleep(0)
        p *= i

    logging.debug('%s! = %s', n, p)
    logging.debug('thread finishing')

n = int(input('n=? '))

th = Thread(target=fact, args=(n, ))
th.start()

for k in range(10):
    logging.debug("Tick %s", k)
    sleep(0)
