

class Tester(object):

    def __init__(self):
        self.path = '/Users/bmharris/Python/travel-trends/fixtures/CountryList.csv'
    
    def ReadFile(self):
        with open(self.path, 'r') as f:
            x = f.readlines()
            country_list = []
            for line in x:
                line = repr(line).replace(r'\r\n','').replace("'",'').strip()
                country_list.append(line)
            return country_list
        
    def CheckDuplicates(self, string_list):
        new_list = string_list
        for line in string_list:
            l = []
            for s in new_list:
                if line == s: pass
                elif line in s:
                    l.append(s)
            if len(l) >= 1:
                for s in l:
                    new_list.remove(s)
            status = str(len(new_list))
        return new_list
        
    def Save(self, data):
        l = self.path.split('/')
        new_path = '/'.join(l[:-1]) + '/CountryListNoDups.txt'
        with open(new_path, 'w') as f:
            for line in data:
                f.write(line + '\r\n')
        
if __name__ == "__main__":
    c = Tester()
    country_list = c.ReadFile()
    no_dups_list = c.CheckDuplicates(country_list)
    c.Save(no_dups_list)
    l = c.Create_country_list()
    for line in l:
        print(line)
