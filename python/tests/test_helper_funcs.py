import unittest
from python.modules.helper_funcs import *


class TestHelperFuncs(unittest.TestCase):
    def test_save_to_json(self):
        test_file = File('/path/to/file', 'filetype')
        save_to_json([test_file], 'test.json')
        loaded = load_json('test.json')
        print(loaded)
        test_str = {'/path/to/file': {'original_path': '/path/to/file', 'new_path': '', 'filetype': 'filetype',
                                      'size': '', 'creation_time': '', 'modification_time': '', 'last_access_time': ''}}

        self.assertEqual(loaded, test_str)


if __name__ == '__main__':
    unittest.main()
