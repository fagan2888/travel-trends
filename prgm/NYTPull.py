#!/usr/bin/env python

import json
import requests
import os

class NYTPull(object):

    def __init__(self):
        pass

    def URL(self, key):
        base_URL = 'http://api.nytimes.com/svc/search/v2/articlesearch'
        fq = 'glocations:("Russia")'
        begin_date = '20100101'
        end_date = '20120101'
        sort = 'oldest'
        page = '{}'
        key = key
        return ''.join([base_URL, '.json?fq=', fq, \
                        '&begin_date=', begin_date, \
                        '&end_date=', end_date, '&sort=', sort, \
                        '&page=', page, '&api-key=', key])
                        
    def FetchURL(self):
        URL = URL()
        r = requests.get(URL)
        payload = r.json()
        return payload
        
    def SavePull(self):
        data = FetchURL()
        
        
        

if __name__ == "__main__":
    c = NYTPull()
    key = 'key'
    url = c.URL(key)
    print(url)
