import os, shutil
import argparse
from distutils.dir_util import copy_tree

def get_arguments():
    parser = argparse.ArgumentParser(description='periodic macchanger')
    parser.add_argument('-s', '--src', help = 'source directory(default current)', default='.', required = False)
    parser.add_argument('-d', '--dst', help = 'destination directory(default current)', default='.', required = False)
    parser.add_argument('-m', '--merge', help = 'merge content on destination directory(default true)', default=True, required = False)
    return parser.parse_args()

def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# target_path = '/home/user/workspace/python/directorybackup'
# backup_path = '/home/user/workspace/python/directorybackup/backup'

args = get_arguments()
# if args.merge:   IMPORTANT! uncomment till macchager have a backup!!!
#     clear_folder(args.dst)
all_subdirs = [d for d in os.scandir(args.src) if (os.path.isdir(d) and d.path != args.dst)]
latest_subdir = max(all_subdirs, key=os.path.getmtime)
print(latest_subdir.path)
copy_tree(src = latest_subdir, dst = args.dst, verbose = True)