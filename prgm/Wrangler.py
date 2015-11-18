from os import getcwd
import pandas as pd
import sqlite3

class dbWrangler(object):
	
	def __init__(self):
		pass
		
	def MakeTable(self, db_conn, path, table_name):
		df = pd.read_csv(path)
		df.to_sql(table_name, db_conn, if_exists='replace')
		
if __name__ == "__main__":
	w = dbWrangler()
	conn = sqlite3.connect('../fixtures/Travel-Trends.db')
	# FlightData
	path1 = '../fixtures/Gtown_class_export_FINAL.txt'
	w.MakeTable(conn, path1, 'FlightData')
	# CountryList
	path2 = '../fixtures/CountryList-names.csv'
	w.MakeTable(conn, path2, 'CountryList')
	# NewCountryList
	path3 = '../fixtures/CountryListNoDups.txt'
	w.MakeTable(conn, path3, 'CountryList-ext')
	
	