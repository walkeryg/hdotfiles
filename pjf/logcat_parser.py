#!/bin/python3

import re


def main():

    infilename = '../README.md'
    outfilename = 'log.output'
    m1 = r'.*dot'
    idx = [1, 3]
    linecnt = 0
    before = [0 for i in range(len(idx))]
    after = [0 for i in range(len(idx))]
    diff = [0 for i in range(len(idx))]

    with open(infilename, 'r') as infile:
        for line in infile:
            if (re.match(m1, line, flags=0)):
                print(line)
                strlist = line.split(' ')
                if(len(strlist) < max(idx)):
                    print("line is smaller than the max idx")
                    continue
                skip = False
                for i in range(len(idx)):
                    try:
                        after[i] = int(strlist[idx[i]])
                    except ValueError:
                        print("skip this line")
                        skip = True
                        break;
                if(skip):
                    continue
                print(strlist)
                if(linecnt%2):
                    diff = [(after[i] - before[i]) for i in range(len(idx))]
                    print(diff)
                before = after.copy()
                linecnt += 1


if __name__ == '__main__':
    main()
