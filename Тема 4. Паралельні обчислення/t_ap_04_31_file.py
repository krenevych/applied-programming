# T04/t_ap_04_31_file.py
import logging
import hashlib
import os.path as op
from threading import Event


class File:
    """
    Клас містить інформацію про файл.
    Поля:
        self._path: str - повний шлях до файлу
        self._dir: str - повний шлях до каталогу файлу
        self._name: str - ім'я файлу
        self._size: int - розмір файлу
        self._file_hash: str - контрольна сума файлу за md5
        self._cancel - подія відміни (завершення) обчислення
    """
    CHUNK_SIZE = 512 * 1024

    def __init__(self, path):
        self._path = op.abspath(path)
        self._dir, self._name = op.split(self._path)
        self._size = 0
        self._file_hash = ""

        self._cancel = Event()

    @property
    def path(self):
        """
        Властивість, що повертає повний шлях до файлу
        """
        return self._path

    @property
    def name(self):
        """
        Властивість, що повертає ім'я файлу
        """
        return self._name

    @property
    def directory(self):
        """
        Властивість, що повертає повний шлях до каталогу файлу
        """
        return self._dir

    @property
    def size(self):
        """
        Властивість, що повертає розмір файлу
        """
        return self._size

    @property
    def file_hash(self):
        """
        Властивість, що повертає контрольну сума файлу за md5
        """
        return self._file_hash

    def __hash__(self):
        """
        Метод обчислює хеш для об'єктів класу.
        Слугує для утворення множин з об'єктів класу.
        :return: (контрольна сума файлу за md5, розмір файлу)
        """
        return hash((self._file_hash, self.size))

    def calculate_file_hash(self):
        """
        Метод обчислює контрльну суму та розмір файлу
        :return: None
        """
        size = 0
        checksum = hashlib.md5()   # ініціалізація обчислення контрольної суми
        try:
            with open(self._path, 'rb') as f:
                while True:
                    chunk = f.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    if self._cancel.is_set():
                        return

                    size += len(chunk)
                    checksum.update(chunk)

            self._size = size
            self._file_hash = checksum.hexdigest()
        except OSError as e:
            logging.warning("Помилка читання файлу %s", e)

    def __str__(self):
        return self._path

    def quit(self):
        """
        Метод завершує (перериває обробку файлу)
        :return: None
        """
        self._cancel.set()

if __name__ == '__main__':
    file = File('t_ap_04_31_file.py')
    file.calculate_file_hash()
    print("file hash:", file.file_hash,
          "\nfile size:", file.size,
          "\nfile path:", file.path)
