import os
import re
import stat
import subprocess
import sys

def _print(*objects, **kwargs):
    sep = kwargs.get('sep',' ')
    end = kwargs.get('end', '\n')
    out = kwargs.get('file', sys.stdout)
    out.write(sep.join(objects) + end)

def _FindProjectRc():
    return "Unknown"

def main(args):
    project_rc = _FindProjectRc()
    _print('ProjectRc is at %s' % project_rc)

if __name__ == '__main__':
    main(sys.argv[1:])
