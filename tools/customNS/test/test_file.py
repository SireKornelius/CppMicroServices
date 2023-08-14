import unittest
import os 
from os.path import join, abspath, expanduser, expandvars, isfile
from filecmp import cmp
from src.utils import NamespaceModifier, resolve_new_path

#Assuming all inputs are valid because they are validated beforehand
class TestFile(unittest.TestCase):

    def setUp(self):
        self.ns_mod = NamespaceModifier('cppmicroservices', 'mw_cppms')
        self.old_dir = abspath(expanduser(expandvars('./test/resources/test')))
        self.new_dir = abspath(expanduser(expandvars('./test/resources/expected')))

    @classmethod
    def tearDownClass(cls):
        files_to_remove = [ './test/resources/expected/cpp_basic.txt', './test/resources/expected/no_change.txt']
        for file in files_to_remove:
            if (isfile(file)):
                os.remove(file)

    def test_no_filechanges(self):
        file_name = abspath(expanduser(expandvars('./test/resources/test/no_change.txt')))
        new_path = resolve_new_path(file_name, self.new_dir, self.old_dir)
        count = self.ns_mod.change_file_namespace(
            file_name,
            new_path
            )
        self.assertEqual(count, 0)
        self.assertTrue(cmp('./test/resources/expected/no_change.txt', './test/resources/expected/expected_no_change.txt', shallow=False))

    def test_filechange_match(self):
        file_name = abspath(expanduser(expandvars('./test/resources/test/cpp_basic.txt')))
        new_path = resolve_new_path(file_name, self.new_dir, self.old_dir)
        count = self.ns_mod.change_file_namespace(
            file_name,
            new_path
            )

        self.assertEqual(count, 17)
        self.assertTrue(cmp('./test/resources/expected/cpp_basic.txt', './test/resources/expected/expected_cpp_basic.txt', shallow=False))
        

if __name__ == '__main__':
    unittest.main()