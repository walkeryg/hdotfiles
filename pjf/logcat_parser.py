#!/bin/python3

import re


def main():

    infilename = '../README.md'
    outfilename = 'log.output'
    m1 = r'.*dot'
    idx = 0
    before = 0
    after = 0

    with open(infilename, 'r') as infile:
        for line in infile:
            if (re.match(m1, line, flags=0)):
                print(line)
                strlist = line.split(' ')
                before = int(strlist[idx])
                print(strlist)
                if (before > 0 and after > 0):
                    print('diff -> %d' % before - after)
                after = before


if __name__ == '__main__':
    main()
