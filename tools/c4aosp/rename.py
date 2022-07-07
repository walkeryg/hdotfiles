#!/usr/bin/python3

import os
import os.path
import shutil
import argparse

def main():
    parser = argparse.ArgumentParser(description='rename files')
    parser.add_argument('--in_pattern', help='the src filename pattern')
    parser.add_argument('--out_pattern', help='the target filename pattern')
    parser.add_argument('--dir', help='the working dir')
    parser.add_argument('--action', help='the working dir')

    args = parser.parse_args()

    if args.dir is None:
        exit("unknown dir to processed") 

    if args.action is None:
        if args.in_pattern is None:
            exit("unknown input pattern")

        if args.out_pattern is None:
            exit("unknown ouput pattern")
    else:
        if args.action == "backup" or args.action == "restore":
            pass
        else:
            exit("action should only be backup or restore")

    if not os.path.exists(args.dir):
        exit("The Dir " + dir + " is not exist")
    
    if args.action == "backup":
        print("rename all Android.bp or Android.mk to Android.bp_bak or Android.mk_bak")
        for root, subdirs, files in os.walk(args.dir):
            for file in files:
                if file == "Android.bp" or file == "Android.mk":
                        shutil.move(os.path.join(root, file), os.path.join(root, file+"_bak"))
    elif args.action == "restore":
        print("rename all Android.bp_bak or Android.mk_bak to Android.bp or Android.mk")
        for root, subdirs, files in os.walk(args.dir):
            for file in files:
                if file == "Android.bp_bak" or file == "Android.mk_bak":
                        shutil.move(os.path.join(root, file), os.path.join(root, file[:-4]))

if __name__ == "__main__":
    main()
