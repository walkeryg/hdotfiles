#!/usr/bin"python3"

import json
import os
import subprocess
import argparse
import re

GCC_PROCESS_HEADER_CMD = "gcc -M"
GCC_PROCESS_ERROR_HEADER_PATTEN = r'.* fatal error: (.*): No such .*'

RTK_ATV_COMMON_PATH = "vendor/realtek/common/ATV"
RTK_FRAMEWORKS_PATH = "vendor/realtek/common/ATV/frameworks"
RTK_FRAMEWORKS_AV_PATH = RTK_FRAMEWORKS_PATH + "/av"
RTK_FRAMEWORKS_NATIVE_PATH = RTK_FRAMEWORKS_PATH + "/native"
RTK_FRAMEWORKS_LIBS_PATH = RTK_FRAMEWORKS_NATIVE_PATH + "/libs"
RTK_FRAMEWORKS_KADP_PATH = RTK_FRAMEWORKS_NATIVE_PATH + "/rtkhal/hal_src/libkadaptor"
RTK_FRAMEWORKS_HAL_PATH = RTK_FRAMEWORKS_NATIVE_PATH + "/rtkhal"
RTK_FRAMEWORKS_CUSTOMERHAL_HS_PATH = RTK_FRAMEWORKS_NATIVE_PATH + "/customerHAL_HS"
RTK_FRAMEWORKS_HALEX_PATH = RTK_FRAMEWORKS_NATIVE_PATH + "/rtkhal/halex"
RTK_FRAMEWORKS_APPCLASS_PATH = RTK_FRAMEWORKS_NATIVE_PATH + "/appclass"
RTK_FRAMEWORKS_SERVICE_PATH = RTK_FRAMEWORKS_NATIVE_PATH + "/services"
RTK_FRAMEWORKS_COMMON_PATH = RTK_FRAMEWORKS_LIBS_PATH + "/common"
RTK_FRAMEWORKS_THIRD_PARTY_PATH = RTK_FRAMEWORKS_LIBS_PATH + "/third_party"
RTK_FRAMEWORKS_CI_PATH = RTK_FRAMEWORKS_NATIVE_PATH + "/third_party/CommonInterface"
RTK_HARDWARE_PATH = RTK_ATV_COMMON_PATH + "/hardware"
RTK_FRAMEWORKS_AV_INCLUDE = RTK_FRAMEWORKS_AV_PATH + "/include/media"
RTK_FRAMEWORKS_NATIVE_INCLUDE = RTK_FRAMEWORKS_NATIVE_PATH + "/include"
RTK_FRAMEWORKS_LIBS_INCLUDE = RTK_FRAMEWORKS_NATIVE_PATH + "/include/libs"
RTK_FRAMEWORKS_UTILS_INCLUDE = RTK_FRAMEWORKS_NATIVE_PATH + "/include/utils"
RTK_FRAMEWORKS_KADP_INCLUDE = RTK_FRAMEWORKS_KADP_PATH + "/inc"
RTK_FRAMEWORKS_CUSTOMERHAL_HS_INCLUDE = RTK_FRAMEWORKS_CUSTOMERHAL_HS_PATH + "/include/include_hs"
RTK_FRAMEWORKS_APPCLASS_INCLUDE = RTK_FRAMEWORKS_NATIVE_PATH + "/include/appclass"
RTK_FRAMEWORKS_SERVICE_INCLUDE = RTK_FRAMEWORKS_NATIVE_PATH + "/include/services"
RTK_FRAMEWORKS_CI_INCLUDE = RTK_FRAMEWORKS_CI_PATH + "/include"
RTK_FRAMEWORKS_EXT_INCLUDE = RTK_FRAMEWORKS_PATH + "/native/ExtTv/include"
RTK_FRAMEWORKS_VERSION_INCLUDE = RTK_FRAMEWORKS_PATH + "/configs/version"
RTK_FRAMEWORKS_HAL_INCLUDE = [RTK_FRAMEWORKS_HAL_PATH, RTK_FRAMEWORKS_HAL_PATH + "/hal_inc", RTK_FRAMEWORKS_HAL_PATH + "/hal_src/hal", RTK_FRAMEWORKS_HAL_PATH + "/hal_src/hal/inc", RTK_FRAMEWORKS_HAL_PATH + "/rhal_tvfe/inc"]
RTK_FRAMEWORKS_RTKUTILITY_INCLUDE = RTK_FRAMEWORKS_HAL_PATH + "/rtkutility/inc"
RTK_FRAMEWORKS_HALEX_INCLUDE = RTK_FRAMEWORKS_HALEX_PATH + "/inc"
RTK_FRAMEWORKS_COMMON_INCLUDE = [RTK_FRAMEWORKS_COMMON_PATH, RTK_FRAMEWORKS_COMMON_PATH + "/include", RTK_FRAMEWORKS_COMMON_PATH + "/IPC/include", RTK_FRAMEWORKS_COMMON_PATH + "/IPC/generate/include/system"]

def append_includes(dirs: list, newdirs):
    if isinstance(newdirs, list):
        for d in newdirs:
            dirs.append(d)
    else:
        dirs.append(newdirs)
    return dirs

def get_pre_include_rtk_dirs():
    dirs = []
    dirs = append_includes(dirs, RTK_ATV_COMMON_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_AV_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_NATIVE_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_LIBS_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_KADP_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_HAL_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_CUSTOMERHAL_HS_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_HALEX_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_APPCLASS_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_SERVICE_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_COMMON_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_THIRD_PARTY_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_CI_PATH)
    dirs = append_includes(dirs, RTK_HARDWARE_PATH)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_AV_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_NATIVE_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_LIBS_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_UTILS_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_KADP_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_CUSTOMERHAL_HS_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_APPCLASS_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_SERVICE_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_CI_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_EXT_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_VERSION_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_HAL_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_RTKUTILITY_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_HALEX_INCLUDE)
    dirs = append_includes(dirs, RTK_FRAMEWORKS_COMMON_INCLUDE)
    return dirs

# gcc -M AudioUtil.cpp will only found headers in "" until error
# gcc -MM AudioUtil.cpp will found all headers including system in <> until error 
class HeaderHelper(object):
    def __init__(self, target_cfile, root_path, filelist_pattern, extra_inc_params):
        self.target_cfile = target_cfile
        self.root_path = root_path
        self.filelist_pattern = filelist_pattern
        self.find_cmd_prefix = 'cat '
        self.find_cmd_prefix = self.find_cmd_prefix + self.root_path + "/" + self.filelist_pattern
        self.find_cmd_prefix = self.find_cmd_prefix + ' | '
        self.find_cmd_prefix = self.find_cmd_prefix + ' grep '
        self.incdir_list = []
        for inc in extra_inc_params:
            self.incdir_list.append(inc)
        self.incdir_list = self.incdir_list + get_pre_include_rtk_dirs()

    def init(self):
        # TODO: generate filelist if not exist
        pass 

    def _do_compile(self, cmd:str, newparms:str):
        cmd = cmd + newparms
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
        out, err = proc.communicate()

        if proc.returncode != 0:
            seachobj = re.search(GCC_PROCESS_ERROR_HEADER_PATTEN, err)
            header = seachobj.group(1)
            return proc.returncode, header
        else:
            return proc.returncode, None

    def _find_include_path(self, header:str):
        find_cmd = self.find_cmd_prefix + header
        proc = subprocess.Popen(find_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
        out, err = proc.communicate() 

        # not found
        if proc.returncode != 0:
            return proc.returncode, []
        else:
            out_list = out.strip().split('\n')
            dir_list = []
            for l in out_list:
                dir_list.append(l.replace('/'+header,''))
            return proc.returncode, dir_list

    def find_all_include_path(self):

        cmd = GCC_PROCESS_HEADER_CMD + " " + self.target_cfile
        extra_inc_params = "" 
        for d in self.incdir_list: 
            extra_inc_params = extra_inc_params + " -I" + self.root_path + "/" + d 

        compile_ret, inc = self._do_compile(cmd, extra_inc_params)
        while compile_ret != 0:
            find_ret, cand_list = self._find_include_path(inc)
            if find_ret != 0:
                print("cound not found " + inc)
                break
            else:
                if len(cand_list) > 1:
                    print("too many same names for " + inc)
                    print("You could specifiled with cmd parameters again with the flowing paths:")
                    for d in cand_list:
                        if cand_list[0].startswith("./"):
                            print(d[2:])
                        else:
                            print(d)
                    break
                else:
                    if cand_list[0].startswith("./"):
                        extra_inc_params = extra_inc_params + " -I" + self.root_path + cand_list[0][2:]
                        self.incdir_list.append(cand_list[0][2:])
                    else:
                        extra_inc_params = extra_inc_params + " -I" + self.root_path + cand_list[0]
                        self.incdir_list.append(cand_list[0])
                    compile_ret, inc = self._do_compile(cmd, extra_inc_params)
        print("Already found includes:")
        for d in self.incdir_list:
            print(d)
def main():

    parse = argparse.ArgumentParser(description="Process input args")
    parse.add_argument("-f", action='store', dest='cfile', default='', help='c files to found include dirs')
    parse.add_argument("-r", action='store', dest='root_path', default='', help='android root path')
    parse.add_argument("-e", action="store", dest='extra_params', default='', nargs='+', help='extra include path already known')

    results = parse.parse_args()
    if results.cfile == '':
        print("Please input c file -f")
        return
    
    if results.root_path == '':
        print("Please input the absolute android root path with -r") 
        return

    helper = HeaderHelper(results.cfile, results.root_path, "filelist", results.extra_params)
    helper.init()
    helper.find_all_include_path()

if __name__ == '__main__':
    main()
