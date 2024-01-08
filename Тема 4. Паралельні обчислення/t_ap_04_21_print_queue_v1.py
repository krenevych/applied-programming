# T04/t_ap_04_21_print_queue_v1.py
from threading import Thread, Event
from queue import Queue


class PrintQueue:
    """
    Клас підтримує чергу ддя показу результатів за допомогою стандартного print
    Поля класу:
        self._queue - черга виведення
        self._thread - потік, що обробляє чергу виведення
        self._thread_stopped - подія, чи завершено роботу потоку
    """
    def __init__(self):
        self._queue = Queue()
        self._thread = Thread(target=self._run, daemon=True)
        self._thread_stopped = Event()
        self._thread.start()

    def _run(self):
        """
        Метод працює у потоці, що разбирає чергу та здійснює показ результатів
        :return: None
        """
        while True:
            print_args = self._queue.get()
            if print_args is None:
                break

            print(*print_args)

    def print(self, *args):
        """
        Метод додає кортеж з аргументами args у чергу.
        Якщо потік вже завершив роботу - ініціює виключкення RuntimeError
        :param args: кортеж з аргументами
        :return: None
        """
        if self._thread_stopped.is_set():
            raise RuntimeError("Спроба викликати print після зупинки потоку")

        self._queue.put(args)

    def stop(self):
        """
        Метод завершує роботу потоку показу результатів
        :return: None
        """
        if not self._thread_stopped.is_set():
            self._thread_stopped.set()
            self._queue.put(None)
            self._thread.join()


printer = PrintQueue()
