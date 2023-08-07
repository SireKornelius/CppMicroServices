import re
from timeit import default_timer
from glob import glob
from functools import wraps
from os.path import dirname, abspath, expanduser, expandvars, join
#typing functions was introduced in python 3.5. Support or not?


def timeit(func):
    '''
    used as decorator to time function
    '''
    @wraps(func)
    def new_func(*args, **kwargs):
        start = default_timer()
        res = func(*args, **kwargs)
        print(f"{func.__name__} runtime: {default_timer() - start}")
        return res
    return new_func

class regexDefinitions():

    @staticmethod
    def readOnlyUpdatedRegexMatcher(string, replace_with, to_replace = 'cppmicroservices'):
        def regNameDec(string, replace_with, to_replace):
            fn = lambda matchobj : f"{matchobj.group(1)}{replace_with}{matchobj.group(5)}" # 78 chars in this line can use as ref
            return re.subn(rf'((^\s{{0}}|[^\w_])namespace(\s|")+?)({to_replace})([^\w_]|\s{{0}}$)', fn, string)

        def regAliasName(string, replace_with, to_replace):
            fn = lambda matchobj : f"{matchobj.group(1)}{replace_with}{matchobj.group(7)}"
            return re.subn(rf'((^\s{{0}}|[^\w_])namespace(\s|")+?[\w_]+?(\s|")+?=(\s|")+?)({to_replace})([^\w_]|\s{{0}}$)', fn, string)

        def regScopePost(string, replace_with, to_replace):
            fn = lambda matchobj : f"{matchobj.group(1)}{replace_with}{matchobj.group(3)}{matchobj.group(5)}"
            return re.subn(rf'(^\s{{0}}|[^\w_])({to_replace})((\s|")*?)(::)', fn, string)
        def regScopePre(string, replace_with, to_replace):
            fn = lambda matchobj : f"{matchobj.group(1)}{matchobj.group(2)}{matchobj.group(4)}{replace_with}{matchobj.group(8)}"
            return re.subn(rf'(::)((\s|")*?)(inline(\s|")*?|(\s|")*?)({to_replace})([^\w_]|\s{{0}}$)', fn, string)

        new_str = string + ""
        count = 0
        check = [regNameDec, regAliasName, regScopePost, regScopePre]
        for func in check:
            temp_string, temp_count = func(new_str, replace_with, to_replace)
            new_str = temp_string
            count += temp_count
        return new_str, count
    
    @staticmethod
    def readOnlySimpleMatcher(string, replace_with, to_replace = 'cppmicroservices'):
        fn = lambda matchobj : f"{matchobj.group(1)}{replace_with}{matchobj.group(3)}"
        return re.subn(rf'([^./1\w]|^\s{{0}})({to_replace})([^./1\w\-(]|\s{{0}}$)', fn, string)
    
class compareRegMatching():
    '''
    A class that can be used to compare behavior of regex matching functions used in script
    '''

    file_types_to_check = ('.hpp', '.cpp', '.h', '.json', '.tpp', '.in')

    @timeit
    def __init__(self, dir_to_test, new_ns_name, old_ns_name = 'cppmicroservices'):
        '''
        directory to simulate the script on, new namespace name, old namespace name (default cppmicroservices)
        '''
        self.to_replace = old_ns_name
        self.replace_with = new_ns_name
        self.changes = {}
        self.count = {}
        self.files = self._findFiles(dir_to_test)
    
    @timeit
    def readFiles(self, regexMatcher):
        '''
        takes in a regexMatcher function (string, replace_with, to_replace) -> modified string which is used to
        parse and modify files
        '''
        if regexMatcher.__name__ in self.changes:
            return
        
        self.changes[regexMatcher.__name__] = set()
        self.count[regexMatcher.__name__] = 0 

        for fi in self.files:
            cnt, change = self._processFile(fi, regexMatcher)
            self.count[regexMatcher.__name__] += cnt
            self.changes[regexMatcher.__name__].update(change)
        return
    
    def _processFile(self, fileName, regexMatcher):
        '''
        scan given file using regexMatcher function and detect potential modifications made
        '''
        with open(fileName, 'r', encoding='utf-8') as file:
            content = file.read()

        new_file, count = regexMatcher(content, self.replace_with, self.to_replace)

        lines_orig = content.split('\n')
        lines_after = new_file.split('\n')

        return count, self._compareFileBeforeAfter(lines_orig, lines_after, fileName)
    
    def _compareFileBeforeAfter(self, fcontent1, fcontent2, fileName):
        '''
        compare original contents of file and simulated new contents
        '''
        if len(fcontent1) != len(fcontent2):
            raise ValueError("files have different num lines")
        ret_list = []
        for orig, new, line_num in zip(fcontent1, fcontent2, range(len(fcontent1))):
            if orig == new:
                continue

            ret_list.append((fileName, line_num, new, orig))

        return ret_list
    
    @timeit
    def _findFiles(self, dir):
        '''
        return a list of files in given dir to open. file_types_to_check / copytrees args are good place to check for errors.
        '''
        files = [abspath(expanduser(expandvars(file))) for file in glob(f"{dir}/**/*", recursive=True) 
                 if file.endswith(self.file_types_to_check) and not abspath(expanduser(expandvars(file))).startswith(join(dir, 'build'))]
        return files
    
    @timeit
    def diffRegexMatchers(self, regexMatcher1, regexMatcher2, fileWrite):
        '''
        Write the difference in proposed modifications of two regex matcher functions to fileWrite
        '''
        exclusive_first = self.changes[regexMatcher1.__name__] - self.changes[regexMatcher2.__name__]
        exclusive_second = self.changes[regexMatcher2.__name__] - self.changes[regexMatcher1.__name__]

        with open(fileWrite, 'w', encoding='utf-8') as file:
            file.write(f'file types checking: {self.file_types_to_check}\n')
            file.write(f'first: {regexMatcher1.__name__}\n_______________________\n')
            for i in exclusive_first:
                file.write(f"filename: {i[0]}; line number: {i[1]}\nnew line: {i[2]}\nold line: {i[3]}\n\n")
            file.write(f'\nsecond: {regexMatcher2.__name__}\n________________________\n')
            for i in exclusive_second:
                file.write(f"filename: {i[0]}; line number: {i[1]}\nnew line: {i[2]}\nold line: {i[3]}\n\n")
        return 


if __name__ == "__main__":
    # a little tool
    top_dir = dirname(dirname(dirname(dirname(abspath(__file__)))))
    reg = compareRegMatching(top_dir, 'cppms')

    do_nothing_func = lambda string, replace_with, to_replace : (string, 0)
    do_nothing_func.__name__ = "do_nothing_func_lambda"

    basic_func = lambda string, replace_with, to_replace : (string.replace(to_replace, replace_with), string.count(to_replace))
    basic_func.__name__ = "basic_func_lambda"

    reg.readFiles(do_nothing_func)
    reg.readFiles(basic_func)
    reg.readFiles(regexDefinitions.readOnlySimpleMatcher)
    reg.readFiles(regexDefinitions.readOnlyUpdatedRegexMatcher)
    #reg.diffRegexMatchers(regexDefinitions.readOnlyUpdatedRegexMatcher, 
    #                      regexDefinitions.readOnlySimpleMatcher, f'{top_dir}/tools/cli_tool/rando.txt')
    print(reg.count)

