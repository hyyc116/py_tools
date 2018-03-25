#coding:utf-8
import sys
from collections import defaultdict
from export_data import *

def check_lines():

    sid_value = {}
    for line in open('../state.txt'):
        line = line.strip()
        splits = line.split('\t')
        if line.startswith('id'):
            continue
        sid = splits[0]
        value = splits[2]
        sid_value[sid] = value

    county_attr={}
    for line in open('../counties.txt'):
        line = line.strip()
        if line.startswith('id'):
            continue

        splits = line.split('\t')
        name = splits[2]
        value = splits[3]
        sid = splits[4]
        state_value = sid_value[sid]

        county_attr[name] = [value,state_value]



    counties = set([line.strip().split('\t')[2] for line in open('../counties.txt') if not line.startswith('id')])
    # print 'counties number:',len(counties)


    name_year=defaultdict(list)
    for line in open('../county_columns_checked.txt'):
        line = line.strip()
        if line.startswith('year'):
            continue
        splits = line.split("\t")
        year = splits[0]
        name = splits[1]
        name_year[name].append(year)


    years = set([str(y) for y in range(1998,2017)])
    # print years
    # print len(name_year.keys())

    # print counties-set(name_year.keys())

    for name in counties:
        c_years = set(name_year[name])
        not_int_years = [y for y in list(years-c_years) if int(y)>2000]
        # if len(not_int_years)>0:
            # print name,','.join(not_int_years)

        for year in not_int_years:
            value,state_value = county_attr[name]
            print '{:}\t{:}\t{:}\t{:}'.format(state_value,name,value,year)


if __name__ == '__main__':
    check_lines()
