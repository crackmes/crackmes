#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
try:
    import ipfsapi
except:
    print('Please install ipfsapi (pip install ipfsapi)')
    sys.exit(1)

import os
import time
from shutil import copy2

def create_dir(path):
    if os.path.isfile(path):
        raise OSEerror('{0} is a regular file'.format(path))
    else:
        os.mkdir(path)

def get_folder_path(crackme_name):
    path = os.path.join(os.getcwd(), 'crackmes_{0}'.format(crackme_name))
    count = 1
    while os.path.isdir(path):
        path = os.path.join(os.getcwd(), 'crackmes_{0}_{1}'.format(crackme_name,
                                                                    count))
        count += 1
    return path

def main():
    crackme_name = input('Crackme name > ')
    crackme_full_path = input('Crackme full path> ')
    author_name = input('Author name > ')
    exec_type = input('Executable format (ELF, PE...) > ')
    exec_type = input('Architecture (x86, x86-64, MIPS, ARM, AVR...) > ')
    date = time.time()

    path = get_folder_path(crackme_name)
    create_dir(path)

    try:
        copy2(crackme_full_path, path)
    except FileNotFoundError:
        print('ERROR: File doesn\'t exist')
        sys.exit(1)


    with open(os.path.join(path, 'metadata.txt'), 'w+') as f:
        f.write(';'.join([crackme_name, author_name, str(date)]))

    # TODO: Allow to change this
    api = ipfsapi.connect('127.0.0.1', 5001)
    print('Your IPFS hash for the crackme is {0}'.format(
                                                    api.add(path)[-1]['Hash']
                                                    ))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Bye!')
