#coding:utf-8
import sys
from collections import defaultdict
from export_data import *

## check the length of county_modified.txt

def check_cols(path):
    for i,line in enumerate(open(path)):

        line = line.strip()
        
        if i==0:
            print line

        splits = line.split("\t")
        # print len(splits)
        if len(splits)!=196:
            print line


if __name__ == '__main__':
    check_cols(sys.argv[1])
    