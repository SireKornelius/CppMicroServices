import re
import fnmatch
from timeit import default_timer
from shutil import copytree
from argparse import ArgumentParser
from glob import glob
from os.path import join, abspath, expanduser, expandvars, isdir

def parse_args(args):
    """Parse command line arguments.
    
        Parameters:
            args (sequence[str]): command line arguments
        Returns:
            (Namespace): Namespace object containing parsed arguments
    """
    parser = ArgumentParser(description='Copy and change cppmicroservices namespace into specified dir')
    
    parser.add_argument(
        'namespace', 
        metavar='NAMESPACE', 
        help='new namespace name'
        )
 
    parser.add_argument(
        'path_to', 
        metavar='PATH_TO', 
        help='path to directory to copy to'
        )
    
    parser.add_argument(
        '--previousNamespace', 
        '-pN', 
        metavar='pN', 
        help='the namespace to change (default=cppmicroservices)', default='cppmicroservices'
        )
    
    parser.add_argument(
        '--stats',
        '-st', 
        action='store_true', 
        help='print instances of namespace/namespace usage modified and runtime duration'
        )
    
    return parser.parse_args(args)


def progressbar(it, pre, size = 40): 
    """Generator function for displaying the script's progress in parsing files.
    """
    count = len(it)
    def show(j: int):
        x = int(size*j/count)
        print(f"{pre}[{'#'*x}{('.'*(size-x))}] {j}/{count}", end='\r', flush=True)
    show(0)
    for i in range(count):
        yield
        show(i+1)
    print("\n", flush=True)
    yield


#Hard code the things I want removed
def wrap_ignore_files(to_inspect, excluded_patterns):
    """Closure passed to shutil.copytree's ignore argument, returning a function which 
    takes in a directory name and list of files in that directory and returns a list 
    of files to ignore relative to that directory.

        Parameters:
            to_inspect(iterable): files to exclude from copy
            excluded_patterns(list[str]): patterns to exclude files

        Returns:
            ignore_files (function)
    """
    def ignore_files(dir, files):
        ignore = []
        for pattern in excluded_patterns:
            for file in files:
                if fnmatch.fnmatch(file, pattern):
                    #print(f"{dir} {file}")
                    ignore.append(file)
        for file in files:
            path = abspath(expanduser(expandvars(join(dir, file))))
            if path in to_inspect:
                ignore.append(file)
        return set(ignore)
    return ignore_files


def resolve_new_path(file_name, new_dir, dir):
    """ Finding new path for file in new dir.

        Parameters:
            file_name (str): absolute path to file
            new_dir (str): absolute path to new dir
            dir (str): absolute path to current dir
        Returns:
            (str): the absolute path to write to in new dir
    """
    suffix = file_name.removeprefix(dir)
    return f"{new_dir}{suffix}"


def check_valid_namespace(input):
    """ Validating user input is a valid c++ identifier (no support for non-english characters).

        Parameters:
            input (str): namespace name
        Returns:
            (bool): True if valid namespace name else return false
    """
    cpp_keywords = {
    'alignas', 'alignof', 'and', 'and_eq', 'asm', 'atomic_cancel', 'atomic_commit', 'atomic_noexce   pt',
    'auto', 'bitand', 'bitor', 'bool', 'break', 'case', 'catch', 'char', 'char8_t', 'char16_t', 'char32_t',
    'class', 'compl', 'concept', 'const', 'consteval', 'constexpr', 'constinit', 'const_cast', 'continue',
    'co_await', 'co_return', 'co_yield', 'decltype', 'default', 'delete', 'do', 'double', 'dynamic_cast',
    'else', 'enum', 'explicit', 'export', 'extern', 'false', 'float', 'for', 'friend', 'goto', 'if', 'inline',
    'int', 'long', 'mutable', 'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr', 'operator', 'or',
    'or_eq', 'private', 'protected', 'public', 'reflexpr', 'register', 'reinterpret_cast', 'requires', 'return',
    'short', 'signed', 'sizeof', 'static', 'static_assert', 'static_cast', 'struct', 'switch', 'synchronized',
    'template', 'this', 'thread_local', 'throw', 'true', 'try', 'typedef', 'typeid', 'typename', 'union',
    'unsigned', 'using', 'virtual', 'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq'
    }
    check = re.search(r'^[a-zA-Z_][a-zA-Z0-9_]*$', input) # dont need to support non-english
    return True if check and input not in cpp_keywords else False


class NamespaceModifier:
    """Class following https://en.cppreference.com/w/cpp/language/namespace to match usage of c++ namespaces by using regex.
    """
    def __init__(self, to_replace, replace_with):
        """ Initialize NamespaceModifier object

        Parameters:
            to_replace (str): namespace to be replaced
            replace_with (str): new namespace
        Returns:
            (None)
        """
        self.to_replace = to_replace
        self.replace_with = replace_with

    def reg_name_dec(self, string):
        """ From cppreferences, matching case (1), (2), (5), (/8), (/9)

        Parameters:
            string (str): input text for regex to match
        Returns:
            (str): new string with modifications (if any) made
        """
        fn = lambda matchobj : f"{matchobj.group(1)}{self.replace_with}{matchobj.group(5)}"
        return re.subn(rf'((^\s{{0}}|[^\w_])namespace(\s|")+?)({self.to_replace})([^\w_]|\s{{0}}$)', fn, string)

    def reg_alias_name(self, string):
        """ From cppreferences, matching case (7)

        Parameters:
            string (str): input text for regex to match
        Returns:
            (str): new string with modifications (if any) made
        """
        fn = lambda matchobj : f"{matchobj.group(1)}{self.replace_with}{matchobj.group(7)}"
        return re.subn(rf'((^\s{{0}}|[^\w_])namespace(\s|")+?[\w_]+?(\s|")+?=(\s|")+?)({self.to_replace})([^\w_]|\s{{0}}$)', fn, string)

    def reg_scope_post(self, string):
        """ From cppreferences, matching case (4), (6)

        Parameters:
            string (str): input text for regex to match
        Returns:
            (str): new string with modifications (if any) made
        """
        fn = lambda matchobj : f"{matchobj.group(1)}{self.replace_with}{matchobj.group(3)}{matchobj.group(5)}"
        return re.subn(rf'(^\s{{0}}|[^\w_])({self.to_replace})((\s|")*?)(::)', fn, string)

    def reg_scope_pre(self, string):
        """ From cppreferences, matching case (/8), (/9)

        Parameters:
            string (str): input text for regex to match
        Returns:
            (str): new string with modifications (if any) made
        """
        fn = lambda matchobj : f"{matchobj.group(1)}{matchobj.group(2)}{matchobj.group(4)}{self.replace_with}{matchobj.group(8)}"
        return re.subn(rf'(::)((\s|")*?)(inline(\s|")*?|(\s|")*?)({self.to_replace})([^\w_]|\s{{0}}$)', fn, string)


    def sub_regex(self, string):
        """ Check input text for current namespace usages and replace with new namespace 
        
        Parameters:
            string (str): input text to for regex expressions to match
        Returns:
            (tuple[str, int]): new string with modifications (if any) made + # of modifications
        """
        new_str = string + ""
        count = 0
        check = [self.reg_name_dec, self.reg_alias_name, self.reg_scope_post, self.reg_scope_pre]
        for func in check:
            temp_string, temp_count = func(new_str)
            new_str = temp_string
            count += temp_count

        return new_str, count
    
    def change_file_namespace(self, file_name, new_file_path):
        """ Search through file for regex patterns matching current namespace usage and replaces the current namespace 
        with a new namespace, writing to new_file_path.

        Parameters:
            file_name (str): absolute path to file to be read
            new_file_path (str): absolute path to where potentially modified contents are written
        Returns:
            (int): # of modifications made
        """
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()

        new_file_content, count = self.sub_regex(content)

        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(new_file_content)

        return count
    

class DirGenerator:
    """Class for making new dir with new namespace from current dir

    Attributes:
    new_namespace (str): new namespace
    old_namespace (str): namespace to change
    dir_to_copy (str): topmost dir to copy and modify namespace of specified subdirs
    folders (list[str]): list of absolute paths to folders to have namespace modified
    file_types_to_check (tuple[str,...]): file types to be checked in folder
    files_to_analyze (list[str]): absolute paths to files which will be updated to new_namespace usage
    ns_mod (NamespaceModifier): object to use to write to new dir with new namespace
    count: (dict[str, int]): dict of modifications made
    time: (dict[str, float]): dict of time taken to make new dir
    """
    def __init__(self, new_namespace, old_namespace, dir_to_copy, folders_to_analyze, file_types_to_check):
        """Initialize DirGenerator object
        
        Parameters:
            new_namespace (str): new namespace 
            old_namespace (str): namespace to modify
            dir_to_copy (str): topmost dir to copy and modify namespace of specified subdirs
            folders_to_analyze (list[str]): subdirs of dir_to_copy to have namespace modified
            file_types_to_check (tuple[str,...]): file types to be checked in folders_to_analyze
        Returns:
            (None)
        """
        if not check_valid_namespace(new_namespace):
            raise ValueError('Invalid namespace name chosen')
        if not isdir(dir_to_copy):
            raise OSError('Invalid directory')
        
        self.old_namespace = old_namespace
        self.new_namespace = new_namespace

        self.dir_to_copy = abspath(expanduser(expandvars(dir_to_copy)))
        self.folders = [abspath(expanduser(expandvars(join(self.dir_to_copy, directory)))) 
                        for directory in folders_to_analyze] 
        
        self.file_types_to_check = file_types_to_check
        self.files_to_analyze = self._find_files()
        self.ns_mod = NamespaceModifier(to_replace=old_namespace, replace_with=new_namespace)
        self.count = {}
        self.time = {}


    def create_modified_dir(self, new_dir, to_filter):
        """Copy dir_to_copy to new_dir with modified namespace 
        (ignoring files/folders with pattern in to_filter)    

        Parameters:
            new_dir (str): path to directory to copy current dir to with modified namespace
            to_filter (list[str]): patterns for files to avoid copy
        Returns:
            (None)  
        """
        new_dir = abspath(expanduser(expandvars(new_dir)))
        temp_time = default_timer()

        print('Copying..')

        copytree(
            self.dir_to_copy, 
            new_dir, 
            ignore=wrap_ignore_files(set(self.files_to_analyze), to_filter)
        )    

        count = 0

        gen = progressbar(range(len(self.files_to_analyze)), "Running: ")

        for file in self.files_to_analyze:

            new_path = resolve_new_path(file, new_dir, self.dir_to_copy)
            count += self.ns_mod.change_file_namespace(file, new_path)

            next(gen)
        next(gen)
        
        self.count[new_dir] = count
        self.time[new_dir] = default_timer() - temp_time

    def _find_files(self):
        """Find files with correct file types to analyze in given folders.
        """
        files = []
        for i in self.folders:
            if not isdir(i):
                raise OSError('Folder not found')
            for file in glob(f"{i}/**/*", recursive=True):
                if file.endswith(self.file_types_to_check):
                    files.append(file)
        return files