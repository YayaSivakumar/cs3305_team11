import unittest
from python.modules.helper_funcs import *


class TestHelperFuncs(unittest.TestCase):

    def test_get_all_file_paths(self):
        pass

    def test_get_file_and_dir_paths(self):
        pass

    def test_save_to_json(self):
        test_file = File('/path/to/file', 'filetype')
        save_to_json([test_file], 'test.json')
        loaded = load_json('test.json')
        test_str = {'/path/to/file': {'original_path': '/path/to/file', 'current_path': '', 'filetype': 'filetype',
                                      'size': '', 'creation_time': '', 'modification_time': '', 'last_access_time': ''}}

        self.assertEqual(loaded, test_str)

    def test_size_convert_int(self):
        # test for input as int
        self.assertEqual(size_convert(1000), '1.0 KB')
        self.assertEqual(size_convert(1000000), '1000.0 KB')
        self.assertEqual(size_convert(1000000000), '1000000.0 KB')

    def test_size_convert_float(self):
        # test for input as float
        self.assertEqual(size_convert(1000.0), '1.0 KB')
        self.assertEqual(size_convert(1000000.5), '1000.0 KB')

    def test_size_convert_string(self):
        # test for input as string
        self.assertRaises(TypeError, size_convert, '1000')

    def test_time_convert_int(self):
        self.assertEqual(time_convert(1523480272), '2018-04-11 21:57:52')

    def test_time_convert_float(self):
        self.assertEqual(time_convert(1523480272.1), '2018-04-11 21:57:52')

    def test_time_convert_string(self):
        self.assertRaises(TypeError, time_convert, '1523480272')
    
    def test_list_of_file_obj(self):
        # file in dictionary
        test_dict = {'/path/to/file': {'original_path': '/path/to/file', 'current_path': '/path/to/file', 'filetype': 'filetype',
                                      'size': '1.0 KB', 'creation_time': '2018-04-11 21:57:52', 'modification_time': '2018-04-11 21:57:52', 'last_access_time': '2018-04-11 21:57:52'}}

        test_output = {'original_path': '/path/to/file', 'current_path': '/path/to/file', 'filetype': 'filetype',
                                      'size': '1.0 KB', 'creation_time': '2018-04-11 21:57:52', 'modification_time': '2018-04-11 21:57:52', 'last_access_time': '2018-04-11 21:57:52'}

        # create file object from dictionaries
        file_obj_in_list = create_list_of_file_obj(test_dict)
        # change file object back to dictionary
        list_to_dict = file_obj_in_list[0].to_dict()

        # test if dictionaries are equal
        self.assertEqual(test_output, list_to_dict)

if __name__ == '__main__':
    unittest.main()
