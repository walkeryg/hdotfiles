#!/usr/bin/python3

from __future__ import print_function

import argparse
import json
import os
import re
import shlex
import sys

from typing import List
from typing import Set
from typing import Dict

RULE_PATTERN = re.compile(r'^\s*rule\s+(\S+)$')
DESCRIPTION_PATTERN = re.compile(r'^\s*description\s*=\s*target.*:\s*(?P<module>\S+)\s*.*$')
DESCRIPTION_PREBUILT_PATTERN = re.compile(r'^\s*description\s*=\s*target\s+Prebuilt\s*:\s*(?P<module>\S+)\s*.*$')
DESCRIPTION_SHARED_PATTERN = re.compile(r'^\s*description\s*=\s*target\s+SharedLib\s*:\s*(?P<module>\S+)\s*.*$')
DESCRIPTION_C_THUMB_PATTERN = re.compile(r'^\s*description\s*=\s*target\s+thumb\s+C\+*\s*:\s*(?P<module>\S+)\s*<=\s*(?P<file>\S+)\s*$')
DESCRIPTION_C_ARM_PATTERN = re.compile(r'^\s*description\s*=\s*target\s+arm\s+C\+*\s*:\s*(?P<module>\S+)\s*<=\s*(?P<file>\S+)\s*$')
COMMAND_PATTERN = re.compile(r'^\s*command\s*=\s*(?P<shell>\S+)\s*-c\s*"(?P<args>.+)"$')
BUILD_PATTERN = re.compile(r'^\s*build\s+.*:\s*(?P<rule>\S+)\s+(?P<file>\S+)')

# Samples
# description = target SharedLib: libfpp (out/target/product/G07/obj/SHARED_LIBRARIES/libfpp_intermediates/LINKED/libfpp.so)
# description = target Prebuilt: netd (out/target/product/G07/obj/EXECUTABLES/netd_intermediates/netd)
# description = target thumb C: libfpp <= vendor/realtek/common/ATV/frameworks/native/customerHAL/src/demux/matrix_ringbuf.c
# description = Target Java: out/target/common/obj/APPS/RtkDisplayMonitor_intermediates/classes-full-debug.jar
# description = target Java source list: RtkDisplayMonitor

# target [ShareLib, Prebuilt] as the start of the module
# target thumb C: module is the C file of the module
# see ninja_pattern.txt

#rule rulename
# description = 
# command = 
#build target: rulename dependencys

# the dependencys will including all obj & so & toolchain

class NinjaHandle(object):
    def __init__(self, filename: str, root: str, outpath: str=""):
        self.filename = filename
        self.rules = {}
        self.compdb = []
        self.directory = root
        self.outpath = outpath
        self.cat_cache = {}

    def cat_expand(self, match):
        file_name = match.group(1).strip()

        if file_name in self.cat_cache:
            return self.cat_cache[file_name]

        try:
            with open(file_name) as cat_file:
                content = cat_file.read().replace('\n', ' ').strip()
        except IOError as ex:
            print(ex, file=sys.stderr)
            content = None

        self.cat_cache[file_name] = content
        return content


    def parse_command(self, command):
        while command:
            first_space = command.find(' ', 1)
            if (first_space == -1):
                first_space = len(command)

            if command[0:first_space].endswith('/clang') or command[0:first_space].endswith('/clang++'):
                break

            command = command[first_space:]

        command = command.strip()

        if not command:
            return ""

        return command

    def gen_compile_commands_for_modules(self, module_list: Set[str]):
        status: Dict = dict()
        cur_module = ""
        file = ""
        command = ""
        with open(self.filename) as ninja_file:
            for line in ninja_file:
                rule_match = RULE_PATTERN.match(line)
                if rule_match:
                    rule_name = rule_match.group(1)
                    if command != "" and file != "":
                    # we can append last compdb records, when we encounter a new rule
                        self.compdb.append({
                            'directory': self.directory,
                            'arguments': command.split(),
                            "file": file
                        })
                    command = ""
                    file = ""
                    continue

                description_match = DESCRIPTION_PATTERN.match(line)
                if description_match:
                    module_name = description_match.group('module')
                    if cur_module != module_name and len(status) >= len(module_list):
                        print("all modules is founded, found %d modules, quit!" % len(status))
                        break
                    if module_name in module_list:
                        if status.__contains__(module_name) is not True:
                            status[module_name] = True

                        description_c_match = DESCRIPTION_C_THUMB_PATTERN.match(line)
                        if not description_c_match:
                            description_c_match = DESCRIPTION_C_ARM_PATTERN.match(line)

                        if description_c_match:
                            file = description_c_match.group("file")
                    cur_module = module_name
                    continue

                command_match = COMMAND_PATTERN.match(line)
                if command_match:
                    if file != "":
                        # only command after c pattern could be clang/clang++ command
                        # parser_command will check again
                        command = self.parse_command(command_match.group("args"))
                    continue

            # encounter file end, the last one should append 
            if command != "" and file != "":
            # we can append last compdb records, when we encounter a new rule
                self.compdb.append({
                    'directory': self.directory,
                    'arguments': command.split(),
                    "file": file
                })
            command = ""
            file = ""

        with open(os.path.join(self.outpath, 'compile_commands.json'), 'w') as compdb_file:
            json.dump(self.compdb, compdb_file, indent=1)
        
    def gen_compile_commands_for_files(self, file_list: Set[str]):
        with open(self.filename) as ninja_file:
            file = ""
            command = ""
            for line in ninja_file:
                rule_match = RULE_PATTERN.match(line)
                if rule_match:
                    rule_name = rule_match.group(1)
                    if command != "" and file != "":
                    # we can append last compdb records, when we encounter a new rule
                        self.compdb.append({
                            'directory': self.directory,
                            'arguments': command.split(),
                            "file": file
                        })
                    command = ""
                    file = ""
                    continue

                description_c_match = DESCRIPTION_C_THUMB_PATTERN.match(line)
                if not description_c_match:
                    description_c_match = DESCRIPTION_C_ARM_PATTERN.match(line)

                if description_c_match:
                    file = description_c_match.group("file")
                    if file not in file_list:
                        file = ""
                    continue

                command_match = COMMAND_PATTERN.match(line)
                if command_match:
                    if file != "":
                        # only command after c pattern could be clang/clang++ command
                        # parser_command will check again
                        command = self.parse_command(command_match.group("args"))
                    continue
        with open(os.path.join(self.outpath, 'compile_commands.json'), 'w') as compdb_file:
            json.dump(self.compdb, compdb_file, indent=1)

    def gen_compile_commands_for_directory(self, directory:str):
        with open(self.filename) as ninja_file:
            file = ""
            command = ""
            for line in ninja_file:
                rule_match = RULE_PATTERN.match(line)
                if rule_match:
                    rule_name = rule_match.group(1)
                    if command != "" and file != "":
                    # we can append last compdb records, when we encounter a new rule
                        self.compdb.append({
                            'directory': self.directory,
                            'arguments': command.split(),
                            "file": file
                        })
                    command = ""
                    file = ""
                    continue

                description_c_match = DESCRIPTION_C_THUMB_PATTERN.match(line)
                if not description_c_match:
                    description_c_match = DESCRIPTION_C_ARM_PATTERN.match(line)

                if description_c_match:
                    file = description_c_match.group("file")
                    if not file.startswith(directory):
                        file = ""
                    continue

                command_match = COMMAND_PATTERN.match(line)
                if command_match:
                    if file != "":
                        # only command after c pattern could be clang/clang++ command
                        # parser_command will check again
                        command = self.parse_command(command_match.group("args"))
                    continue
        with open(os.path.join(self.outpath, 'compile_commands.json'), 'w') as compdb_file:
            json.dump(self.compdb, compdb_file, indent=1)

    def gen_all_for_ninja(self):
        cur_module = ""
        file = ""
        command = ""
        with open(self.filename) as ninja_file:
            for line in ninja_file:
                rule_match = RULE_PATTERN.match(line)
                if rule_match:
                    rule_name = rule_match.group(1)
                    if command != "" and file != "":
                    # we can append last compdb records, when we encounter a new rule
                        self.compdb.append({
                            'directory': self.directory,
                            'arguments': command.split(),
                            "file": file
                        })
                    command = ""
                    file = ""
                    continue

                description_match = DESCRIPTION_PATTERN.match(line)
                if description_match:
                    module_name = description_match.group('module')

                    description_c_match = DESCRIPTION_C_THUMB_PATTERN.match(line)
                    if not description_c_match:
                        description_c_match = DESCRIPTION_C_ARM_PATTERN.match(line)

                    if description_c_match:
                        file = description_c_match.group("file")
                    cur_module = module_name
                    continue

                command_match = COMMAND_PATTERN.match(line)
                if command_match:
                    if file != "":
                        # only command after c pattern could be clang/clang++ command
                        # parser_command will check again
                        command = self.parse_command(command_match.group("args"))
                    continue

        with open(os.path.join(self.outpath, 'compile_commands.json'), 'w') as compdb_file:
            json.dump(self.compdb, compdb_file, indent=1)

def main():
    parser = argparse.ArgumentParser(description='Generate compile_commands.json for AOSP')
    android_build_top = os.getenv('ANDROID_BUILD_TOP')

    if android_build_top:
        parser.add_argument('-r', '--root', nargs='?', default=android_build_top, help='the root dir of aosp')
    else:
        parser.add_argument('-r', '--root', help='the root dir of aosp')

    target_product = os.getenv('TARGET_PRODUCT')
    if target_product:
        parser.add_argument('--ninja_file', nargs='?', default='out/build-{}.ninja'.format(target_product))
    else:
        parser.add_argument('--ninja_file', help='ninja file to paser, it will generate compile_commands.json')
    
    parser.add_argument('-m', '--modules', nargs='+')
    
    parser.add_argument('-f', '--files', nargs='+')

    parser.add_argument("-d", "--dir", nargs=1, help="which directory you want to generate compile_commands, must relative dir with root")

    parser.add_argument("-o", "--out_path", nargs="?", default="")

    args = parser.parse_args()


    if args.ninja_file is None:
        exit(1, 'no ninja_file is specified')

    targetn = 0
    if args.modules is not None:
        targetn += 1
    if args.files is not None:
        targetn += 1
    if args.dir is not None:
        targetn += 1

    if targetn > 1:
        exit(1, 'modules or files or dir should not co-exist, only one can be specified')

    ninja_handle = NinjaHandle(args.ninja_file, args.root, args.out_path)

    if args.modules is not None:
        module_sets = set(args.modules)
        if len(module_sets) > 0:
            ninja_handle.gen_compile_commands_for_modules(module_sets)

    if args.files is not None:
        file_sets = set(args.files)
        if len(file_sets) > 0:
            ninja_handle.gen_compile_commands_for_files(file_sets)
            
    if args.dir is not None:
        directory = args.dir[0]
        ninja_handle.gen_compile_commands_for_directory(directory)

    if args.modules is None and args.files is None and args.dir is None:
        ninja_handle.gen_all_for_ninja()

if __name__ == "__main__":
    main()
