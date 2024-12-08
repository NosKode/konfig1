import os
import tarfile
from datetime import datetime

class FileNotFoundException(Exception):
    """Исключение для случая, когда файл или директория не найдены"""
    pass

class VirtualFileSystem:
    def __init__(self, tar_path):
        self.root = "MyVirtualMachine"  # Корневая папка виртуальной файловой системы
        self.current_path = self.root
        self.load_tar(tar_path)

    def load_tar(self, tar_path):
        """Загружает содержимое TAR-архива в виртуальную файловую систему"""
        if not os.path.exists(tar_path):
            raise FileNotFoundException(f"The TAR file '{tar_path}' does not exist.")
        with tarfile.open(tar_path, "r") as tar:
            tar.extractall(self.root)

    def list_directory(self):
        """Возвращает список файлов и директорий в текущей директории"""
        items = []
        if os.path.exists(self.current_path) and os.path.isdir(self.current_path):
            for file in os.listdir(self.current_path):
                file_path = os.path.join(self.current_path, file)
                size = os.path.getsize(file_path)
                modified_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
                item_type = "Directory" if os.path.isdir(file_path) else "File"
                items.append(f"{item_type:<10} {size:<10} {modified_time} {file}")
        return "\n".join(items)

    def change_directory(self, path):
        """Меняет текущую директорию, проверяя выход за пределы виртуальной файловой системы"""
        new_path = os.path.join(self.current_path, path)
        new_path = os.path.abspath(new_path)  # Преобразуем путь в абсолютный

        # Проверяем, не пытаемся ли мы выйти за пределы корня виртуальной файловой системы
        if not new_path.startswith(os.path.abspath(self.root)):
            raise FileNotFoundException(f"Cannot change directory: '{path}' is outside the virtual file system.")

        # Если путь существует, меняем текущую директорию
        if os.path.isdir(new_path):
            self.current_path = new_path
        else:
            raise FileNotFoundException(f"Directory not found: '{path}'")

    def get_relative_path(self):
        """Возвращает относительный путь от корня виртуальной файловой системы"""
        return os.path.relpath(self.current_path, self.root).replace("\\", "/")

    def read_file(self, file_name):
        """Читает содержимое файла"""
        file_path = os.path.join(self.current_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        else:
            raise FileNotFoundException("File not found")

    def create_or_update_file(self, file_name):
        """Создает или обновляет файл"""
        file_path = os.path.join(self.current_path, file_name)
        with open(file_path, "a", encoding="utf-8") as file:
            os.utime(file_path, None)
