#coding:utf-8

import sys
from collections import defaultdict
from export_data import *

def export_county():
    logging.info('query attrs...')
    sql = 'select attr_name,attr_of_total,attr_value,page_id from attr'
    query_op = dbop()
    cursor = query_op.query_database(sql)
    pid_attrs = defaultdict(list)
    for row in cursor:
        attr_name,attr_of_total,attr_value,page_id = row
        pid_attrs[page_id].append([attr_name,attr_of_total,attr_value])

    ##读取page的表， # 每一个page对应的attrs
    logging.info('query pages...')
    sql = 'select id,keywords,data_id from page'
    pages = defaultdict(list)
    for pid,keywords,data_id in query_op.query_database(sql):
        # did_pages[data_id].append(keywords)
        attrs = pid_attrs[pid]
        for attr in attrs:
            attr.append(keywords)
            pages[pid].append(attr)

    ## 读取state 以及 county msa的数据
    logging.info('query county msa...')
    sql = 'select id,name from state'
    sid_name = {}
    for sid,name in query_op.query_database(sql):
        sid_name[sid] = name

    ## 读取 county 以及msa
    county_info = {}
    sql = 'select id,name,state_id from country'
    for mid,name,state_id in query_op.query_database(sql):
        state_name = sid_name[state_id]
        county_info[mid] = [name,state_name]

    msa_info = {}
    sql = 'select id,name,state_id from msa'
    for mid,name,state_id in query_op.query_database(sql):
        state_name = sid_name[state_id]
        msa_info[mid] = [name,state_name]

    logging.info('size of county:{:}'.format(len(county_info)))
    logging.info('size of msa:{:}'.format(len(msa_info)))

    ## 读取data piece
    logging.info('query county datapiece ...')
    data = []

    sql = 'select year,businessall_id,businessnoncommercial_id,businessnonresident_id,businessresident_id,country_id,gained_id,jobs_id,lost_id,msa_id,netchange_id,saleall_id,salesperbusiness_id,salesperemployee_id,state_id from datapiece'
    for row in query_op.query_database(sql):
        year,businessall_id,businessnoncommercial_id,businessnonresident_id,businessresident_id,country_id,gained_id,jobs_id,lost_id,msa_id,netchange_id,saleall_id,salesperbusiness_id,salesperemployee_id,state_id = row
        ## 年份
        lines =[str(year)]
        ## county or
        if country_id is not None:
            lines.extend(county_info[country_id])
            lines.append('county')
        else:
            lines.extend(msa_info[country_id])
            lines.append('MSA')

        businessall=pages[businessall_id]
        businessnoncommercial=pages[businessnoncommercial_id]
        businessnonresident=pages[businessnonresident_id]
        businessresident=pages[businessresident_id]
        gained=pages[gained_id]
        jobs=pages[jobs_id]
        lost=pages[lost_id]
        netchange=pages[netchange_id]
        saleall=pages[saleall_id]
        salesperbusiness=pages[salesperbusiness_id]
        salesperemployee=pages[salesperemployee_id]
        lines.extend(all_attrs(businessall))
        lines.extend(all_attrs(businessnoncommercial))
        lines.extend(all_attrs(businessnonresident))
        lines.extend(all_attrs(businessresident))
        lines.extend(all_attrs(gained))
        lines.extend(all_attrs(jobs))
        lines.extend(all_attrs(lost))
        lines.extend(all_attrs(netchange))
        lines.extend(all_attrs(saleall))
        lines.extend(all_attrs(salesperbusiness))
        lines.extend(all_attrs(salesperemployee))
        data.add('\t'.join(lines))

    open('data.txt','w').write('\n'.join(data))



def all_attrs(pages):
    col=[]
    for attr in pages:
        col.extend(attr)
    return col






def output_csv(path):
    samples=[]
    for line in open(path):
        ld = {}
        line = line.strip()
        cs = []
        splits = line.split("===")
        # print len(splits)
        # cols=[]
        for l in splits[:-1]:
            ss = l.split(":")
            col=':'.join(ss[:-1])
            ld[col] = ss[-1]
            cs.append(col)

        samples.append(ld)
        
    # print 'length of samples',len(samples)
    cols=[]
    for ld in samples:
        # print len(ld.keys()),len(set(ld.keys()))
        cols.extend(ld.keys())

    cols = sorted(list(set(cols)),reverse=True)
    
    print '\t'.join(cols)
    for ld in samples:
        vs = []
        for col in cols:
            vs.append(ld[col])

        print '\t'.join(vs)

def test_cols(path):
    for line in open(path):
        line = line.strip()
        if len(line.split("\t"))!=96:
            print 'false'

def wrong_place(path):
    place_year=defaultdict(list)
    f = open(path)
    f.readline()
    for line in f:
        line = line.strip()
        splits = line.split("\t")
        year = int(splits[0])
        place = splits[2]
        place_year[place].append(year)

    yearset = set(range(1999,2017))

    for place in place_year.keys():
        if len(yearset - set(place_year[place]))!=0:
            print place,yearset - set(place_year[place])




if __name__ == '__main__':
    # output_csv(sys.argv[1])
    # test_cols('County_checked.txt')
    # wrong_place('County_checked.txt')
    export_county()


