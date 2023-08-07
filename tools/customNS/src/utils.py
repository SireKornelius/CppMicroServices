import re

def change_file_namespace(file_name, new_dir, dir, to_replace, replace_with):
    """
    Search through file for regex patterns matching namespace usage and replaces the current namespace name 
    with a new namespace name
    """
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    new_file_content, count = sub_regex(to_replace, replace_with, content)
    new_file_path = new_path(file_name, new_dir, dir)

    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.write(new_file_content)

    return count

def progressbar(it, pre, size = 40): 
    """
    Generator function for displaying the script's progress in parsing files
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

def new_path(file_name, new_dir, dir):
    """
    Finding new path for file in new dir
    """
    suffix = file_name.removeprefix(dir)
    return f"{new_dir}{suffix}"

def check_valid(input):
    """
    Validating user input is a valid c++ identifier (no support for non-english characters)
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

# https://en.cppreference.com/w/cpp/language/namespace - following functions try to match c++ namespace syntax
def reg_name_dec(to_replace, replace_with, string):
    fn = lambda matchobj : f"{matchobj.group(1)}{replace_with}{matchobj.group(5)}"
    return re.subn(rf'((^\s{{0}}|[^\w_])namespace(\s|")+?)({to_replace})([^\w_]|\s{{0}}$)', fn, string)

def reg_alias_name(to_replace, replace_with, string):
    fn = lambda matchobj : f"{matchobj.group(1)}{replace_with}{matchobj.group(7)}"
    return re.subn(rf'((^\s{{0}}|[^\w_])namespace(\s|")+?[\w_]+?(\s|")+?=(\s|")+?)({to_replace})([^\w_]|\s{{0}}$)', fn, string)

def reg_scope_post(to_replace, replace_with, string):
    fn = lambda matchobj : f"{matchobj.group(1)}{replace_with}{matchobj.group(3)}{matchobj.group(5)}"
    return re.subn(rf'(^\s{{0}}|[^\w_])({to_replace})((\s|")*?)(::)', fn, string)

def reg_scope_pre(to_replace, replace_with, string):
    fn = lambda matchobj : f"{matchobj.group(1)}{matchobj.group(2)}{matchobj.group(4)}{replace_with}{matchobj.group(8)}"
    return re.subn(rf'(::)((\s|")*?)(inline(\s|")*?|(\s|")*?)({to_replace})([^\w_]|\s{{0}}$)', fn, string)


def sub_regex(to_replace, replace_with, string):
    """
    Check line for one of four regex patterns and replace if found. Returns string with substitutions made and count of number of substitutions made.
    """
    new_str = string + ""
    count = 0
    check = [reg_name_dec, reg_alias_name, reg_scope_post, reg_scope_pre]
    for func in check:
        temp_string, temp_count = func(to_replace, replace_with, new_str)
        new_str = temp_string
        count += temp_count

    return new_str, count