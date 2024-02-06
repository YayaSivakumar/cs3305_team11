import unittest
from python.modules.helper_funcs import *


class TestHelperFuncs(unittest.TestCase):

    def test_get_all_file_paths(self):
        pass

    def test_get_file_and_subdir_paths(self):
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

    def test_create_list_of_file_obj(self):
        # file in dictionary
        test_dict = {
            '/path/to/file': {'original_path': '/path/to/file', 'current_path': '/path/to/file', 'filetype': 'filetype',
                              'size': '1.0 KB', 'creation_time': '2018-04-11 21:57:52',
                              'modification_time': '2018-04-11 21:57:52', 'last_access_time': '2018-04-11 21:57:52'}}

        test_output = {'original_path': '/path/to/file', 'current_path': '/path/to/file', 'filetype': 'filetype',
                       'size': '1.0 KB', 'creation_time': '2018-04-11 21:57:52',
                       'modification_time': '2018-04-11 21:57:52', 'last_access_time': '2018-04-11 21:57:52'}

        # create file object from dictionaries
        file_obj_in_list = create_list_of_file_obj(test_dict)
        # change file object back to dictionary
        list_to_dict = file_obj_in_list[0].to_dict()

        # test if dictionaries are equal
        self.assertEqual(test_output, list_to_dict)

    def test_move_file(self):
        pass

    def test_save_to_json(self):
        pass

    def test_load_json(self):
        pass

    def test_remove_empty_directories(self):
        def test_remove_empty_directories(self):
            # Create a temporary directory for testing
            test_dir = '/path/to/test_dir'
            os.makedirs(os.path.join(test_dir, 'non_empty_dir'))
            os.makedirs(os.path.join(test_dir, 'empty_dir'))

            # Create a dummy file in 'non_empty_dir'
            with open(os.path.join(test_dir, 'non_empty_dir', 'dummy_file.txt'), 'w') as f:
                f.write("This is a dummy file.")

            try:
                # Call the function
                delete_empty_directories(test_dir)

                # Assert function is behaving correctly
                self.assertTrue(os.path.exists(os.path.join(test_dir, 'non_empty_dir')))
                self.assertTrue(os.path.exists(os.path.join(test_dir, 'non_empty_dir', 'dummy_file.txt')))
                self.assertFalse(os.path.exists(os.path.join(test_dir, 'empty_dir')))
            finally:
                # Delete the temporary test directory and its contents
                shutil.rmtree(test_dir)


if __name__ == '__main__':
    unittest.main()
