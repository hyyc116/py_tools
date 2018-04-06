#coding:utf-8
import urllib2
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.DEBUG)
from bs4 import BeautifulSoup
from collections import defaultdict
import time
import json


def output_file():
    col_tits = open('../county_columns_checked.txt').readline().strip().split("\t")
    county_year_key_attrs = json.loads(open('../county_year_key_attrs.json').read())
    # print col_tits

    name_state = {}
    for line in open('../missing_county.txt'):
        line = line.strip()
        splits = line.split("\t")
        name_state[splits[1]] = splits[0]

    for name in county_year_key_attrs.keys():
        for year in county_year_key_attrs[name].keys():
            key_attrs = county_year_key_attrs[name][year]

            all_vals = []
            all_vals.append(year)
            all_vals.append(name)
            all_vals.append(name_state[name])
            all_vals.append('County')
            vals=[]
            for tit in col_tits:
                if ':' in tit:
                    if tit.startswith('non-commercial'):
                        tit = tit.replace('non-commercial','noncommercial-businesses')

                    key,attr,t = tit.split(":")


                    attr_dict = key_attrs[key]
                    if attr_dict is None:
                        ## 如果是空的话 也要返回空
                        vals.append('NA')

                    else:
                        vals.append(attr_dict[attr][t])

            if ','.join(vals) != ','.join(['NA']*192):
                # print vals
                # print len(vals)
                all_vals.extend(vals)
                print '\t'.join(all_vals)

if __name__ == '__main__':
    output_file()

