#coding:utf-8
import urllib2
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.DEBUG)
from bs4 import BeautifulSoup
from collections import defaultdict
import time
import json

KEYS=['all-businesses','resident-businesses','nonresident-businesses','noncommercial-businesses','All-Jobs','Total-Gained','Total-Lost','change','All-Sales','Sales-Per-Employee','Sales-Per-Establishment']



def crawl_county_year(state,t1,t2,county_id,key):

    url = 'http://youreconomy.org/profile/details.ye?type=e&key={:}&state={:}&year1={:}&year2={:}&county={:}&custom=undefined'.format(key,state,t1,t2,county_id)
    logging.info('crawling url:{:}'.format(url))
    try:
        response = urllib2.urlopen(url)
    except:
        # print 'error'
        return None

    html = response.read()
    return html

def parse_first_year(html):
    soup = BeautifulSoup(html,'lxml')
    attr_dict = defaultdict(dict)
    for tr in soup.select('tr'):
        tds = tr.select('td')
        if len(tds)==0:
            continue
        td_strs = []
        for td in tds:
            if td.string is None:
                continue
            td_strs.append(td.string.strip()) 

        if len(td_strs)==0:
            continue
        attr,value,percent = td_strs[:3]
        attr_dict[attr]['attr_value']=value
        attr_dict[attr]['attr_of_total']=percent


    return attr_dict

def parse_second_year(html):
    soup = BeautifulSoup(html,'lxml')
    attr_dict = defaultdict(dict)
    for tr in soup.select('tr'):
        tds = tr.select('td')
        if len(tds)==0:
            continue
        td_strs = []
        for td in tds:
            if td.string is None:
                continue
            td_strs.append(td.string.strip()) 

        if len(td_strs)==0:
            continue
        attr = td_strs[0]
        value = td_strs[3]
        percent = td_strs[4]
        attr_dict[attr]['attr_value']=value
        attr_dict[attr]['attr_of_total']=percent

    return attr_dict


def crawl_all_keys(state,t1,t2,county_id,isfirst=True):
    key_attrs={}
    for key in KEYS:
        html = crawl_county_year(state,t1,t2,county_id,key)


        if html is None:
            attr_dict=None
        else:
            if isfirst:
                year = t1
                attr_dict = parse_first_year(html)

            else:
                year = t2
                attr_dict = parse_second_year(html)
        key_attrs[key] = attr_dict

    return key_attrs




def crawl_all_missing_data(path):
    county_year_key_attrs = defaultdict(dict)
    progress = 0
    for line in open(path):
        progress+=1
        time.sleep(2)

        print 'progress:',progress

        line = line.strip()
        state_value,county,county_id,year = line.split('\t')

        if year=='2016':
            t1 = '2015'
            t2 = '2016'
            isfirst = False
        else:
            t1 = year
            t2 = '2016'
            isfirst = True
        
        key_attrs = crawl_all_keys(state_value,t1,t2,county_id,isfirst)
        county_year_key_attrs[county][year]=key_attrs

    open('../county_year_key_attrs.json','w').write(json.dumps(county_year_key_attrs))


if __name__ == '__main__':
    crawl_all_missing_data('../missing_county.txt')

