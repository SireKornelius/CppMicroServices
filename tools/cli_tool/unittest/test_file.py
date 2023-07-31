import unittest, sys
from shutil import copyfile
from filecmp import cmp
import os 
sys.path.append(os.path.abspath(os.path.join('..', 'src')))
from script import changeFileNamespace

#changeFileNamespace(file_name, new_dir, dir, to_replace, replace_with):
# Assuming all inputs are valid because they are validated beforehand
class TestFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.files_to_remove = [ './resources/expected/cpp_basic.txt', './resources/expected/no_change.txt']

    @classmethod
    def tearDownClass(cls) -> None:
        for file in cls.files_to_remove:
            os.remove(file)
    
    # not possible b/c check before hand
    #def test_filenotfound(self):
    #    with self.assertRaises(OSError):
    #        changeFileNamespace('./nonexistent_file', 'cppmicroservices', 'mw_cppms')

    def test_no_filechanges(self):
        #copyfile('./resources/test/no_change.txt', './resources/test/modified_no_change.txt')
        count = changeFileNamespace('./resources/test/no_change.txt',
                                    './resources/expected', './resources/test','cppmicroservices', 'mw_cppms')
        self.assertEqual(count, 0)
        self.assertTrue(cmp('./resources/expected/no_change.txt', './resources/expected/expected_no_change.txt'), msg='File not equal expected output')

    def test_filechange_match(self):
        #copyfile('./resources/test/cpp_basic.txt', './resources/test/modified_cpp_basic.txt')

        count = changeFileNamespace('./resources/test/cpp_basic.txt',
                                    './resources/expected', './resources/test','cppmicroservices', 'mw_cppms')

        self.assertEqual(count, 17)
        self.assertTrue(cmp('./resources/expected/cpp_basic.txt', './resources/expected/expected_cpp_basic.txt'), msg='File not equal expected output')
        # Have some more complex changes
        

if __name__ == '__main__':
    unittest.main()