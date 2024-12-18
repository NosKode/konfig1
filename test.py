import os
import unittest
from unittest.mock import Mock, patch
from command_handler import CommandHandler
from virtual_file_system import VirtualFileSystem, FileNotFoundException


class TestCommandHandler(unittest.TestCase):

    def setUp(self):
        self.vfs = Mock(spec=VirtualFileSystem)
        self.output = Mock()
        self.handler = CommandHandler(
            vfs=self.vfs,
            log_file_path="test_log.csv",
            username="test_user",
            output_callback=self.output
        )

    def test_list_directory(self):
        self.vfs.list_directory.return_value = "Directory Contents"
        self.handler.execute_command("ls")
        self.output.assert_called_with("Directory Contents")

    def test_change_directory_success(self):
        self.handler.execute_command("cd ./valid_folder")
        self.vfs.change_directory.assert_called_with("./valid_folder")

    def test_change_directory_failure(self):
        self.vfs.change_directory.side_effect = FileNotFoundException("Error")
        self.handler.execute_command("cd ./invalid_folder")
        self.output.assert_called_with("Error: Error\n")

    def test_tac_success(self):
        self.vfs.read_file.return_value = "line1\nline2\nline3"
        self.handler.execute_command("tac ./valid_folder/test.txt")
        self.output.assert_called_with("line3\nline2\nline1")

    def test_tac_file_not_found(self):
        self.vfs.read_file.side_effect = FileNotFoundException("Error")
        self.handler.execute_command("tac ./invalid_folder/missing.txt")
        self.output.assert_called_with("Error: Error\n")

    def test_touch_file(self):
        self.handler.execute_command("touch ./valid_folder/newfile.txt")
        self.vfs.create_or_update_file.assert_called_with("./valid_folder/newfile.txt")
        self.output.assert_called_with("Touched file: ./valid_folder/newfile.txt\n")


class TestVirtualFileSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_tar_path = "C:\\Users\\misha\\Desktop\\конфиг\\test.tar"
        cls.vfs = VirtualFileSystem(cls.test_tar_path)

    def test_list_directory(self):
        contents = self.vfs.list_directory()
        self.assertIsInstance(contents, str)

    def test_change_directory_valid(self):
        # Изменить путь, чтобы он соответствовал архиву
        self.vfs.change_directory("./valid_folder")
        self.assertTrue(self.vfs.current_path.endswith("./valid_folder"))

    def test_change_directory_invalid(self):
        with self.assertRaises(FileNotFoundException):
            self.vfs.change_directory("./invalid_folder")

    def test_read_file(self):
        # Изменить путь, чтобы он соответствовал архиву
        content = self.vfs.read_file("./valid_folder/test.txt")
        self.assertIsInstance(content, str)

    def test_create_or_update_file(self):
        # Изменить путь, чтобы он соответствовал архиву
        file_path = os.path.join(self.vfs.current_path, "./valid_folder/newfile.txt")
        self.vfs.create_or_update_file("./valid_folder/newfile.txt")
        self.assertTrue(os.path.exists(file_path))


if __name__ == "__main__":
    unittest.main()
