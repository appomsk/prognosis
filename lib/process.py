#!/usr/bin/python3

import sys
import os
import glob
import pandas as pd

import config as cfg
import fetch

def new_vals(df, col, win_size):
    idx = df.columns.get_loc(col)

    idx += 1
    diffs = [0]
    for i in range(1, len(df)):
        t = df[col][i] - df[col][i-1]
        diffs.append(t)
    df.insert(idx, cfg.mkcol_diff(col), diffs)  # Diff

    idx += 1
    ps = [0]
    for i in range(1, len(df)):
        a = df[col][i]
        b = df[col][i-1]
        t = 0 if b == 0 else (a/b)-1
        ps.append(t)
    df.insert(idx, cfg.mkcol_p(col), ps)

    pps = [0, 0]
    for i in range(2, len(df)):
        a = ps[i]
        b = ps[i-1]
        t = 0 if b == 0 else (a/b)-1
        pps.append(t)
    
    idx += 1
    ave = average_p(df, ps, win_size)
    df.insert(idx, cfg.mkcol_avep(col), ave)

    avepp = average_pp(df, pps, win_size)

    idx += 1
    ave = average1(ps, avepp) 
    df.insert(idx, cfg.mkcol_ave1(col), ave)

    idx += 1
    df.insert(idx, cfg.mkcol_pp(col), pps)

    idx += 1
    df.insert(idx, cfg.mkcol_avepp(col), avepp)

def average1(ps, pps):
    # from average pps
    k = 0
    while pps[k] == 0:
        k += 1
    rst = [0] * (k+1)  # from average pp we can get data for the next day
    
    for i in range(k, len(pps)):
        rst.append(ps[i]*(1+pps[i]))
    rst.pop(-1)
    return rst

def average_p(df, ps, win_size):
    k = 0
    while ps[k] == 0:
        k += 1
    rst = [0] * (k + win_size - 1)  # -1 - because of one place for the first average

    av = sum(ps[k:k+win_size])/win_size
    rst.append(av)
    k += 1   # k on the start of the first window

    for i in range(k, len(ps)-win_size+1):
        s = sum(ps[i:i+win_size])
        av = (s + rst[i+win_size-2])/(win_size+1)
        rst.append(av)

    return rst

def average_pp(df, pps, win_size):
    k = 0
    while pps[k] == 0:
        k += 1
    rst = [0] * (k + win_size - 1)  # -1 - because of one place for the first average

    av = sum(pps[k:k+win_size])/win_size
    rst.append(av)
    k += 1   # k on the start of the first window

    for i in range(k, len(pps)-win_size+1):
        s = sum(pps[i:i+win_size])
        av = (s + rst[i+win_size-2])/(win_size+1)
        rst.append(av)

    return rst


def process(df, win_size = 5):
    for col in df.columns:
        if col == cfg.dates:
            continue
        new_vals(df,  col, win_size)

    return df


if __name__ == '__main__':
    what = ""
    if len(sys.argv) != 1:
        what = sys.argv[1]
    df = fetch.fetch(what)
    print(process(df).to_markdown())
