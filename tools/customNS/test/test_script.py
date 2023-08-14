import unittest
import filecmp
from shutil import rmtree
from os.path import dirname, abspath, join, isdir, expanduser, expandvars
from src.utils import DirGenerator, parse_args

# Need to fix because have altered behavior of script.. (maybe mock? idk)

class TestFile(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        dirs_to_remove = ['./test/resources/expected/test_dir', './test/resources/expected/test_dir_change']
        for directory in dirs_to_remove:
            if (isdir(directory)):
                rmtree(directory)
        filecmp.clear_cache()

    def test_bad_user_input(self):
        with self.assertRaises(SystemExit) as e:
            parse_args(['-lw', '-m'])

        with self.assertRaises(SystemExit) as e:
            parse_args(['mw_cppms'])

        with self.assertRaises(SystemExit) as e:
            parse_args(['../folder'])

        with self.assertRaises(SystemExit) as e:
            parse_args(['mw_cppms', 'some_folder', 'st'])

        with self.assertRaises(SystemExit) as e:
            parse_args(['mw_cppms', 'some_folder', '-nothing'])
        

    def test_good_user_input(self):

        parser = parse_args(['mw_cppms', '../new_folder'])
        self.assertEqual('mw_cppms', parser.namespace)
        self.assertEqual('../new_folder', parser.path_to)

        parser = parse_args(['mw_cppms', '../new_folder', '-st', '-pN=something'])
        self.assertEqual('mw_cppms', parser.namespace)
        self.assertEqual('../new_folder', parser.path_to)
        self.assertEqual('something', parser.previousNamespace)
        self.assertTrue(parser.stats)
        # spaces are handled before hand so no need test  
    

    
    def test_invalid_namespace_name(self):
        valid_dir_to_copy = abspath(expanduser(expandvars(join(dirname(__file__), 'resources/test/test_dir'))))
        valid_folders = ['.'] 
        with self.assertRaises(ValueError) as e:
            dgen = DirGenerator(
                new_namespace='mw@cppms',
                old_namespace='to_replace',
                dir_to_copy=valid_dir_to_copy,
                folders_to_analyze=valid_folders,
                file_types_to_check=('.cpp')
            )
        with self.assertRaises(ValueError) as e:
            dgen = DirGenerator(
                new_namespace='123mw_cppms',
                old_namespace='to_replace',
                dir_to_copy=valid_dir_to_copy,
                folders_to_analyze=valid_folders,
                file_types_to_check=('.cpp')
            )
    
    def test_invalid_user_input(self):
        valid_dir_to_copy = abspath(expanduser(expandvars(join(dirname(__file__), 'resources/test/test_dir'))))
        valid_folders = ['.'] 
        with self.assertRaises(OSError) as e:
            dgen = DirGenerator(
                new_namespace='mw_cppms',
                old_namespace='to_replace',
                dir_to_copy='invalid_dir',
                folders_to_analyze=valid_folders,
                file_types_to_check=('.cpp')
            )
        with self.assertRaises(OSError) as e:
            dgen = DirGenerator(
                new_namespace='mw_cppms',
                old_namespace='to_replace',
                dir_to_copy=valid_dir_to_copy,
                folders_to_analyze=['nonexistent_folder'],
                file_types_to_check=('.cpp')
            )

    def test_valid_no_change(self):
        valid_dir_to_copy = abspath(expanduser(expandvars(join(dirname(__file__), 'resources/test/test_dir'))))
        valid_folders = ['.'] 
        dgen = DirGenerator(
            new_namespace='mw_cppms',
            old_namespace='cppmicroservices',
            dir_to_copy=valid_dir_to_copy,
            folders_to_analyze=valid_folders,
            file_types_to_check=('.cpp')
        )
        dgen.create_modified_dir('./test/resources/expected/test_dir', [])
        comp = filecmp.dircmp('./test/resources/expected/expected_test_dir', './test/resources/expected/test_dir')
        self.assertEqual(len(comp.diff_files), 0)
        compf = filecmp.cmpfiles(
            a='./test/resources/expected/expected_test_dir', 
            b='./test/resources/expected/test_dir',
            common=['something.cpp'],
            shallow=False
            )
        self.assertEqual(compf[0], ['something.cpp'])
        self.assertEqual(compf[1], [])
        self.assertEqual(compf[2], [])
    
    def test_valid_change(self):
        valid_dir_to_copy = abspath(expanduser(expandvars(join(dirname(__file__), 'resources/test/test_dir_change'))))
        valid_folders = ['.']  
        dgen = DirGenerator(
            new_namespace='mw_cppms',
            old_namespace='cppmicroservices',
            dir_to_copy=valid_dir_to_copy,
            folders_to_analyze=valid_folders,
            file_types_to_check=('.cpp', '.json')
        )
        dgen.create_modified_dir('./test/resources/expected/test_dir_change', ['.txt'])
        comp = filecmp.dircmp('./test/resources/expected/expected_test_dir_change', './test/resources/expected/test_dir_change')
        self.assertEqual(len(comp.diff_files), 0)

        compf = filecmp.cmpfiles(
            a='./test/resources/expected/expected_test_dir_change/ignore', 
            b='./test/resources/expected/test_dir_change/ignore',
            common=['no_change.cpp'],
            shallow=False
            )
        self.assertEqual(compf[0], [])
        self.assertEqual(compf[1], ['no_change.cpp'])
        self.assertEqual(compf[2], [])

        compf = filecmp.cmpfiles(
            a='./test/resources/expected/expected_test_dir_change/inner', 
            b='./test/resources/expected/test_dir_change/inner',
            common=['inner.cpp', 'ignore.txt'],
            shallow=False
            )
        self.assertEqual(compf[0], ['inner.cpp'])
        self.assertEqual(compf[1], [])
        self.assertEqual(compf[2], ['ignore.txt'])

        compf = filecmp.cmpfiles(
            a='./test/resources/expected/expected_test_dir_change/inner2', 
            b='./test/resources/expected/test_dir_change/inner2',
            common=['t.json', 'test.cpp'],
            shallow=False
            )
        self.assertEqual(set(compf[0]), set(['test.cpp', 't.json']))
        self.assertEqual(compf[1], [])
        self.assertEqual(compf[2], [])


if __name__ == '__main__':
    unittest.main()