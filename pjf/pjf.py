FIND = ''
prjrc_conf = 'project.rc'
FZF = 'fzf'
INDEX = 'INDEX'

import os
import os.path
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
    
    curdir = os.getcwd()
    prjrc = None

    olddir = None
    while curdir != '/' \
            and curdir != olddir \
            and not prjrc:
        prjrc = os.path.join(curdir, prjrc_conf)
        if not os.path.isfile(prjrc):
            prjrc = None
            olddir = curdir
            curdir = os.path.dirname(curdir)
    return prjrc

def _ParseProjectDir(project_rc):

    dir_list = []
    with open(project_rc) as f:
        for line in f.readlines():
            if(line.startswith('/')):
                dir_list.append(line.strip())
            else:
                dir_list.append(os.path.join(os.path.dirname(project_rc), line.strip()))
    return dir_list

def _GetIndexFile(project_rc):

    indexfile = None
    if os.path.isfile(project_rc):
        indexfile = os.path.join(os.path.dirname(project_rc), INDEX)
    return indexfile

def _SelectProjectDirFZF(dir_list):

    proc = subprocess.Popen('sh -c fzf -m',
                            shell=True,
                            stdout=subprocess.PIPE
                            )
    fzf_result = proc.stdout.read().strip()
    proc.stdout.close()
    _print('fzf result %s:' %fzf_result)
    # proc.stderr.read()
    # proc.stderr.close()

    if proc.wait() != 0:
        _print('fatal: fzf errors', file=sys.stderr)
        sys.exit(1)

def _SelectProjectFilesFZF(dir_list):

    cmd = ['ag', '-g', '']
    cmd.extend(dir_list)
    print(cmd)
    # proc = subprocess.Popen('ag -g custom',shell=True,stdout=subprocess.PIPE)
    # for line in proc.stdout.readlines():
        # print(line)
    # proc.stdout.close()
    search_proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    fzf_proc = subprocess.Popen(['fzf'],stdin=search_proc.stdout,stdout=subprocess.PIPE)

    fzf_result = fzf_proc.stdout.read().strip()
    fzf_proc.stdout.close()
    _print('fzf result: %s' %fzf_result)
    if fzf_proc.wait() != 0:
        _print('fatal: fzf errors', file=sys.stderr)
        sys.exit(1)

def _IndexProjectFiles(dir_list, indexfile):

    if indexfile is None:
        return

    if dir_list is None:
        return

    idxfile = open(indexfile, 'w')
    cmd = ['ag', '-g', '""']
    cmd.extend(dir_list)
    print(' '.join(cmd))
    proc = subprocess.Popen(' '.join(cmd),shell=True,stdout=subprocess.PIPE)
    for line in proc.stdout.readlines():
        print(line.decode('utf-8').strip())
        idxfile.write(line.decode('utf-8'))
    proc.stdout.close()
    idxfile.close()

def main(args):

    project_rc = _FindProjectRc()
    _print('ProjectRc is at %s' % project_rc)
    dir_list = _ParseProjectDir(project_rc)
    print(dir_list)
    indexfile = _GetIndexFile(project_rc)
    _IndexProjectFiles(dir_list,  indexfile)

if __name__ == '__main__':
    main(sys.argv[1:])
