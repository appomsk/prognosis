#!/usr/bin/python3
import sys
import re
import os
import datetime
import requests
import pandas as pd

import config as cfg

def mining(content):
    active_title = '(Number of Infected People)'
    active_title2 = 'Active Cases'
    cases_title = 'Total Cases'
    deaths_title = 'Total Deaths'
    titles = (active_title, active_title2, cases_title, deaths_title)
    names = {active_title: cfg.active, active_title2: cfg.active,
                        cases_title: cfg.cases, deaths_title: cfg.deaths}

    content = re.sub('\n', '', content)
    content = re.sub("'", '"', content)
    flags = re.DOTALL | re.VERBOSE
    chunkpattern = r'''
        Highcharts.chart[^;]*;
    '''
    chunks = re.findall(chunkpattern, content, flags)

    flags = re.VERBOSE
    datapattern = r'''
        title:.*?text:\s*"(.*?)"
        .*?
        xAxis[^\[]+\[(.*?)]
        .*?
        data:\s*\[(.*?)]
    '''
    s = set()
    for chunk in chunks:
        t = re.findall(datapattern, chunk, flags)
        if t and len(t[0]) == 3:
            s.add(t[0])

    rst = {}
    for it in s:
        if it[0] not in titles:
            continue
        title = it[0]
        if title == cases_title:
            s = re.sub('["]', '', it[1])
            rst[cfg.dates] = []
            for d in s.split(','):
                t = datetime.datetime.strptime("2020" + d, "%Y%b %d")
                t = str(datetime.date(t.year, t.month, t.day))
                rst[cfg.dates].append(t)
        rst[names[title]] = map(int, it[2].split(','))

    df = pd.DataFrame(rst)

# and active cases and recovered are very unreliable
#    recovered = []
#    for i in range(len(df)):
#        recovered.append(df[names[cases_title]][i] - df[names[active_title]][i] -
#                         df[names[deaths_title]][i])
#
#    df[recovered_name] = recovered
    df = df[cfg.fetcheddf_order]

    return df

def filepath(url):
    datadir = cfg.datadir
    d = os.path.dirname(os.path.realpath(__file__))
    d = os.path.join(d, datadir)
    if not os.path.exists(d):
        os.mkdir(d)

    date = str(datetime.date.today())

    t = re.search(r'/country/(.*)/$', url)
    country = t[1] if t else 'world'

    path = os.path.join(d, date + '-' + country)
    return path

def save(path, df):
    s = df.to_csv(index=False)
    with open(path, 'w') as fd:
        fd.write(s)

def fetch_all():
    """ Save all data to datadir """
    # ignore returned df-s
    for url in cfg.urls:
        fetch(url)

def get_url(s=""):
    """ Get url from url, country or empty (then 'world') """
    r = None
    if s.startswith('https://'): 
        r = s
    elif s == "" or s == 'world':
        r = cfg.world_url
    else:
        r = cfg.prefix_url + s + '/'

    return r

def fetch(smth=""):
    """ fetch dataframe

    smth may be url, country, or empty string (world)
    """
    url = get_url(smth)
    path = filepath(url)
    r = None
    if os.path.exists(path):
        r = pd.read_csv(path)
    else:
        raw = requests.get(url).text
        r = mining(raw)
        save(filepath(url), r)
    return r

if __name__ == '__main__':
    if len(sys.argv) == 1:
        fetch_all()
    else:
        print(fetch(sys.argv[1]).to_markdown())
