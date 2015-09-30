#!/usr/bin/env python

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

if __name__ == "__main__":
    c = NYTPull()
    key = 'key'
    url = c.URL(key)
    print(url)
