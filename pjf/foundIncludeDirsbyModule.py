#!/usr/bin"python3"

import json
import os
import subprocess
import argparse
import re

MODULE = "librtk_omx_vdec"
MODUE_INFO_JSON = 'module-info.json'
PREFIX = "/home/walker_yang/WorkShop/realtek/hisense/android-10"
SOONG = "out/soong/.intermediates"
SOONG_HEADER_SUFFIX = "_genc++_headers"
HARDWARE_PATTEN = "android.hardware."
VENDOR_HARDWARE_PATTEN = "vendor.realtek."

class ModuleHelper(object):
    def __init__(self, module_info_json, prefix):
        self.module_info_json = module_info_json
        self.prefix = prefix 
    
    def init(self):
        with open(self.module_info_json) as f:
            self.all_mod = json.load(f)

    def find_dependency(self, target: str):
        module = self.all_mod.get(target)
        dependency = module.get("dependencies")
        return dependency
    
    def find_path(self, target: str):
        module = self.all_mod.get(target)
        path = module.get("path")[0]
        realpath = os.path.join(self.prefix, path)
        if os.path.exists(realpath):
            return realpath
        else:
            return ""

    def find_soong_include_path(self, target: str):
        module = self.all_mod.get(target)
        path = module.get("path")[0]
        realpath = os.path.join(self.prefix, SOONG, path)
        bfind = False
        header_include = os.path.join(realpath, target + SOONG_HEADER_SUFFIX)
        if os.path.exists(header_include):
            bfind = True
            return header_include
        return ""

    def find_include_path(self, target: str):
        module = self.all_mod.get(target)
        path = module.get("path")[0]
        realpath = os.path.join(self.prefix, path)
        bfind = False
        header_include = os.path.join(realpath, "include")
        if os.path.exists(header_include):
            bfind = True
        else:
            # found like libhidlbase -> libhidl/base
            basename = os.path.basename(path)
            idx = target.find(basename)
            if idx >= 0:
                cand = target[idx + len(basename):]
                header_include = os.path.join(realpath, cand, "include")
                if os.path.exists(header_include):
                    bfind = True
        
        # TODO: need parse Android.mk to get LOCAL_EXPORT_C_INCLUDE_DIRS or Android.bp to get export_include_dirs & LOCAL_C_INCLUDES

        if not bfind:
            clas = module.get("class")[0]
            if clas == 'HEADER_LIBRARIES':
                header_include = os.path.join(realpath, "include") 
                if os.path.exists(header_include):
                    bfind = True
                else:
                    header_include = realpath
                    bfind = True
        if bfind:
            # print("found " + header_include)
            return header_include
        else:
            # print("not found for " + target)
            return ""



def main():
    parse = argparse.ArgumentParser(description="Process input args")
    parse.add_argument("-m", action='store', dest='module', default='', help='module to resolve headers')
    parse.add_argument("-p", action='store', dest='path_prefix', default='', help='android root path')
    parse.add_argument("-f", action="store", dest='module_info', default='', help='set module_info.json')

    results = parse.parse_args()
    if results.module_info == '':
        print("Please input module_info.json with -f")
        return
    
    if results.module == '':
        print("Please input which module to found header include with -m") 
        return
    if results.path_prefix == '':
        print("Please input the absolute android root path with -m") 
        return

    helper = ModuleHelper(results.module_info, results.path_prefix)
    helper.init()
    target = results.module
    header_list = []
    dependency = helper.find_dependency(target)
    for l in dependency:
        if l.startswith(HARDWARE_PATTEN) or l.startswith(VENDOR_HARDWARE_PATTEN):
            header_inc = helper.find_soong_include_path(l)
        else:
            header_inc = helper.find_include_path(l)
        if not header_inc == "":
            header_list.append(header_inc)
    
    for inc in header_list:
        print(inc)

if __name__ == '__main__':
    main()
