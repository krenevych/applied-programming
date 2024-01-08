# T04/t_ap_04_32_dir_tree.py

import os
import os.path as op
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from threading import Event

from t_ap_04_31_file import File

class DirTree:
    """
    Клас обробляє та містить інформацію про дерево каталогів.
    Поля:
        self._path: str - повний шлях до кореневого каталогу дерева
        self._dir: str - повний шлях до батьківського каталогу
        self._name: str - ім'я каталогу
        self._subdirs: list - список підкаталогів
        self._files: list - список файлів
        self._files_futures - список майбутніх викликів для файлів
    """

    def __init__(self, path):
        self._path = op.abspath(path)
        self._dir, self._name = op.split(self._path)
        self._subdirs = []
        self._files = []

        self._cancel = Event()
        self._files_futures = {}

    @property
    def path(self):
        """
        Властивість, що повертає повний шлях до кореневого каталогу дерева
        """
        return self._path

    @property
    def name(self):
        """
        Властивість, що повертає ім'я каталогу
        """
        return self._name

    @property
    def directory(self):
        """
        Властивість, що повертає повний шлях до батьківського каталогу
        """
        return self._dir

    @property
    def subdirs(self):
        """
        Властивість, що повертає список підкаталогів
        """
        return self._subdirs

    @property
    def files(self):
        """
        Властивість, що повертає список файлів
        """
        return self._files

    def all_child_dirs(self):
        """
        Метод повертає список усіх підкаталогів, які є у дереві на всіх рівнях
        :return: list - список підкаталогів - об'єктів класу DirTree
        """
        dirs_deque = deque([self])
        children = [self]
        while dirs_deque:
            subdir = dirs_deque.popleft()
            children.extend(subdir.subdirs)
            dirs_deque.extend(subdir.subdirs)
        return children

    def all_child_files(self):
        """
        Метод повертає список усіх файлів, які є у дереві на всіх рівнях
        :return: list - список файлів - об'єктів класу File
        """
        dirs_deque = deque([self])
        children = []
        while dirs_deque:
            subdir = dirs_deque.popleft()
            children.extend(subdir.files)
            dirs_deque.extend(subdir.subdirs)
        return children

    def scan(self):
        """
        Метод сканує дерево каталогів.
        Наповнює дерево підкаталогів.
        Обчислює контрольні суми для всіх файлів.
        :return: None
        """
        files_executor = ThreadPoolExecutor(max_workers=4)
        self._scan(files_executor)
        files_executor.shutdown(wait=True)

    def _scan(self, files_executor):
        """
        Внутрішній рекурсивний метод, що виконує основну роботу scan
        :param files_executor: пул потоків
        :return: None
        """
        items = os.listdir(self._path)
        for item in items:
            if self._cancel.is_set():
                return

            full_path = op.join(self._path, item)
            if op.isdir(full_path):
                # обробити підкаталог
                new_dir = DirTree(full_path)
                self._subdirs.append(new_dir)
                new_dir._scan(files_executor)
            elif op.isfile(full_path):
                # обробити файл
                new_file = File(full_path)
                self._files.append(new_file)
                # ініціювати потік обчислення контрольної суми файлу
                fut = files_executor.submit(new_file.calculate_file_hash)
                fut.add_done_callback(self._task_done)
                self._files_futures[fut] = new_file

    def _task_done(self, fut):
        """
        Метод викликається, коли обробка 1 файлу завершена
        :param fut: майбутній виклик, що виконався
        :return: None
        """
        self._files_futures.pop(fut, None)

    def __contains__(self, path):
        """
        Перевірити, чи входить шлях у дерево каталогів
        :param path: шлях
        :return: bool
        """
        tree_parts = self._path.split(os.sep)
        path_parts = path.split(os.sep)
        try:
            contains = all(tree_parts[i] == path_parts[i]
                           for i in range(len(tree_parts)))
        except IndexError:
            contains = False
        return contains

    def __str__(self):
        return self._path

    def quit(self):
        """
        Метод завершує (перериває обробку дерева каталогів)
        :return: None
        """
        self._cancel.set()
        for subdir in self.subdirs:
            subdir.quit()

        # запобігти виключенню через можливу зміну словника у циклі
        # може статись у _task_done, який викликається з іншого потоку
        items = list(self._files_futures.items())
        for fut, file in items:
            if not fut.cancel():
                file.quit()


if __name__ == '__main__':
    d = DirTree('.')
    d.scan()
    print("files: ", list(str(f) for f in d.all_child_files()))
    print("subdirs:", list(str(s) for s in d.all_child_dirs()))
    if d.files:
        print('{} contains {} is {}'.format(
            d, d.files[0].path, d.files[0].path in d))
