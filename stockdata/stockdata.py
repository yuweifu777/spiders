# -*- coding: utf-8 -*-
import re
import json
import time
import requests
import pymongo
import datetime
import pandas as pd
from random import randint
from threading import Thread


def __code_to_symbol(code):
    code = code
    return 'sh%s' % code if code[0] in ['5', '6', '9'] else 'sz%s' % code


def __random(n):
    start = 10 ** (n - 1)
    end = (10 ** n) - 1
    return str(randint(start, end))


def todt(str_dt):
    return datetime.datetime.strptime(str_dt, '%Y-%m-%d')


def update_dt(d):
    d.update({u'date': todt(d['tradedate'])})


# main function: return history data
def get_data(code='', start='', end=''):
    symbol = __code_to_symbol(code)
    url = 'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param={},day,{},{},640,qfq&r=0.{}' \
        .format(symbol, start, end, __random(17))
    for _ in range(5):
        try:
            resp = requests.get(url)
            lines = resp.text.split('=')[1]
            reg = re.compile(r',{"nd.*?}')
            lines = re.subn(reg, '', lines)
            js = json.loads(lines[0])
            dataflag = 'qfqday' if 'qfqday' in list(js['data'][symbol].keys()) else 'day'
            df = pd.DataFrame(js['data'][symbol][dataflag],
                              columns=['tradedate', 'open', 'close', 'high', 'low', 'volumn'])
            return df
        except Exception, e:
            print '[API]: Bad request.' + str(e)
            print 'url is: ', url
            time.sleep(2)


def drudgery(ids, db, start, end, tasks):
    if len(tasks) == 0:
        return 0
    no_k = 1
    n = len(tasks)
    for ticker in tasks:
        try:
            data = get_data(code=ticker, start=start, end=end)  # dataframe
            data = data.T.to_dict().values()  # list of dictionaries
            map(update_dt, data)
            coll = db[ticker]  # collection: ticker = '000002'
            coll.insert_many(data)
            coll.create_index("tradedate", unique=True)
            print '[API|Session{}]: '.format(ids) + 'Finished {} in {}.'.format(no_k, n)
            no_k += 1
        except Exception, e:
            msg = '[API|Session{}]: '.format(ids) + \
                  'Exception encountered when ' + \
                  'requesting data; ' + str(e)
            print 'Check if suspended: ', ticker
            print msg
            pass


def overload(db, start, end):
    # load all tickers
    jsonfile = open('equTicker.json', 'r')
    alltickers = json.loads(jsonfile.read())
    jsonfile.close()
    # multithread number
    sessionnum = 30
    chunksize = len(alltickers) / sessionnum
    tasklists = [alltickers[k:k + chunksize] for k in range(0, len(alltickers), chunksize)]
    k = 0
    for tasks in tasklists:
        thrd = Thread(target=drudgery, args=(k, db, start, end, tasks))
        thrd.start()
        k += 1
    return 1


def download_all(start, end):
    client = pymongo.MongoClient()
    data_db = client['tickerdata']
    overload(data_db, start, end)


def download_one(code, start, end):
    client = pymongo.MongoClient()
    db = client['tickerdata']
    data = get_data(code, start, end)
    data = data.T.to_dict().values()
    try:
        db[code].insert_many(data)
        db[code].create_index("tradedate", unique=True)
    except Exception, e:
        print str(e) + ': data already exists'
        pass


# download one security's data
# download_one('000002', '2016-01-01', '2016-10-01')

# down load for all tickers in equTicker.json
download_all('2016-11-10', '2016-11-17')
