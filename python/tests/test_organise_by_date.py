import sys
import os
import unittest

# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from python.modules.organise_by_date import *

class TestOrganiseByDate(unittest.TestCase):

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
    
    def test_time_convert(self):
        pass

    def test_get_metadata_from_files(self):
        pass

    def test_organise_by_date(self):
        pass

if __name__ == '__main__':
    unittest.main()