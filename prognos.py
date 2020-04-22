#!/usr/bin/python3

import sys
import os
import datetime
import math
import getopt
import pandas as pd
import config as cfg
import fetch
import process

def prognos(df, colname, window_size):
    pname = cfg.mkcol_p(colname)
    ppname = cfg.mkcol_pp(colname)
    avename = cfg.mkcol_avepp(colname)
    datename = cfg.dates

    data = {}
    for k in (datename, colname, pname, ppname):
        data[k] = list(df[k][len(df)-window_size:])

    dates = []
    for d in data[datename]:
        dates.append(datetime.date(*map(int, d.split('-'))))
    data[datename] = dates

    # data[ppname][-1] = df.at[len(df)-1, avename]
    colpp = df.at[len(df)-1, avename]

    for i in range(window_size):
        day = data[datename][-1]
        day += datetime.timedelta(days=1)
        data[datename].append(day)

        colp  = data[pname][-1]*(1+data[ppname][-1])
        data[pname].append(colp)

        col = data[colname][-1]*(1+data[pname][-1])
        r = math.ceil(math.log10(col))
        col = int(round(col, -r+3))
        data[colname].append(col)

        colpp = (sum(data[ppname][i:i+window_size])+colpp)/(window_size+1)
        data[ppname].append(colpp)
        
    rst = pd.DataFrame(data)
    rst.set_index(datename, inplace=True)

    return rst

def usage():
    progname = os.path.basename(sys.argv[0])
    text = '''
Usage: %s [OPTIONS] [COUNTRY]

Prints the prognosis for the specified number of DAYS with 
real data for the previous number of DAYS (see OPTIONS).

COUNTRY can be empty and then 'world' by default or URL: 
https://www.worldometers.info/coronavirus/country/COUNTRY/ 
or it can be just COUNTRY from URL.

OPTIONS are:
   -f FIELD[,FIELD...] Specify fields (Cases, Active, Deaths)
   -d DAYS             Specify days for prognosis (default 5)
   -h | --help         This usage message
''' % progname
    return text

if __name__ == '__main__':

    window_size = 5
    country = 'world'
    fields = [cfg.cases, cfg.active, cfg.deaths]
    
    opts, remainder = getopt.getopt(sys.argv[1:], 'f:d:h', ['help'])
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(usage())
            exit()
        elif opt == '-f':
            fields = arg.split(',')
        elif opt == '-d':
            window_size = int(arg)

    if remainder:
        country = remainder[0]

    df = fetch.fetch(country)
    df = process.process(df, window_size)
    for field in fields:
        print(prognos(df, field, window_size))
