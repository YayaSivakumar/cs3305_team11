import sys
import os
import unittest
from modules.organise_by_type import *

# Add the parent directory to sys.path in order to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class TestOrganiseByType(unittest.TestCase):
    """
    test class for the organise_by_type modules which have return values
    """

    # test each file type for correct category assignment
    def test_document_file_type(self):
        result = determine_filetype('blah.pdf')
        self.assertEqual(result, 'documents')
    
    def test_photo_file_type(self):
        result = determine_filetype('blah.jpeg')
        self.assertEqual(result, 'photos')

    def test_video_file_type(self):
        result = determine_filetype('blah.mp4')
        self.assertEqual(result, 'videos')
    
    def test_music_file_type(self):
        result = determine_filetype('blah.wav')
        self.assertEqual(result, 'music')
    
    def test_misc_file_type(self):
        result = determine_filetype('blah.js')
        self.assertEqual(result, 'misc')
    
    # test special cases for correct category assignment
    def test_no_extension_file_type(self):
        result = determine_filetype('blah')
        self.assertEqual(result, 'misc')
    
    def test_empty_filename_file_type(self):
        result = determine_filetype('')
        self.assertEqual(result, 'misc')
    
    def test_dot_in_filename_file_type(self):
        result = determine_filetype('blah.blah.pdf')
        self.assertEqual(result, 'documents')

    def test_get_file_paths_valid_directory(self):
        # test that the function returns a list 
        result = get_all_file_paths(os.getcwd()+'/Tester')
        self.assertIsInstance(result, list)

        # test that the list contains only strings and that each path exists
        for i in result:
            self.assertIsInstance(i, str)
            self.assertTrue(os.path.exists(i))

        # test that the list contains the correct number of files
        self.assertEqual(len(result), 16)

    def test_get_file_paths_invalid_directory(self):
        # test that given a non existant folder, an empty list is returned
        result = get_all_file_paths('/doesnotexist')
        self.assertIsInstance(result, list)

        # test that the resulting list contains no files
        self.assertEqual(len(result), 0)

# run tests
if __name__ == "__main__":
    unittest.main()