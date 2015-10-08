#!/usr/bin/env python

##AND section_name:("World" "Travel" "Foreign")

import json
import requests
import os
import time

class NYTPull(object):

    def __init__(self):
        pass

    def ReplaceString(self, string):
        find = {':':'%3A','"':'%22','(':'%28',')':'%29',' ':'+'}
        for key in find:
            string = string.replace(key, find[key])
        return string

    def FormatCountryList(self, country_list):
        pass

    def URL(self, country, begin_date, end_date, key):
        base_url = 'http://api.nytimes.com/svc/search/v2/articlesearch'
        resp_format = 'json'
        fq = self.ReplaceString('glocations:({})'.format(country))
        sort = 'oldest'
        if page>100: raise ValueError('Page > 100: Needs to be <=100')
        key = self.ReplaceString(key)
        return ''.join([base_url, '.', resp_format, \
                        '?fq=', fq, \
                        '&begin_date=', begin_date, \
                        '&end_date=', end_date, \
                        '&sort=', sort, '&page=', page, \
                        '&api-key=', key])
                        
    def FetchURL(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            payload = r.json()
            return payload['response'] 
        
    def SavePull(self, data):
        content = json.dumps(data)
        with open('Page{}.json'.format(i), 'w') as f:
            f.write(content)

    def Main(self):
        country = ''
        begin_date = ''
        end_date = ''
        key = 'XXXXXXX'
        url = c.URL(country, begin_date, end_date, key)
        data = FetchURL(url)
        c.SavePull(data)
        
if __name__ == "__main__":
    c = NYTPull()
    c.Main()
