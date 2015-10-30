#!/usr/bin/env python

import datetime
from os import getcwd
from time import sleep
from math import ceil
from request import get
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
        source.append(folder).append(file)
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
        content = dump(data)
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

    # PagePull
    def PagePull(self, country):
        hits = self.Pull(country, self.begin_date, self.end_date, 0)
        sleep(10)
        max_page = ceil(hits/10)
        if max_page == 1:
            pass
        elif max_page <= 100:
            for i in range(1, max_page):
                sleep(10)
                self.Pull(country, self.begin_date, self.end_date, i)
        elif max_page > 100:
            self.AltPagePull(country, max_page)
