#!/usr/bin/env python

##AND section_name:("World" "Travel" "Foreign")

import json
import requests
import os
import time

class NYTPull(object):

    def __init__(self):
        pass

    def MakePath(self, folder, file):
        origin = os.getcwd().split('\\')
        source = origin[0:len(origin)-1]
        source.append(folder)
        source.append(file)
        path = '\\'.join(source)
        return path

    def ReplaceString(self, string):
        find = {':':'%3A','"':'%22','(':'%28',')':'%29',' ':'+'}
        for key in find:
            string = string.replace(key, find[key])
        return string

    def URL(self, country, begin_date, end_date, page, key):
        base_url = 'http://api.nytimes.com/svc/search/v2/articlesearch'
        resp_format = 'json'
        q = self.ReplaceString('"{}"'.format(country))
        fq = self.ReplaceString('section_name:("World" "Travel" "Foreign")')
        sort = 'oldest'
        key = self.ReplaceString(key)
        return ''.join([base_url, '.', resp_format, \
                        '?q=', q, \
                        '&fq=', fq, \
                        '&begin_date=', begin_date, \
                        '&end_date=', end_date, \
                        '&sort=', sort, '&page=', page, \
                        '&api-key=', key])
                        
    def FetchURL(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            payload = r.json()
            return payload['response'] 
        
    def SavePull(self, data, page):
        content = json.dumps(data)
        path = self.MakePath('fixtures', 'Page{}.json'.format(page))
        with open(path, 'w') as f:
            f.write(content)

    def Main(self):
        country = 'Falkland Islands'
        begin_date = '20100101'
        end_date = '20130101'
        page = str(0)
        key = 'XXXXXXX'
        url = self.URL(country, begin_date, end_date, page, key)
        print(url)
        data = self.FetchURL(url)
        self.SavePull(data, page)
        
if __name__ == "__main__":
    c = NYTPull()
    c.Main()
