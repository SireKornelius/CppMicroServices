import unittest, sys
from shutil import copyfile
from filecmp import cmp
from os.path import dirname, abspath, join
import subprocess
sys.path.append(abspath(join('..', 'src')))
from script import changeFileNamespace

#@unittest.skipIf(True if subprocess.run(['ls'], capture_output=True).returncode != 0 else False, "subprocess issue") #again a a design thing
class TestFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.python_interp = sys.executable
        parent_dir = dirname(dirname(abspath(__file__)))
        print(parent_dir)
        cls.path_to_script = join(parent_dir, 'src', 'script.py')
        #cls.path_to_test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'expected', 'exp'

    def test_bad_user_input(self): # A little sussy
        res = subprocess.run([self.python_interp, self.path_to_script], capture_output=True)
        self.assertNotEqual(res.returncode, 0)
    
    def testInvalidNamespaceName(self):
        pass



if __name__ == '__main__':
    unittest.main()