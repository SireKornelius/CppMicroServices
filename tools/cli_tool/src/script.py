from timeit import default_timer
from glob import glob
from os.path import isdir, isfile, dirname, abspath, expanduser, expandvars, join
from os import rename, remove
from shutil import copytree, ignore_patterns, rmtree
from multiprocessing import Pool, current_process
import argparse
from utils import checkValid, progressbar, subRegex, new_path


def changeFileNamespace(file_name, new_dir, dir, to_replace, replace_with):
    '''
    Search through file for regex patterns matching namespace usage and replaces the current namespace name 
    with a new namespace name
    '''
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    new_file_content, count = subRegex(to_replace, replace_with, content)
    new_file_path = new_path(file_name, new_dir, dir)

    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.write(new_file_content)

    return count


def parseArgs():
    '''
    Parse command line arguments 
    '''
    parser = argparse.ArgumentParser(description='Copy and change cppmicroservices namespace into specified dir')
    parser.add_argument('namespace', metavar='NAMESPACE', help='new namespace name')
    parser.add_argument('path_from', metavar='PATH_FROM', help='path to directory to copy from')
    parser.add_argument('path_to', metavar='PATH_TO', help='path to directory to copy to')
    parser.add_argument('--previousNamespace', '-pN', metavar='pN', help='the namespace to change (default=cppmicroservices)', default='cppmicroservices')
    parser.add_argument('--sprocess', '-sp', action='store_true', help='Use single process (default=False)')
    parser.add_argument('--stats', '-st', action='store_true', help='print instances of namespace/namespace usage modified and runtime duration')
    
    return parser.parse_args()



def modifyNamespace():
    '''
    Copy directory to specified path and modify new directory namespace name
    '''
    starttime = default_timer()

    args = parseArgs()

    replace_with = args.namespace
    new_dir = args.path_to
    dir = args.path_from
    singleProcess = args.sprocess
    timed = args.stats

    if not checkValid(replace_with):
        raise ValueError('Invalid namespace name')
    if not isdir(dir):
        raise OSError(f"{dir} not found")
    
    if args.previousNamespace:
        to_replace = args.previousNamespace
    else:
        raise ValueError('Invalid namespace name')

    print('Copying Files..')

    # if need to check more file types change
    copytree(dir, new_dir, ignore=ignore_patterns('.git*', 'build', '__pycache__', '*.hpp', '*.cpp', '*.h', '*.json', '*.tpp', '*.in'), dirs_exist_ok=True)
    copying_time = default_timer() - starttime
    temp_time = default_timer()

    new_dir = abspath(expanduser(expandvars(new_dir)))
    dir = abspath(expanduser(expandvars(dir)))

    file_types_to_check = ('.hpp', '.cpp', '.h', '.json', '.tpp', '.in')

    #not touching files in build dir
    files = [abspath(expanduser(expandvars(file))) for file in glob(f"{dir}/**/*", recursive=True) 
             if file.endswith(file_types_to_check) and not abspath(expanduser(expandvars(file))).startswith(join(dir, 'build'))] # get rid of rst file, no need to rename
    
    finding_files_time = default_timer() - temp_time


    temp_time = default_timer()
    count = 0
    gen = progressbar(range(len(files)), "Running: ")

    if singleProcess:
        for fi in files:
            count += changeFileNamespace(fi, new_dir, dir, to_replace, replace_with)
            next(gen)
        next(gen)
        
    else:
        with Pool() as pool:
            results = []
            for fi in files:
                result = pool.apply_async(changeFileNamespace, (fi, new_dir, dir, to_replace, replace_with))
                results.append(result)
            for res in results:
                count += res.get()
                next(gen)
            next(gen)

    if timed:
        print(f"modifications made: {count}")
        print(f"copying files: {copying_time}")
        print(f"finding files: {finding_files_time}")
        print(f"analyzing & writing files: {default_timer() - temp_time}")
        print(default_timer() - starttime)

if __name__ == '__main__':
    modifyNamespace()