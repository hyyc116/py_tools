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

def check_un_crawled():
    news=[]
    for line in open('../data_new.txt'):
        line = line.strip()
        splits = line.split('\t')
        news.append('{:}\t{:}'.format(splits[1],splits[0]))
    news = set(news)

    for line in open("../errors.txt"):
        line = line.strip()
        splits = line.split("\t")
        name = splits[1]
        years = splits[2:]
        not_in = []
        for year in years:
            if '{:}\t{:}'.format(name,year) not in news:
                not_in.append(year)

        if len(not_in)>0:
            print splits[0]+"\t"+name+"\t"+str(not_in)






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


def two_data(path):
    county_set=[]
    msa_set=[]
    counties = [] 
    msas = []

    for line in open(path):
        line = line.strip()
        splits = line.split("\t")
        name = splits[1]
        atype = splits[3]
        if atype=='county':
            counties.append(line)
            county_set.append(name)
        else:
            msas.append(line)
            msa_set.append(name)

    print 'county',len(set(county_set))
    print 'msa',len(set(msa_set))
    open('county_content.txt','w').write('\n'.join(counties))
    open('msa_content.txt','w').write('\n'.join(msas))




if __name__ == '__main__':
    # test_cols(sys.argv[1])
    # wrong_place(sys.argv[1])
    # out_check()
    # two_data(sys.argv[1])
    check_un_crawled()


