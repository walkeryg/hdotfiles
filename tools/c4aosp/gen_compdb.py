#!/usr/bin/python3

from __future__ import print_function

import argparse
import ijson
import json
import os
import re
from generate_compdb import NinjaHandle

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

    def append_list(self, compdb: List):
        self.compdb.extend(compdb)

    def dump(self):
        # dump to file
        self.compdb.sort(key = lambda item:item["file"])
        try:
            with open(self.filename, "w") as compdb_file:
                json.dump(self.compdb, compdb_file, indent=1)
        except EnvironmentError:
            exit(1, "dump to outfile err")

def main():
    parser = argparse.ArgumentParser(description='gen compile_commands for android')

    parser.add_argument('-p', '--product',  help='which product u want, TARGET_PRODUCT')
    parser.add_argument('-r', '--root', help='aosp root dir')
    parser.add_argument('--path', help='which dir files you want to generate compile_commands, must relative with aosp top')
    parser.add_argument('-f', '--force', help='force to generate if already exist')

    args = parser.parse_args()


    if args.product is None:
        target_product = os.getenv('TARGET_PRODUCT')
    else:
        target_product = args.product

    if target_product is None or target_product == "":
        exit(1, 'could not found TARGET_PRODUCT, or u should specified with --product')

    if args.root is None:
        exit(1, 'no aosp root is specified. please give it using -r or --root')
    
    if args.path is None:
        exit(1, 'prefix path not specified')

    ninga_name = "build-" + target_product + ".ninja"
    ninja_file = os.path.join(args.root, "out", ninga_name)
    
    if not os.path.isfile(ninja_file):
        exit(1, "could not find ninja files:" + ninja_file)

    target_path = os.path.join(args.root, args.path)

    if not os.path.isdir(target_path):
        exit(1, "could not find target path:" + target_path)

    target_file = os.path.join(target_path, "compile_commands.json")

    if os.path.exists(target_file):
        if args.force is None:
            exit(1, "compile_commands.json is already exist, will")
        else:
            print("force to overwrite the exist compile_commands.json")
    
    bp_compdb = os.path.join(args.root, "out/soong/development/ide/compdb/compile_commands.json")
    
    nj_cache = NinjaCache(target_file)
    if os.path.exists(bp_compdb):
        print("Found bp_compdb:" + bp_compdb)
        # cut from whole compile_commands.json
        try:
            with open(bp_compdb, 'rb') as fin:
                jsonobj = ijson.items(fin, 'item')
                jsons = (o for o in jsonobj)
                for jo in jsons:
                    # print("directory={}\narguments={}\nfile={}\n".format(jo['directory'],jo['arguments'],jo['file']))
                    file:str = jo['file']
                    directory:str = jo['directory']
                    arguments:str = jo['arguments']
                    if file.startswith(args.path):
                        nj_cache.append(directory, arguments, file)

        except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
            exit(1, "infile error")
        print("found " + str(len(nj_cache.compdb)) + " in " + bp_compdb)
    else:
        print("Not found bp_compdb:" + bp_compdb)
        print("You could generate the whole compile_commands.json by SOONG_GEN_COMPDB=1 SOONG_GEN_COMPDB_DEBUG=1 when you compile, see readme")

    ninja_handle = NinjaHandle(ninja_file, args.root, target_path)
    ninja_handle.gen_compile_commands_for_directory(args.path)
    nj_cache.append_list(ninja_handle.compdb)
    nj_cache.dump()


if __name__ == "__main__":
    main()
