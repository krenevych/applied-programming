# T04/t_ap_04_01_fact_thread_v3.py
from threading import Thread
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG)

class ThreadWithResult(Thread):
    def __init__(self, target=None, args=(), kwargs=()):
        self._func = target
        self._f_args = args
        self._f_kwargs = kwargs if kwargs else {}
        self._result = None

        Thread.__init__(self, daemon=True)

    def run(self):
        self._result = self._func(*self._f_args, **self._f_kwargs)

    def get_result(self):
        return self._result


def fact(n):
    p = 1
    for i in range(1, n + 1):
        logging.debug('factorial thread i=%s, p=%s', i, p)
        sleep(0)
        p *= i

    logging.debug('thread finishing')
    return p

n = int(input('n=? '))

th = ThreadWithResult(target=fact, args=(n, ))
th.start()

for k in range(10):
    logging.debug("Tick %s", k)
    sleep(0)

th.join()
fct = th.get_result()
logging.debug('%s! = %s', n, fct)
