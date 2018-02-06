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

        if "NULL" not in line:
            print line
            # print line
        # if length >4 and splits[3]=='MSA':

        #     print line
            
        # if len(line.split("\t"))!=96:
        #     print 'false'

def out_check():
    year_name_set=set([])
    for line in open("errors.txt"):
        line = line.strip()
        splits = line.split("\t")
        name = splits[1]
        years = splits[2:]
        for year in years:
            year_name_set.add('{:}\t{:}'.format(name,year))

    for line in open('data.txt'):
        line = line.strip()
        splits = line.split('\t')
        if '{:}\t{:}'.format(splits[1],splits[0]) in year_name_set:
            print line




def wrong_place(path):
    atype_place_year=defaultdict(lambda:defaultdict(list))
    f = open(path)
    f.readline()
    for line in f:
        line = line.strip()
        splits = line.split("\t")
        year = int(splits[0])
        place = splits[1]
        atype=splits[3]
        atype_place_year[atype][place].append(year)

    for atype in atype_place_year.keys():
        for place in atype_place_year[atype].keys():
            # if len(place_year[place])==1:
            print atype+"\t"+place+"\t"+"\t".join([str(i) for i in atype_place_year[atype][place]])

if __name__ == '__main__':
    # test_cols(sys.argv[1])
    # wrong_place(sys.argv[1])
    out_check()


