# T04/t_ap_04_01_fact_thread_v2.py
from threading import Thread
from time import sleep

ver = int(input('print_queue version [1-2]:'))
if ver == 1:
    from T04.t_ap_04_21_print_queue_v1 import printer
else:
    from T04.t_ap_04_21_print_queue_v2 import printer


def fact(n):
    p = 1
    for i in range(1, n + 1):
        printer.print('factorial thread', i, p)
        sleep(0)
        p *= i

    printer.print(n, '! = ', p)
    printer.print('thread finishing')


n = int(input('n=? '))

th = Thread(target=fact, args=(n, ), daemon=True)
th.start()

for k in range(10):
    printer.print("Tick", k)
    sleep(0)

th.join()
printer.stop()
