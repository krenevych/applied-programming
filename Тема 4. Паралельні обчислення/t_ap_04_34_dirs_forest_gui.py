# T04/t_ap_04_33_dirs_forest.py

from tkinter import *
from tkinter.filedialog import askdirectory
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from t_ap_04_33_dirs_forest import DirsForest


class DirsForestGui:
    """
    Клас реалізує графічний інтерфейс для лісу каталогів.
    Поля:
        self._dirs_forest: ліс каталогів
        self._top - вікно верхнього рівня
        self._executor - пул потоків для дерев каталогів
        self._tree_futures - майбутні виклики для дерев каталогів
        self._to_add_list_box - список каталогів, що додаються
        self._added_list_box - список каталогів, що додані
    """
    FILENAME = "dir_forest_files.txt"

    def __init__(self):
        self._dirs_forest = DirsForest()
        self._top = Tk()
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._tree_futures = deque()


        self._make_widgets()
        self._poll()
        self._top.mainloop()

    def _make_widgets(self):
        self._font = ("Arial", 16)
        self._top.title("Дерева каталогів")

        to_add_list_frame = Frame(self._top)
        self._to_add_scroll = Scrollbar(to_add_list_frame)
        self._to_add_scroll.pack(side=RIGHT, fill=Y)
        self._to_add_list_box = Listbox(
            to_add_list_frame, width=100, height=15,
            yscrollcommand=self._to_add_scroll.set,
            font=self._font)
        self._to_add_scroll.config(command=self._to_add_list_box.yview)
        self._to_add_list_box.pack(side=RIGHT, fill=BOTH, expand=YES)
        to_add_list_frame.pack(side=TOP, fill=BOTH, expand=YES)

        added_list_frame = Frame(self._top)
        self._added_scroll = Scrollbar(added_list_frame)
        self._added_scroll.pack(side=RIGHT, fill=Y)
        self._added_list_box = Listbox(
            added_list_frame, width=100, height=15,
            yscrollcommand=self._added_scroll.set,
            font=self._font)
        self._added_scroll.config(command=self._added_list_box.yview)
        self._added_list_box.pack(side=RIGHT, fill=BOTH, expand=YES)
        added_list_frame.pack(side=TOP, fill=BOTH, expand=YES)

        # рамка та кнопки
        bfm = Frame(self._top)
        Button(bfm, text='Додати',command=self._add_handler,
               font=self._font)\
            .pack(side=RIGHT, padx=5, pady=5)
        Button(bfm, text='Зберегти', command=self._save_handler,
               font=self._font)\
            .pack(side=RIGHT, padx=5, pady=5)
        Button(bfm, text='Закрити', command=self._close_handler,
               font=self._font)\
            .pack(side=RIGHT, padx=5, pady=5)
        bfm.pack(fill=X, expand=YES)

    def _add_handler(self):
        """
        Метод обробляє натиснення кнопки "Додати"
        :return: None
        """
        dir_path = askdirectory()
        if not dir_path:
            return

        self._to_add_list_box.insert(END, dir_path)
        self._add_tree(dir_path)

    def _add_tree(self, dir_path):
        """
        Метод ініціює додавання 1 дерева катлогів
        :param dir_path: дерево каталогів
        :return: None
        """
        fut = self._executor.submit(self._dirs_forest.add_tree, dir_path)
        self._tree_futures.append(fut)

    def _poll(self):
        """
        Метод викликається щосекунди та перевіряє,
        чи завершилась обробка одного дерева.
        Якщо так, то переносить каталог зі списку тих, що додаються,
        у список тих, що додані
        :return: None
        """
        if self._tree_futures:
            try:
                self._tree_futures[0].result(timeout=0.01)
                # потік додавання дерева катлогів завершив роботу
                path = self._to_add_list_box.get(0)
                self._to_add_list_box.delete(0)
                self._added_list_box.insert(END, path)
                self._tree_futures.popleft()
            except TimeoutError:
                pass

        self._top.after(1000, self._poll)

    def _close_handler(self):
        """
        Метод обробляє натиснення кнопки "Закрити"
        :return: None
        """
        for fut in self._tree_futures:
            fut.cancel()
        self._dirs_forest.quit()
        self._top.quit()

    def _save_handler(self):
        """
        Метод обробляє натиснення кнопки "Зберегти"
        :return: None
        """
        files_dict = self._dirs_forest.files_hashes
        with open(self.FILENAME, 'w', encoding='utf-8') as f:
            for (hs, size), files_set in files_dict.items():
                files_str = ' '.join(f.path for f in files_set)
                line = "{}, {}: {}\n".format(hs, size, files_str)
                f.write(line)


if __name__ == '__main__':
    forest_gui = DirsForestGui()
