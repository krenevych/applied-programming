# T04/t_ap_04_11_count_in_threads_v1.py

from threading import Thread

MAX_NUM = 100000


def counter():
    global count

    for i in range(MAX_NUM):
        count += 1


for k in range(10):
    count = 0
    thread1 = Thread(target=counter)
    thread2 = Thread(target=counter)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print('k=', k, 'count=', count)
