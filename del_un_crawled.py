#coding:utf-8
from export_data import *

def del_data():
    msas = set([line.strip() for line in open('msa_crawled.txt')])
    counties = set([line.strip() for line in open('county_crawled.txt')])
    query_op = dbop()
    del_op = dbop()
    sql = 'select id,name from msa'
    count=0
    for mid,name in query_op.query_database(sql):
        if name not in msas:
            del_op.execute_sql('update datapiece set msa_id = -1 where msa_id={:}'.format(mid))
            count+=1
            print count 

    sql = 'select id,name from country'
    count=0
    for mid,name in query_op.query_database(sql):
        if name not in msas:
            del_op.execute_sql('update datapiece set msa_id = -1 where country_id={:}'.format(mid))
            count+=1
            print count 

if __name__ == '__main__':
    del_data()

