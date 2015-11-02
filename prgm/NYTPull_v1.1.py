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
        self.country_list = 'countries.txt'

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

    # Create the url
    def URL(self, country, begin_date, end_date, page):
        resp_format = 'json'
        q = self.ReplaceString('"{}"'.format(country))
        fq = self.ReplaceString('section_name:("World" "Travel" "Foreign")')
        sort = 'oldest'
        if type(page) == int:
            page = str(page)
        key = self.ReplaceString(self.key)
        url = ''.join([self.url, '.', resp_format, \
                        '?q=', q, \
                        '&fq=', fq, \
                        '&begin_date=', begin_date, \
                        '&end_date=', end_date, \
                        '&sort=', sort, '&page=', page, \
                        '&api-key=', key])
        return url

    # Fetches URL from API
    def FetchURL(self, url):
        r = get(url)
        if r.status_code == 200:
            payload = r.json()
        return payload['response']

    # Name a enumerated json file
    def NameFile(self, name, i):
        if type(i) == int:
            i = str(i)
        l = [name, i, '.json']
        file = ''.join(l)
        return file
        
    # Save a file
    def Save(self, content, file):
        path = self.MakePath('fixtures', file)
        with open(path, 'w') as f:
            f.write(content)
            print('Saved: {}'.format(file))

    # Retrieves file from api
    def Pull(self, country, begin_date, end_date, page, offset=0):
        url = self.URL(country, begin_date, end_date, page)
        data = self.FetchURL(url)
        page_num = page + offset
        file = self.NameFile(country, page_num)
        content = dumps(data)
        self.Save(content, file)
        if page == 0:
            return data['meta']['hits']

    # Readfile containing country names
    def ReadLoop(self, file):
        path = self.MakePath('fixtures', self.country_list)
        with open(path) as f:
            for line in f:
                country = line.strip('\n\r')
                self.PagePull(country)

    # Pull first page and determine next steps
    def InitPull(self, country):
        hits = self.Pull(country, self.begin_date, self.end_date, 0)
        sleep(10)
        max_page = ceil(hits/10)
        if max_page == 1:
            pass
        elif max_page <= 100:
            self.PagePull(country, self.begin_date, self.end_date, max_page)
        elif max_page > 100:
            self.AltPagePull(country, max_page)

    # Retrieve pages up to 100
    def PagePull(self, country, begin_date, end_date, max_page):
        for i in range(1, max_page):
            self.Pull(country, begin_date, end_date, i)

    # Converts a string date to datetime format
    def Dates(self, date_string):
        year = int(date_string[:4])
        month = int(date_string[4:6])
        day = int(date_string[6:])
        date = datetime.date(year, month, day)
        return date

    # Converts a datetime format to a string
    def DateString(self, date):
        date = str(date).replace('-','')
        return date

    # Adds one day to a string formatted date
    def AddaDay(self, date_string):
        date = self.Dates(date_string)
        date_plus_1 = date + datetime.timedelta(days=1)
        return self.DateString(date_plus_1)

    #Finds the middle date of any two dates
    def MidDate(self, begin_date, end_date):
        begin = self.Dates(begin_date)
        end = self.Dates(end_date)
        delta = (end - begin) / 2
        midpoint = begin + delta
        return self.DateString(midpoint)

    # Under Construction
    def AltPagePull(self, country, max_page):
        m1 = self.MidDate(self.begin_date, self.end_date)
        new_cnt = self.Pull(country, self.begin_date, m1, 0, offset=100)
        print(new_cnt)
        m2 = self.AddaDay(m1)
        new_cnt = self.Pull(country, m2, self.end_date, 0, offset=200)
        print(new_cnt)

    # Read country names from file
    def ReadCountries(self, file):
        f = ['Iran', 'Russia']
        for line in f:
            self.InitPull(line)
##        path = self.MakePath('fixtures', file)
##        with open(path) as f:
##            for line in f:
##                country = line.strip('\n\r')
##                self.PullLoop(country, self.begin_date, self.end_date)

if __name__ == "__main__":
    c = NYTPull('3b0e8a2c16c2aabe3a3ca8b76ef573fc:1:72949871')
    c.ReadCountries('Countries.txt')
