# T04/t_ap_04_01_fact_thread_v0.py
from threading import Thread
from time import sleep


def fact(n):
    p = 1
    for i in range(1, n + 1):
        print('factorial thread', i, p)
        sleep(0)
        p *= i

    print(n, '! = ', p)
    print('thread finishing')

n = int(input('n=? '))

th = Thread(target=fact, args=(n, ))
th.start()

for k in range(10):
    print("Tick", k)
    sleep(0)
