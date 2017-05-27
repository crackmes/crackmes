#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import argparse
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
    parser = argparse.ArgumentParser(description='Crackmes uploader to IPFS, generating the proper file structures and \
            metadata')
    parser.add_argument('-n', '--name', nargs=1, help='Name of the crackme')
    parser.add_argument('-p', '--path', nargs=1, help='Path of the crackme')
    parser.add_argument('-a', '--author', nargs=1, help='Author name or nickname')
    parser.add_argument('-t', '--type', nargs=1, help='Binary type', choices=['ELF', 'PE'])
    parser.add_argument('-x', '--arch', nargs=1, help='Binary architecture', choices=['x86', 'x86-64', 'MIPS', 'ARM', 'ARM64'])
    parser.add_argument('--host', nargs=1, type=str, default='127.0.0.1', help='IPFS host, default: 127.0.0.1')
    parser.add_argument('--port', nargs=1, type=int, default=5001, help='IPFS port, default: 5001')
    args = parser.parse_args()

    crackme_name = args.name[0]
    crackme_full_path = args.path[0]
    author_name = args.author[0]
    exec_type = args.type[0]
    exec_arch = args.arch[0]
    date = time.time()

    ipfs_host = args.host
    ipfs_port = args.port
    print('port', ipfs_port, 'host', ipfs_host)

    path = get_folder_path(crackme_name)
    print('PATH', path)
    create_dir(path)

    try:
        copy2(crackme_full_path, path)
    except FileNotFoundError:
        print('ERROR: File doesn\'t exist')
        sys.exit(1)

    with open(os.path.join(path, 'metadata.txt'), 'w+') as f:
        f.write(';'.join([crackme_name, author_name, str(date)]))

    # TODO: Allow to change this


    api = ipfsapi.connect(ipfs_host, ipfs_port)
    result = api.add(path)
    if len(result) != 3:
        print('ERROR: Not a path hash')
    else:
        print('Your IPFS hash for the crackme is {0}'.format(result[-1]['Hash']))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Bye!')
