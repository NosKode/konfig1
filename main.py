import argparse
import tkinter as tk
from tkinter import scrolledtext
from command_handler import CommandHandler
from virtual_file_system import VirtualFileSystem


class ShellEmulatorApp:
    def __init__(self, master, username, computername, vfs, log_file):
        self.master = master
        self.username = username
        self.computername = computername
        self.vfs = vfs
        self.command_handler = CommandHandler(vfs, log_file, username, self.write_output)

        # Настройка окна
        self.master.title("Shell Emulator")
        self.master.geometry("800x600")

        # Поле для вывода
        self.output_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state=tk.DISABLED, font=("Courier", 12))
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Поле ввода
        self.input_frame = tk.Frame(self.master)
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)
        self.command_entry = tk.Entry(self.input_frame, font=("Courier", 12))
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.command_entry.bind("<Return>", self.execute_command)

        # Кнопка для отправки команды
        self.execute_button = tk.Button(self.input_frame, text="Execute", command=self.execute_command)
        self.execute_button.pack(side=tk.RIGHT, padx=5)

        # Приветственное сообщение
        self.write_output(f"Welcome, {self.username}! Type 'exit' to quit.\n")

        # Показать приглашение сразу при запуске
        self.write_prompt()

    def execute_command(self, event=None):
        command = self.command_entry.get().strip()
        if command:
            # Показать команду только после вывода приглашения
            prompt = f"{command}\n"
            self.write_output(prompt)  # Печатаем команду

            # Выполняем команду
            self.command_entry.delete(0, tk.END)
            try:
                if command == "exit":
                    self.master.quit()
                else:
                    self.command_handler.execute_command(command)
            except Exception as e:
                self.write_output(f"Error: {e}\n")

            # После выполнения команды, выводим результат и строку приглашения
            self.write_prompt()

    def write_prompt(self):
        """Печатает строку приглашения с текущей директорией"""
        self.write_output(f"\n{self.username}@{self.computername}:{self.vfs.get_relative_path()}$ ")

    def write_output(self, text):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, text)
        self.output_area.config(state=tk.DISABLED)
        self.output_area.see(tk.END)


def main():
    # Парсинг аргументов
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--username", required=True, help="Имя пользователя для shell")
    parser.add_argument("--computername", required=True, help="Имя компьютера для shell")
    parser.add_argument("--tar", required=True, help="Путь к tar-архиву виртуальной файловой системы")
    parser.add_argument("--log", required=True, help="Путь к файлу логов (CSV)")
    args = parser.parse_args()

    # Инициализация виртуальной файловой системы
    vfs = VirtualFileSystem(args.tar)

    # Запуск GUI
    root = tk.Tk()
    app = ShellEmulatorApp(root, args.username, args.computername, vfs, args.log)
    root.mainloop()


if __name__ == "__main__":
    main()
