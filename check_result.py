#coding:utf-8
import sys
from collections import defaultdict
from export_data import *

def test_cols(path):
    for line in open(path):
        line = line.strip()
        splits = line.split("\t")
        length= len(splits)
        ## 长度是196 入股
        if length!=196:
            print line
            # print line
        # if length >4 and splits[3]=='MSA':

        #     print line
            
        # if len(line.split("\t"))!=96:
        #     print 'false'

def wrong_place(path):
    place_year=defaultdict(list)
    f = open(path)
    f.readline()
    for line in f:
        line = line.strip()
        splits = line.split("\t")
        year = int(splits[0])
        place = splits[1]
        place_year[place].append(year)

    # yearset = set(range(1999,2017))

    for place in place_year.keys():
        # if len(yearset - set(place_year[place]))!=0:
            # print place,yearset - set(place_year[place])
        print place+"\t"+place_year[place]

if __name__ == '__main__':
    # test_cols(sys.argv[1])
    wrong_place(sys.argv[1])


