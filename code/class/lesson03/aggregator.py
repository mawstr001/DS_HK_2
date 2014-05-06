#!/usr/bin/env python
"""
General Assembly - Data Science
Lesson 3 : New York Times, Aggregated CTR
"""
from __future__ import division
import urllib
from urlparse import urlparse
import pandas as pd
import os.path

# Define the location of the data directory in relation to this script.
DATA_DIR = '../../../data/'

def download_series(base_url, extension, limit):
    """
    download a series of files with incremental numberic suffix
    @param str base_url  base url to download from
    @param str extension  file format extension
    @param int limit  how many files should be downloaded
    @return list      list of file locations
    """
    file_list = []
    for i in range(limit):
        filename = urlparse(base_url).path.split('/')[-1] + str(i+1) + '.' + extension
        print "Downloading %s..." % filename
        urllib.urlretrieve(base_url + str(i+1) + '.' + extension, DATA_DIR + filename)
        file_list.append(DATA_DIR + filename)
    return file_list

def merge_csv(file_list, output):
    fout=open(DATA_DIR + output,"a")
    # first file:
    for line in open(file_list[0]):
        fout.write(line)
    # now the rest:    
    for file_name in file_list[1:]:
        f = open(file_name)
        f.next() # skip the header
        for line in f:
             fout.write(line)
        f.close() 
    fout.close()
    return output

def load_nytimes_dataset(n):
    """
    request NYT datasets
    @param int n     number of CSVs to obtain
    @return list      list of CSVs
    """

    assert n < 32

    if not os.path.isfile(DATA_DIR + 'nyt_agg.csv'):
        base_url = 'http://stat.columbia.edu/~rachel/datasets/nyt'
        file_list = download_series(base_url, 'csv', n)
        merge_csv(file_list, 'nyt_agg.csv')
    
    df = pd.read_csv(DATA_DIR + 'nyt_agg.csv')

    return df

def ratio(x,y):
    if y != 0:
        return x/y
    else:
        return 0

def add_ratio(df,label,numerator,denominator):
    df[label] = map(ratio, df[numerator], df[denominator])
    return df

# df = load_nytimes_dataset(31)
   
# df = add_ratio(df,'CTR', "Clicks", "Impressions")

# df.to_csv('nytimes_aggregation.csv')