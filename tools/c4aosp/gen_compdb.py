#!/usr/bin/python3

from __future__ import print_function

import argparse
import ijson
import json
import os
import re

from typing import List
from typing import Set
from typing import Dict

class NinjaCache(object):
    def __init__(self, filename: str):
        self.filename = filename
        self.compdb = []

    def append(self, directory, arguments, file):
        self.compdb.append({
            'directory': directory,
            'arguments': arguments,
            "file": file
        })

    def dump(self):
        # dump to file
        try:
            with open(self.filename, "w") as compdb_file:
                json.dump(self.compdb, compdb_file, indent=1)
        except EnvironmentError:
            exit(1, "dump to outfile err")

def main():
    parser = argparse.ArgumentParser(description='gen compile_commands for android')

    parser.add_argument('-p', '--product',  help='which product u want, TARGET_PRODUCT')
    
    parser.add_argument('--path', help='which dir files you want to generate compile_commands, must relative with aosp top')

    args = parser.parse_args()


    if args.product is None:
        target_product = os.getenv('TARGET_PRODUCT')
    else:
        target_product = args.product

    if target_product is None or target_product == "":
        exit(1, 'could not found TARGET_PRODUCT, or u should specified with --product')

    if args.path is None:
        exit(1, 'prefix path not specified')

    try:
        with open(args.infile, 'rb') as fin:
            nj_cache = NinjaCache(args.outfile)
            jsonobj = ijson.items(fin, 'item')
            jsons = (o for o in jsonobj)
            for jo in jsons:
                # print("directory={}\narguments={}\nfile={}\n".format(jo['directory'],jo['arguments'],jo['file']))
                file:str = jo['file']
                directory:str = jo['directory']
                arguments:str = jo['arguments']
                if file.startswith(args.path):
                    nj_cache.append(directory, arguments, file)
            nj_cache.dump()

    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        exit(1, "infile error")

if __name__ == "__main__":
    main()
