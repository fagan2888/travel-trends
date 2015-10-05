#!/usr/bin/env python

##goal = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?\
##        fq=glocations%3A%28%22Russia%22+%22Iran%22%29&begin_date=20100101&\
##        end_date=20130101&sort=oldest&page=1&\
##        api-key=KEYGOESHERE'.replace(' ','')

import json
import requests
import os

class NYTPull(object):

    def __init__(self):
        pass

    def ReplaceString(self, string):
        find = {':':'%3A','"':'%22','(':'%28',')':'%29',' ':'+'}
        for key in find:
            string = string.replace(key, find[key])
        return string

    def URL(self, key):
        base_url = 'http://api.nytimes.com/svc/search/v2/articlesearch'
        resp_format = 'json'
        fq = self.ReplaceString('glocations:("Russia" "Iran")')
        begin_date = '20100101'
        end_date = '20130101'
        sort = 'oldest'
        page = '{}'
        key = self.ReplaceString(key)
        return ''.join([base_url, '.', resp_format, \
                        '?fq=', fq, \
                        '&begin_date=', begin_date, \
                        '&end_date=', end_date, \
                        '&sort=', sort, '&page=', page, \
                        '&api-key=', key])
                        
    def FetchURL(self, key):
        URL = self.URL(key).format(1)
        r = requests.get(URL)
        payload = r.json()
        return payload['response']
        
    def SavePull(self, key):
        data = self.FetchURL(key)
        content = json.dumps(data)
        with open('test{}.json'.format(1), 'w') as f:
            f.write(content)
        
if __name__ == "__main__":
    c = NYTPull()
    key = '3b0e8a2c16c2aabe3a3ca8b76ef573fc:1:72949871'
    url = c.URL(key).format(1)
    print(url)
    c.SavePull(key)

