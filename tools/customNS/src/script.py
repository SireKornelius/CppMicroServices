import sys
from timeit import default_timer
from glob import glob
from os.path import abspath, expanduser, expandvars, join, dirname
from shutil import copytree
from multiprocessing import Pool
from argparse import ArgumentParser
from utils import DirGenerator, parse_args

# File types to look through, folders to look through, and files/folders to not copy
file_types_check = ('.hpp', '.cpp', '.h', '.json', '.tpp', '.in')
folders_check = ['compendium', 'framework', 'httpservice', 'shellservice', 'util', 'webconsole', 'tools/shell']
to_filter = ('.git*', 'build', '__pycache__') # modify this

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    to_replace = args.previousNamespace
    replace_with = args.namespace
    stats = args.stats
    
    top_dir = abspath(expanduser(expandvars(dirname(dirname(dirname(dirname(__file__)))))))
    new_dir = abspath(expanduser(expandvars(args.path_to)))

    dgen = DirGenerator(
        new_namespace=replace_with,
        old_namespace=to_replace,
        dir_to_copy=top_dir,
        folders_to_analyze=folders_check,
        file_types_to_check=file_types_check
    )

    dgen.create_modified_dir(new_dir=new_dir, to_filter=to_filter)

    if stats:
        print(dgen.count)
        print(dgen.time)