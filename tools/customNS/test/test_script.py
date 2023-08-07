import unittest
import subprocess
from sys import executable
from filecmp import dircmp
from shutil import rmtree
from os.path import dirname, abspath, join, isdir

class TestFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.python_interp = executable
        parent_dir = dirname(dirname(abspath(__file__)))
        cls.path_to_script = join(parent_dir, 'src', 'script.py')
        cls.dirs_to_remove = ['./test/resources/expected/test_dir']
        
    @classmethod
    def tearDownClass(cls):
        for directory in cls.dirs_to_remove:
            if (isdir(directory)):
                rmtree(directory)

        # return codes: 0 = good, 1 = generic error, 2 = misuse of command line arguments 
    def test_bad_user_input(self):
        res = subprocess.run([self.python_interp, self.path_to_script], capture_output=True)
        self.assertEqual(res.returncode, 2)

        res = subprocess.run([self.python_interp, self.path_to_script, '-st', '-sp'], capture_output=True)
        self.assertEqual(res.returncode, 2)

        #can use these paths as test will always be run from same place
        res = subprocess.run(
            [
            self.python_interp, 
            self.path_to_script, 
            'mw_cppms', 
            './test/resources/test/test_dirInvalid', 
            './test/resources/expected'
            ], 
            capture_output=True
            )
        self.assertEqual(res.returncode, 1)
    
    def test_invalid_namespace_name(self):
        res = subprocess.run(
            [
            self.python_interp, 
            self.path_to_script, 
            '12mw_cppms', 
            './test/resources/test/test_dir', 
            './test/resources/expected/test_dir'
            ], 
            capture_output=True
            )
        self.assertEqual(res.returncode, 1)

        res = subprocess.run(
            [
            self.python_interp, 
            self.path_to_script, 
            'mw@cppms', 
            './test/resources/test/test_dir', 
            './test/resources/expected/test_dir'
            ], 
            capture_output=True
            )
        self.assertEqual(res.returncode, 1)
    
    def test_valid(self):
        res = subprocess.run(
            [
            self.python_interp,
            self.path_to_script, 
            'mw_cppms', 
            './test/resources/test/test_dir', 
            './test/resources/expected/test_dir'
            ], 
            capture_output=True
            )
        self.assertEqual(res.returncode, 0)

        comp = dircmp('./test/resources/expected/expected_test_dir', './test/resources/expected/test_dir')
        self.assertEqual(len(comp.diff_files), 0)

        res = subprocess.run(
            [
            self.python_interp, 
            self.path_to_script, 
            'mw_cppms', 
            './test/resources/test/test_dir',
            './test/resources/expected/test_dir', 
            '-sp', 
            '-st'
            ], 
            capture_output=True
            )
        self.assertEqual(res.returncode, 0)

        comp = dircmp('./test/resources/expected/expected_test_dir', './test/resources/expected/test_dir')
        self.assertEqual(len(comp.diff_files), 0)



if __name__ == '__main__':
    unittest.main()