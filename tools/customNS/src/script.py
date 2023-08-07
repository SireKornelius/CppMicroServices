from timeit import default_timer
from glob import glob
from os.path import isdir, abspath, expanduser, expandvars, join
from shutil import copytree, ignore_patterns
from multiprocessing import Pool
from argparse import ArgumentParser
from utils import check_valid, progressbar, change_file_namespace


def parse_args():
    '''
    Parse command line arguments 
    '''
    parser = ArgumentParser(description='Copy and change cppmicroservices namespace into specified dir')
    
    parser.add_argument(
        'namespace', 
        metavar='NAMESPACE', 
        help='new namespace name'
        )
    
    parser.add_argument(
        'path_from', 
        metavar='PATH_FROM', 
        help='path to directory to copy from'
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
        '--sprocess', 
        '-sp', 
        action='store_true', 
        help='Use single process (default=False)'
        )
    
    parser.add_argument(
        '--stats',
        '-st', 
        action='store_true', 
        help='print instances of namespace/namespace usage modified and runtime duration'
        )
    
    return parser.parse_args()


def modify_namespace():
    '''
    Copy directory to specified path and modify new directory namespace name
    '''
    starttime = default_timer()

    args = parse_args()

    replace_with = args.namespace
    new_dir = args.path_to
    dir = args.path_from
    singleProcess = args.sprocess
    timed = args.stats

    if not check_valid(replace_with):
        raise ValueError('Invalid namespace name')
    if not isdir(dir):
        raise OSError(f"{dir} not found")
    
    if args.previousNamespace:
        to_replace = args.previousNamespace
    else:
        raise ValueError('Invalid namespace name')

    print('Copying Files..')
    
    new_dir = abspath(expanduser(expandvars(new_dir)))
    dir = abspath(expanduser(expandvars(dir)))

    file_types_to_check = ('.hpp', '.cpp', '.h', '.json', '.tpp', '.in')

    #not touching files in build dir
    
    files = [abspath(expanduser(expandvars(file))) for file in glob(f"{dir}/**/*", recursive=True) 
             if file.endswith(file_types_to_check) and 
             not abspath(expanduser(expandvars(file))).startswith(join(dir, 'build'))] 
    
    finding_files_time = default_timer() - starttime
    temp_time = default_timer()

    # copy tree after looking through files
    # if need to check more file types change
    
    copytree(
        dir, 
        new_dir, 
        ignore=ignore_patterns('.git*', 'build', '__pycache__', *file_types_to_check), 
        dirs_exist_ok=True
        )    
    copying_time = default_timer() - temp_time

    temp_time = default_timer()
    count = 0
    gen = progressbar(range(len(files)), "Running: ")

    if singleProcess:
        for fi in files:
            count += change_file_namespace(fi, new_dir, dir, to_replace, replace_with)
            next(gen)
        next(gen)
        
    else:
        with Pool() as pool:
            results = []

            for fi in files:
                result = pool.apply_async(change_file_namespace, (fi, new_dir, dir, to_replace, replace_with))
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
    modify_namespace()