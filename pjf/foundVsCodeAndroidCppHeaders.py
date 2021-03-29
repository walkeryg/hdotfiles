#!/usr/bin/python3

import json
import os

MODULE = "librtk_omx_vdec"
MODUE_INFO_JSON = 'module-info.json'

if __name__ == '__main__':
    target = MODULE
    with open(MODUE_INFO_JSON) as f:
        all_mod = json.load(f)
        module = all_mod.get(MODULE)
        dependency = module.get("dependencies")
        for l in dependency:
            print(l)
