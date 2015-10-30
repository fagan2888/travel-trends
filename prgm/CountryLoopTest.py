import datetime
from os import getcwd
from time import sleep
from math import ceil
from requests import get
from json import dumps

class Tester(object):

    def __init__(self):
        self.begin_date = '20100101'
        self.end_date = '20130101'
        self.l = ['Iran', 'Iraq', 'Russia']

    def Pull(self, country, begin_date, end_date, page, offset=0):
        page_num = page + offset
        l = [country, str(page_num)]
        file = ''.join(l)
        print(file, begin_date, end_date)
        if page == 0:
            if offset == 0:
                if country == 'Iran': return 2575
                if country == 'Russia': return 1350
                if country == 'Iraq': return 576
            elif offset > 0 and offset <= 100:
                if country == 'Russia': return 656
                if country == 'Iran': return 1732
            elif offset > 100: return 897

    def PagePull(self, country):
        hits = self.Pull(country, self.begin_date, self.end_date, 0)
        #sleep(10)
        max_page = ceil(hits/10)
        if max_page == 1:
            pass
        elif max_page <= 100:
            for i in range(1, max_page):
                #sleep(10)
                self.Pull(country, self.begin_date, self.end_date, i)
        elif max_page > 100:
            pass

    def Loop(self):
        for line in self.l:
            self.PagePull(line)
        
if __name__ == "__main__":
    c = Tester()
    c.Loop()
