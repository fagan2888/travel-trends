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

    def InitPull(self, country):
        hits = self.Pull(country, self.begin_date, self.end_date, 0)
        #sleep(10)
        max_page = ceil(hits/10)
        if max_page == 1:
            pass
        elif max_page <= 100:
            self.PagePull(country, self.begin_date, self.end_date, max_page)
        elif max_page > 100:
            self.AltPagePull(country, max_page)

    def PagePull(self, country, begin_date, end_date, max_page):
        for i in range(1, max_page):
            self.Pull(country, begin_date, end_date, i)

    def Dates(self, date_string):
        year = int(date_string[:4])
        month = int(date_string[4:6])
        day = int(date_string[6:])
        date = datetime.date(year, month, day)
        return date

    def DateString(self, date):
        date = str(date).replace('-','')
        return date

    def AddaDay(self, date_string):
        date = self.Dates(date_string)
        date_plus_1 = date + datetime.timedelta(days=1)
        return self.DateString(date_plus_1)
        
    def MidDate(self, begin_date, end_date):
        begin = self.Dates(begin_date)
        end = self.Dates(end_date)
        delta = (end - begin) / 2
        midpoint = begin + delta
        return self.DateString(midpoint)

    def AltPagePull(self, country, max_page):

        m1 = self.MidDate(self.begin_date, self.end_date)
        new_cnt = self.Pull(country, self.begin_date, m1, 0, offset=100)
        print(new_cnt)
        m2 = self.AddaDay(m1)
        new_cnt = self.Pull(country, m2, self.end_date, 0, offset=100)
        print(new_cnt)

    def Loop(self):
        for line in self.l:
            self.InitPull(line)
        
if __name__ == "__main__":
    c = Tester()
    c.Loop()
