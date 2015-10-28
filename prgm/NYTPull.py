#!/usr/bin/env python

import datetime
from os import getcwd
from time import sleep
from math import ceil
from requests import get
from json import dumps

class NYTPull(object):

    def __init__(self, key):
        self.url = 'http://api.nytimes.com/svc/search/v2/articlesearch'
        self.key = key
        self.begin_date = '20100101'
        self.end_date = '20130101'

    # Dynamically creates path to fixtures folder
    def MakePath(self, folder, file):
        origin = getcwd().split('\\')
        source = origin[0:len(origin)-1]
        source.append(folder)
        source.append(file)
        path = '\\'.join(source)
        return path

    # Replaces certain character values for the URL
    def ReplaceString(self, string):
        find = {':':'%3A','"':'%22','(':'%28',')':'%29',' ':'+'}
        for x in find:
            string = string.replace(x, find[x])
        return string

    # Create the URL for use
    def URL(self, country, begin_date, end_date, page):
        resp_format = 'json'
        q = self.ReplaceString('"{}"'.format(country))
        fq = self.ReplaceString('section_name:("World" "Travel" "Foreign")')
        sort = 'oldest'
        if type(page) == int:
            page = str(page)
        key = self.ReplaceString(self.key)
        return ''.join([self.url, '.', resp_format, \
                        '?q=', q, \
                        '&fq=', fq, \
                        '&begin_date=', begin_date, \
                        '&end_date=', end_date, \
                        '&sort=', sort, '&page=', page, \
                        '&api-key=', key])

    # Fetches URL from API
    def FetchURL(self, url):
        r = get(url)
        if r.status_code == 200:
            payload = r.json()
            return payload['response'] 

    # Saves Data into country file
    def SavePull(self, country, data, page):
        content = dumps(data)
        if type(page) == int:
            page = str(page)
        file = [country.replace(' ',''),page,'.json']
        path = self.MakePath('fixtures', ''.join(file))
        with open(path, 'w') as f:
            f.write(content)
            print('Created: ', file)

    # Pulls from API
    def Pull(self, country, begin_date, end_date, page):
        url = self.URL(country, begin_date, end_date, page)
        data = self.FetchURL(url)
        self.SavePull(country, data, page)
        if page == 0:
            return data['meta']['hits']

    # Pulls all pages from API, ensuring all hits are pulled
    def PullLoop(self, country, begin_date, end_date):
        hits = self.Pull(country, begin_date, end_date, 0)
        max_page = ceil(hits/10)
        if max_page == 1:
            pass
        elif max_page <= 100:
            sleep(10)
            for i in range(1, max_page):
                self.Pull(country, begin_date, end_date, i)
                sleep(10)
        elif max_page > 100:
            self.AdjDates(country, begin_date, end_date)

    def Dates(self, date):
        year = int(date[0:4])
        month = int(date[4:6])
        day = int(date[6:4])
        datetime.date(year, month, day)

    # Adjusts begin_date and end_date when hits>100
    def AdjDates(self, country, begin_date, end_date):
        begin_date = Dates(begin_date)
        end_date = Dates(end_date)
        delta = (end_date - begin_date)/2
        

    def Main(self):
        country = 'Falkland Islands'
        self.PullLoop(country, self.begin_date, self.end_date, key)
        
if __name__ == "__main__":
    c = NYTPull('3b0e8a2c16c2aabe3a3ca8b76ef573fc:1:72949871')
    c.Main()
