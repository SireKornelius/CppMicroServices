import unittest
import os 
from os.path import abspath, expanduser, expandvars, isfile
from filecmp import cmp
from src.utils import NamespaceModifier, resolve_new_path

class TestFile(unittest.TestCase):
    """Test that file modification works as expected
    """

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
        """Testing file without references to cppmicroservices namespace should not have contents changed
        """
        file_name = abspath(expanduser(expandvars('./test/resources/test/no_change.txt')))
        new_path = resolve_new_path(file_name, self.new_dir, self.old_dir)
        count = self.ns_mod.change_file_namespace(
            file_name,
            new_path
            )
        self.assertEqual(count, 0)
        self.assertTrue(cmp('./test/resources/expected/no_change.txt', './test/resources/expected/expected_no_change.txt', shallow=False))

    def test_filechange_match(self):
        """Testing file with references to cppmicroservices namespace should have all refernces match new namespace
        """
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