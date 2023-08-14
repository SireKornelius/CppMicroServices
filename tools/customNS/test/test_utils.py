import unittest
import glob
from os import listdir
from os.path import abspath, expanduser, expandvars, dirname, join, basename
from filecmp import cmp
from src.utils import resolve_new_path, check_valid_namespace, wrap_ignore_files

class TestFile(unittest.TestCase): 
    def test_resolve_new_path(self):
        file = abspath(expanduser(expandvars(dirname(__file__))))
        file = abspath(expanduser(expandvars(join(file, 'resources/test/test_dir_change/inner/inner.cpp'))))

        dir = abspath(expanduser(expandvars(dirname(__file__))))
        dir = abspath(expanduser(expandvars(join(dir, 'resources/test/test_dir_change'))))

        new_dir = abspath(expanduser(expandvars(dirname(__file__))))
        new_dir = abspath(expanduser(expandvars(join(new_dir, 'resources/expected/test_dir_change'))))
        new_path = resolve_new_path(file, new_dir, dir)

        self.assertEqual(basename(dirname(new_path)), 'inner')
        self.assertEqual(basename(dirname(dirname(new_path))), 'test_dir_change')
        self.assertEqual(basename(dirname(dirname(dirname(new_path)))), 'expected')
        
    def test_valid_namespace(self):
        self.assertTrue(check_valid_namespace('mw_cppms'))
        self.assertTrue(check_valid_namespace('mwcppms'))
        self.assertTrue(check_valid_namespace('abcd'))
        self.assertTrue(check_valid_namespace('random_xyz_1235'))

    def test_invalid_namespace(self):
        self.assertFalse(check_valid_namespace('1234asd'))
        self.assertFalse(check_valid_namespace('random xyz_1235'))
        self.assertFalse=(check_valid_namespace('你好')) # Although valid c++ namespace, this tool does not support non-english identifiers

    def test_wrap_ignore_files(self):
        dir = abspath(expanduser(expandvars(dirname(__file__))))
        dir = abspath(expanduser(expandvars(join(dir, 'resources/test/test_dir_change'))))

        files = listdir(dir)
        ignore = {f"{abspath(expanduser(expandvars(join(dir, 'ignore'))))}"}
        ignore_files = wrap_ignore_files(ignore, [])

        self.assertEqual(ignore_files(dir, files), {'ignore'})

        dir = abspath(expanduser(expandvars(join(dir, 'ignore'))))
        files = listdir(dir)
        ignore = set()
        ignore_files = wrap_ignore_files(ignore, ['*.cpp'])
        self.assertEqual(ignore_files(dir, files), {'no_change.cpp'})

if __name__ == '__main__':
    unittest.main()