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
    parser = ArgumentParser(description='Copy and change cppmicroservices namespace into specified dir.')
    
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
    def show(j):
        x = int(size*j/count)
        print(f"{pre}[{'#'*x}{('.'*(size-x))}] {j}/{count}", end='\r', flush=True)
    show(0)
    for i in range(count):
        yield
        show(i+1)
    print("\n", flush=True)
    yield


def wrap_ignore_files(to_inspect, excluded_patterns, files_to_not_pattern_match):
    """Closure passed to shutil.copytree's ignore argument, returning a function which 
    takes in a directory name and list of files in that directory and returns a list 
    of files to ignore relative to that directory.

        Parameters:
            to_inspect(iterable[str]): files to exclude from copy
            excluded_patterns(iterable[str]): patterns to exclude files, unix style wildcards supported
            files_to_not_pattern_match(iterable[str]): exceptions to excluded_patterns, unix style wildcards supported
        Returns:
            ignore_files (function)
    """
    def should_not_match(path, file):
        for exclusion in files_to_not_pattern_match:
            if fnmatch.fnmatch(path, exclusion) or fnmatch.fnmatch(file, exclusion):
                return True
        return False
    
    def ignore_files(dir, files):
        ignore = []
        for pattern in excluded_patterns:
            for file in files:
                if fnmatch.fnmatch(file, pattern):
                    path = abspath(expanduser(expandvars(join(dir, file))))
                    if should_not_match(path, file): # Some directories / files should not be touched
                        continue
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
    'alignas', 'alignof', 'and', 'and_eq', 'asm', 'atomic_cancel', 'atomic_commit', 'atomic_noexcept',
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
        Note that some regex expressions will overlap / multiple regexes would be able to detect certain namespace usage which is intended.

        All usages of namespaces according to cppreferences:

        namespace ns-name { declarations }	(1)	

        inline namespace ns-name { declarations }	(2)	(since C++11)

        namespace { declarations }	(3)

        ns-name :: member-name	(4)	

        using namespace ns-name ;	(5)	

        using ns-name :: member-name ;	(6)	

        namespace name = qualified-namespace ;	(7)	

        namespace ns-name :: member-name { declarations }	(8)	(since C++17)

        namespace ns-name :: inline member-name { declarations }	(9)	(since C++20)
    """
    def __init__(self, old_namespace, new_namespace):
        """ Initialize NamespaceModifier object. Compile regex expressions.

        Parameters:
            old_namespace (str): namespace to be replaced
            new_namespace (str): new namespace
        Returns:
            (None)
        """
        if not check_valid_namespace(new_namespace):
            raise ValueError('Invalid namespace name chosen')
        self.old_namespace = old_namespace
        self.new_namespace = new_namespace

        self.reg_ns_dec = re.compile(rf'((^\s{{0}}|[^\w_])namespace(\s|")+?)({self.old_namespace})([^\w_]|\s{{0}}$)')
        self.reg_ns_dec_repl = lambda matchobj : f"{matchobj.group(1)}{self.new_namespace}{matchobj.group(5)}"

        self.reg_ns_alias = re.compile(rf'((^\s{{0}}|[^\w_])namespace(\s|")+?[\w_]+?(\s|")+?=(\s|")+?)({self.old_namespace})([^\w_]|\s{{0}}$)')
        self.reg_ns_alias_repl = lambda matchobj : f"{matchobj.group(1)}{self.new_namespace}{matchobj.group(7)}"

        self.reg_post_ns = re.compile(rf'(^\s{{0}}|[^\w_])({self.old_namespace})((\s|")*?)(::)')
        self.reg_post_ns_repl = lambda matchobj : f"{matchobj.group(1)}{self.new_namespace}{matchobj.group(3)}{matchobj.group(5)}"

        self.reg_pre_ns = re.compile(rf'(::)((\s|")*?)(inline(\s|")*?|(\s|")*?)({self.old_namespace})([^\w_]|\s{{0}}$)')
        self.reg_pre_ns_repl = lambda matchobj : f"{matchobj.group(1)}{matchobj.group(2)}{matchobj.group(4)}{self.new_namespace}{matchobj.group(8)}" 

    def replace_namespace_declaration(self, string):
        """ From cppreferences, matching case (1), (2), (5), (/8), (/9)

        Parameters:
            string (str): input text for regex to match
        Returns:
            (str): new string with modifications (if any) made
        """
        return self.reg_ns_dec.subn(self.reg_ns_dec_repl, string)

    def replace_namespace_alias(self, string):
        """ From cppreferences, matching case (7)

        Parameters:
            string (str): input text for regex to match
        Returns:
            (str): new string with modifications (if any) made
        """
        return self.reg_ns_alias.subn(self.reg_ns_alias_repl, string)

    def replace_post_namespace_resolution(self, string):
        """ From cppreferences, matching case (4), (6)

        Parameters:
            string (str): input text for regex to match
        Returns:
            (str): new string with modifications (if any) made
        """
        return self.reg_post_ns.subn(self.reg_post_ns_repl, string)

    def replace_pre_namespace_resolution(self, string):
        """ From cppreferences, matching case (/8), (/9)

        Parameters:
            string (str): input text for regex to match
        Returns:
            (str): new string with modifications (if any) made
        """
        return self.reg_pre_ns.subn(self.reg_pre_ns_repl, string)


    def sub_regex(self, string):
        """ Check input text for current namespace usages and replace with new namespace 
        
        Parameters:
            string (str): input text to for regex expressions to match
        Returns:
            (tuple[str, int]): new string with modifications (if any) made + # of modifications
        """
        new_str = string[:]
        count = 0
        check = [self.replace_namespace_declaration, self.replace_namespace_alias, 
                 self.replace_post_namespace_resolution, self.replace_pre_namespace_resolution]
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
        dir_to_copy (str): topmost dir to copy and modify namespace of specified subdirs
        folders (iterable[str]): absolute paths to folders to have namespace modified
        file_types_to_check (iterable[str]): file types to be checked in folder
        files_to_analyze (iterable[str]): absolute paths to files which will be updated to new_namespace usage
        count: (dict[str, int]): dict of # modifications made
        time: (dict[str, float]): dict of time taken to make new dir
    """
    def __init__(self, dir_to_copy, folders_to_analyze, file_types_to_check):
        """Initialize DirGenerator object
        
        Parameters:
            dir_to_copy (str): topmost dir to copy and modify namespace of specified subdirs
            folders_to_analyze (iterable[str]): subdirs of dir_to_copy to have namespace modified
            file_types_to_check (iterable[str]): file types to be checked in folders_to_analyze
        Returns:
            (None)
        """
        if not isdir(dir_to_copy):
            raise OSError('Invalid directory')

        self.dir_to_copy = abspath(expanduser(expandvars(dir_to_copy)))
        self.folders = [abspath(expanduser(expandvars(join(self.dir_to_copy, directory)))) 
                        for directory in folders_to_analyze] 
        
        self.file_types_to_check = file_types_to_check
        self.files_to_analyze = self._find_files_to_analyze()
        self.count = {}
        self.time = {}


    def create_modified_dir(self, new_dir, to_filter, files_to_not_apply_filter, namespace_modifier):
        """Copy dir_to_copy to new_dir with modified namespace 
        (ignoring files/folders with pattern in to_filter)    

        Parameters:
            new_dir (str): path to directory to copy current dir to with modified namespace
            to_filter (iterable[str]): patterns for files to avoid copy, unix style wildcards supported
            files_to_not_apply_filter (iterable[str]): files of exceptions to to_filter, unix style wildcards supported
            namespace_modifier (NamespaceModifier): NamespaceModifier object used to modify namespace of file

        Returns:
            (None)  
        """
        new_dir = abspath(expanduser(expandvars(new_dir)))
        temp_time = default_timer()

        print('Copying..')

        # copy all files from current directory to new directory except 
        # those we will analyze for namespace modifications and files which have a pattern matched
        copytree(
            self.dir_to_copy, 
            new_dir, 
            ignore=wrap_ignore_files(
                to_inspect=set(self.files_to_analyze), 
                excluded_patterns=to_filter, 
                files_to_not_pattern_match=files_to_not_apply_filter,
                ),
            dirs_exist_ok=True
        )    

        count = 0

        gen = progressbar(range(len(self.files_to_analyze)), "Running: ")

        # Look through all files with specified extensions, in specified dirs, and write new contents to new_path
        for file in self.files_to_analyze:

            new_path = resolve_new_path(file, new_dir, self.dir_to_copy)
            count += namespace_modifier.change_file_namespace(file, new_path)

            next(gen)
        next(gen)
        
        self.count[new_dir] = count
        self.time[new_dir] = default_timer() - temp_time

    def _find_files_to_analyze(self): 
        """Find files with correct file types to analyze in given folders.
        """
        files = []
        for i in self.folders:
            if not isdir(i):
                raise OSError('Folder not found')
            for file in glob(f"{i}/**/*", recursive=True):
                if file.endswith(tuple(self.file_types_to_check)):
                    files.append(file)
        return files