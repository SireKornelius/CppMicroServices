import sys
from os.path import abspath, expanduser, expandvars, dirname
from utils import DirGenerator, NamespaceModifier, parse_args

# Get absolute path to directory to be copied.
# expandvars/expanduser accounts for unix specific tilde and environment variables.
top_dir = abspath(expanduser(expandvars(dirname(dirname(dirname(dirname(__file__)))))))

dirs_to_check = ['compendium', 'framework', 'httpservice', 'shellservice', 'util', 'webconsole', 'tools/shell'] # Folders to analyze
file_types_check = ['.hpp', '.cpp', '.h', '.json', '.tpp', '.in'] # File types to analyze
to_filter = ['.git*', 'build', '__pycache__'] # Files to not copy over to new dir - with unix shell style wildcards
files_to_not_apply_filter = [f'{top_dir}/third_party*'] # Exceptions to to_filter - with unix shell style wildcards

if __name__ == '__main__':

    # Pass all command line arguments after path-to-script to be parsed 
    args = parse_args(sys.argv[1:])
    to_replace = args.previousNamespace
    replace_with = args.namespace
    stats = args.stats
    new_dir = abspath(expanduser(expandvars(args.path_to)))

    # Namespace object used to modify files to new namespace
    namespace_modifier = NamespaceModifier(old_namespace=to_replace, new_namespace=replace_with)

    # DirGenerator object used to create new modified directory
    dgen = DirGenerator(
        dir_to_copy=top_dir,
        folders_to_analyze=dirs_to_check,
        file_types_to_check=file_types_check,
    )
    dgen.create_modified_dir(
        new_dir=new_dir, 
        to_filter=to_filter, 
        files_to_not_apply_filter=files_to_not_apply_filter,
        namespace_modifier=namespace_modifier
        )

    if stats:
        print(dgen.count)
        print(dgen.time)