import unittest
import os 
from filecmp import cmp
from src.utils import change_file_namespace

#changeFileNamespace(file_name, new_dir, dir, to_replace, replace_with):
# Assuming all inputs are valid because they are validated beforehand
class TestFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files_to_remove = [ './test/resources/expected/cpp_basic.txt', './test/resources/expected/no_change.txt']

    @classmethod
    def tearDownClass(cls):
        for file in cls.files_to_remove:
            if (os.path.isfile(file)):
                os.remove(file)

    def test_no_filechanges(self):
        count = change_file_namespace(
            './test/resources/test/no_change.txt',
            './test/resources/expected', 
            './test/resources/test',
            'cppmicroservices', 
            'mw_cppms'
            )
        self.assertEqual(count, 0)
        self.assertTrue(cmp('./test/resources/expected/no_change.txt', './test/resources/expected/expected_no_change.txt'))

    def test_filechange_match(self):
        count = change_file_namespace(
            './test/resources/test/cpp_basic.txt',
            './test/resources/expected', 
            './test/resources/test',
            'cppmicroservices', 
            'mw_cppms'
            )

        self.assertEqual(count, 17)
        self.assertTrue(cmp('./test/resources/expected/cpp_basic.txt', './test/resources/expected/expected_cpp_basic.txt'))
        

if __name__ == '__main__':
    unittest.main()