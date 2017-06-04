import os
import optparse
import platform
import re
import sys
import subprocess

class Tag(object):
    """Base Class for Gen/Update Tags"""

    def __init__(self):
        self.__ignore = [
            '.*o',
        ]
    def Usage(self):
        print("NotImplemented")
        sys.exit(1)

    def update(self):
        raise NotImplementedError

    def _kill(sef, proc_pid):
        process = psutil.Process(proc_pid)
        for proc in process.children():
            proc.kill()
        process.kill()

