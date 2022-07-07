#!/usr/bin/python3

import enum
import os
import re
import argparse
import shutil

from enum import Enum
from typing import List

EXCLUDE_PRJS =[
"kernel/system", 
"kernel/linux",
"vendor/realtek/system", 
"vendor/realtek/frameworks/native/libvip",
"vendor/realtek/image_file_creator",
"kernel/system/lib/develop/DDK", 
"device/realtek/RealtekATV-kernel",
"vendor/realtek/system/lib/develop/DDK", 
"vendor/realtek/system/lib/develop/linux-fusion"
] 

class CollectState(Enum):
    SKIP = 1,
    COLLECT_NON_TRACKING = 2,
    COLLECT_TRACKING = 3

def is_project(args_str: str):
    match_obj = re.match(r"^project ", args_str)
    if match_obj:
        return True
    else:
        return False

def get_project(args_str: str):
    match_obj = re.match(r"^project[\t ](\S*)[\t ]*\(", args_str)
    if match_obj:
        return match_obj.group(1) 
    else:
        match_obj = re.match(r"^project[\t ](\S*)[\t ]*branch", args_str)
        if match_obj:
            return match_obj.group(1)
        else:    
            return ""

def is_none_branch(args_str: str):
    match_obj = re.search(r"NO BRANCH", args_str)
    if match_obj:
        return True
    else: 
        return False

def is_m_or_a_file(args_str: str):
    match_obj = re.match(r"[ \t]-[m-][\t ]", args_str)
    if match_obj:
        return True
    else:
        return False

def get_file(args_str: str):
    match_obj = re.match(r"[ \t]-[m-][\t ](.*)$", args_str)
    if match_obj:
        file:str = match_obj.group(1)
        if file[-1] == '/':
            return ""
        return match_obj.group(1)
    else:
        return "" 

def is_excluded(args_str: str):
    for ex in EXCLUDE_PRJS:
        match_obj = re.search(ex, args_str)
        if match_obj:
            return True
    return False

def remove_prefix(args_str: str, prefix:str):
    if args_str.startswith(prefix):
        return args_str[len(prefix):]
    else:
        return args_str

def cp_parents(target_dir, file):
    if not os.path.exists(file):
        print("can not copy file:" + file)
        return

    dir = os.path.dirname(file)
    if os.path.exists(os.path.join(target_dir, dir)):
        dest = os.path.normpath(os.path.join(target_dir, file))
        if os.path.exists(dest):
            print("overwrite exist")
        shutil.copy(file, dest)
    else:
        print("makedirs:" + os.path.join(target_dir, dir))
        os.makedirs(os.path.join(target_dir, dir), exist_ok=True)
        dest = os.path.normpath(os.path.join(target_dir, file))
        if os.path.exists(dest):
            print("overwrite exist")
        shutil.copy(file, dest)

def main():
    parser = argparse.ArgumentParser(description='Collect Decopling files, only android root directory')

    parser.add_argument('--infile', help='repo status file, please use "repo status >> tmp.log" to generate it' )
    parser.add_argument('--prefix', help='Android Root Prefix' )
    parser.add_argument('--copy_target', help='If have this param, it will copy files to the target')
    args = parser.parse_args()

    if args.infile is None:
        exit("missing status file")

    if args.prefix is None:
        exit("android root preflix should be set")

    need_copy = False 
    if args.copy_target is not None:
        if os.path.exists(args.copy_target):
            need_copy = True
        else:
            exit("target dir is not exist")

    collected_files = []
    collected_warning_files = []
    state = CollectState.SKIP
    with open(args.infile) as inf:
        last_project = ""
        for line in inf:
            # find next prj
            if is_project(line):
                if not is_excluded(line):
                    if is_none_branch(line):
                        state = CollectState.COLLECT_NON_TRACKING
                    else:
                        state = CollectState.COLLECT_TRACKING
                else:
                    state = CollectState.SKIP
                last_project = get_project(line)
                continue

            if is_m_or_a_file(line):
                if last_project != "":
                    if state == CollectState.COLLECT_NON_TRACKING:
                        if(get_file(line) != ""):
                            collected_files.append(os.path.join(remove_prefix(last_project, args.prefix), get_file(line)))
                    elif state == CollectState.COLLECT_TRACKING:
                        if(get_file(line) != ""):
                            collected_warning_files.append(os.path.join(remove_prefix(last_project, args.prefix), get_file(line)))
        
        print("Total collected %s files" % len(collected_files))

    for file in collected_files:
        print(file)
        if need_copy:
            cp_parents(args.copy_target, file)

    print("the following files may be submited, please check...")
    for file in collected_warning_files:
        print(file)


if __name__ == "__main__":
    main()