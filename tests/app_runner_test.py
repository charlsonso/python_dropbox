import unittest
from python_dropbox.app.credential_checker import get_service
from python_dropbox.app.app_runner import overwrite_db, append_to_db, get_modified_files, update_drive_files, download_drive_files
import os
from unittest.mock import patch

def create_db_file():
    db_path = "hi.txt"
    with open(db_path, 'w+') as f:
        f.write('hi')
    return db_path

class TestMethods(unittest.TestCase):
    def test_overwrite_db(self):
        db_path = create_db_file()
        list_of_files = ['abc']
        overwrite_db(db_path, list_of_files)
        with open(db_path, 'r') as f:
            j = f.readline()
            self.assertTrue(j, list_of_files[0])
        os.remove(db_path)

    def test_append_to_db(self):
        db_path = create_db_file()
        append_to_db(db_path, 'abc')
        with open(db_path) as f:
            lines = f.readlines()
        self.assertTrue(['hi.txt', 'abc'], lines)
        os.remove(db_path)
        create_db_file()

    def test_get_modified_files(self):
        db_path = create_db_file()
        google_item_dict = [{'name': 'hi.txt', 'modifiedTime': '2025-03-01T00:00:00Z'}]
        target_folder = '.'
        files_to_compare_time = ['hi.txt']
        self.assertTrue(('hi.txt', 1), get_modified_files(files_to_compare_time, google_item_dict, target_folder))
        os.remove(db_path)

if __name__ == '__main__':
    unittest.main()
