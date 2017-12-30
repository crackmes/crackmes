#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import argparse
import shutil
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
        os.makedirs(path, exist_ok=True)

def download(api, file, dest_dir):
    with open(file) as f:
        content = f.read()

    crackme_link = content.split(';')[0]

    if os.path.exists("{}/{}".format(dest_dir, crackme_link)):
        print("Crackme {} already donwloaded".format(file))
        return

    # TODO: Can we pass some parameter to ipfs api to download the content to
    # that directory directly?
    api.get(crackme_link)
    shutil.move(crackme_link, dest_dir)
    print("Downloaded crackme {} to directory {}".format(file, dest_dir))

def main():
    parser = argparse.ArgumentParser(description='Crackmes downloader')
    parser.add_argument('-a', '--all', action="store_true", help='Download all crackmes')
    parser.add_argument('-D', '--destdir', type=str, default='downloads', help='Destination directory')
    parser.add_argument('--host', nargs=1, type=str, default='127.0.0.1', help='IPFS host, default: 127.0.0.1')
    parser.add_argument('--port', nargs=1, type=int, default=5001, help='IPFS port, default: 5001')
    args = parser.parse_args()

    ipfs_host = args.host
    ipfs_port = args.port
    print('port', ipfs_port, 'host', ipfs_host)

    create_dir(args.destdir)

    api = ipfsapi.connect(ipfs_host, ipfs_port)

    for root, subdirs, files in os.walk("."):
        if root[0:3] != "./l": # XXX
            continue

        dest_dir = "{}/{}".format(args.destdir, root)
        create_dir(dest_dir)
        for i in files:
            file = "{}/{}".format(root, i)
            download(api, file, dest_dir)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Bye!')
