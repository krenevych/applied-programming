# T04/t_ap_04_33_dirs_forest.py

from collections import defaultdict
from threading import Event

from t_ap_04_32_dir_tree import DirTree


class DirsForest:
    """
    Клас обробляє та містить інформацію про ліс каталогів.
    Поля:
        self._trees: list - список дерев каталогів
        self._files_hashes: dict - словник, що містить множини однакових файлів
        self._trees_adding: dict - словник, що містить дерева, які додаються
    """

    def __init__(self):
        self._trees = []
        self._files_hashes = defaultdict(set)

        self._cancel = Event()
        self._trees_adding = dict()

    @property
    def trees(self):
        """
        Властивість, що повертає список дерев каталогів
        """
        return self._trees

    @property
    def files_hashes(self):
        """
        Властивість, що повертає словник, що містить множини однакових файлів
        """
        return self._files_hashes

    def add_tree(self, path):
        """
        Метод додає дерево каталогів за шляхом до кореневого каталогу
        Добудовує словник, що містить множини однакових файлів
        :return: None
        """
        if any(path in tree for tree in self._trees):
            # якщо шлях э частиною одного з наявних дерев катлогів
            return

        new_tree = DirTree(path)
        # видалити зі списку усі дерева, які э піддеревами path
        for tree in self._trees[:]:
            if tree.path in new_tree:
                self._trees.remove(tree)

        self._trees_adding[path] = new_tree
        new_tree.scan()
        self._trees_adding.pop(path, None)
        if self._cancel.is_set():
            return

        self._trees.append(new_tree)

        for file in new_tree.all_child_files():
            self._files_hashes[(file.file_hash, file.size)].add(file)

    def quit(self):
        """
        Метод завершує (перериває обробку дерев каталогів)
        :return: None
        """
        self._cancel.set()
        for _, tree in self._trees_adding.items():
            tree.quit()
        self._trees_adding.clear()


if __name__ == '__main__':
    forest = DirsForest()
    forest.add_tree('..')
    forest.add_tree('.')

    max_equal = 1
    for file_hash in forest.files_hashes:
        max_equal = max(max_equal, len(forest.files_hashes[file_hash]))
    print("максимальна кількість однакових файлів:", max_equal)
