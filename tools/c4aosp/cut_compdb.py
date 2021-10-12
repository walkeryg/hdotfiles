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
    parser = argparse.ArgumentParser(description='cut a small compile_commands from whole bigger one')

    parser.add_argument('-i', '--infile', help='the whole bigger compile_commands file')

    parser.add_argument('-o', '--outfile',  help='the compile_commands file cut from infile')
    
    parser.add_argument('--prefix', help='which dir files you want to generate')

    args = parser.parse_args()


    if args.infile is None:
        exit(1, 'no infile is specified')

    if args.outfile is None:
        exit(1, 'no outfile is specified')

    if args.infile == args.outfile:
        exit(1, 'infile path should different with outfile')
    
    if args.prefix is None:
        exit(1, 'prefix not specified')

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
                if file.startswith(args.prefix):
                    nj_cache.append(directory, arguments, file)
            nj_cache.dump()

    except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
        exit(1, "infile error")

if __name__ == "__main__":
    main()