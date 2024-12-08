import csv
import time
from virtual_file_system import FileNotFoundException

class CommandHandler:
    def __init__(self, vfs, log_file_path, username, output_callback):
        self.vfs = vfs
        self.log_file_path = log_file_path
        self.username = username
        self.output_callback = output_callback

    def execute_command(self, command):
        if command.startswith("ls"):
            self.list_directory()
        elif command.startswith("cd"):
            self.change_directory(command)
        elif command.startswith("exit"):
            self.exit()
        elif command.startswith("tac"):
            self.tac(command)
        elif command.startswith("touch"):
            self.touch(command)
        else:
            self.output_callback(f"Unknown command: {command}\n")

    def list_directory(self):
        result = self.vfs.list_directory()
        self.output_callback(result)
        self.log_action("ls", result)

    def change_directory(self, command):
        path = command[2:].strip()
        try:
            self.vfs.change_directory(path)
            self.log_action("cd", f"Changed directory to {path}")
        except FileNotFoundException as e:
            self.output_callback(f"Error: {e}\n")

    def exit(self):
        self.log_action("exit", "Exiting emulator")
        self.output_callback("Goodbye!\n")
        exit(0)

    def tac(self, command):
        args = command.split()
        if len(args) == 2:
            file_name = args[1]
            try:
                content = self.vfs.read_file(file_name)
                reversed_content = "\n".join(content.splitlines()[::-1])
                self.output_callback(reversed_content)
                self.log_action("tac", f"Reversed content of {file_name}")
            except FileNotFoundException as e:
                self.output_callback(f"Error: {e}\n")
        else:
            self.output_callback("Usage: tac <file_name>\n")

    def touch(self, command):
        args = command.split()
        if len(args) == 2:
            file_name = args[1]
            try:
                self.vfs.create_or_update_file(file_name)
                self.output_callback(f"Touched file: {file_name}\n")
                self.log_action("touch", f"Touched file {file_name}")
            except Exception as e:
                self.output_callback(f"Error: {e}\n")
        else:
            self.output_callback("Usage: touch <file_name>\n")

    def log_action(self, command, result):
        log_entry = {
            "user": self.username,
            "command": command,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            with open(self.log_file_path, "a", newline="", encoding="utf-8") as log_file:
                writer = csv.DictWriter(log_file, fieldnames=["user", "command", "result", "timestamp"])
                if log_file.tell() == 0:
                    writer.writeheader()
                writer.writerow(log_entry)
        except Exception as e:
            self.output_callback(f"Error logging action: {e}\n")
