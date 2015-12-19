#!/usr/bin/env python

from os import getcwd
import pandas as pd
import sqlite3

class dbWrangler(object):
	
	def __init__(self):
		pass
		
	def MakeTable(self, db_conn, path, table_name, typ='csv'):
		c = db_conn.cursor()
		query = "DROP TABLE IF EXISTS {};".format(table_name)
		c.execute(query)
		if typ == 'csv':
			df = pd.read_csv(path)
		if typ == 'excel':
			xl = pd.ExcelFile(path)
			df = xl.parse("NewList")
		df.to_sql(table_name, db_conn, if_exists='replace')
		
if __name__ == "__main__":
	# w = dbWrangler()
	conn = sqlite3.connect('../fixtures/Travel-Trends.db')
	# # FlightData
	# path1 = '../fixtures/Gtown_class_export_FINAL.txt'
	# w.MakeTable(conn, path1, 'FlightData')
	# # CountryList Crosswalk
	# path2 = '../fixtures/country lookup file.xlsx'
	# w.MakeTable(conn, path2, 'Crosswalk', typ='excel')
	# # NYTList
	# path3 = '../fixtures/CountryListNoDups.txt'
	# w.MakeTable(conn, path3, 'CountryList')
	
	c = conn.cursor()
	query00="DROP TABLE IF EXISTS Crosswalk2;"
	query01="""CREATE TABLE Crosswalk2 AS
					SELECT DISTINCT *
					FROM Crosswalk
					WHERE "2-byte" != ''
				;"""
	query02="DROP TABLE IF EXISTS Crosswalk;"
	query03="""ALTER TABLE Crosswalk2
					RENAME TO Crosswalk
				;"""
				
	c.execute(query00)
	c.execute(query01)
	c.execute(query02)
	c.execute(query03)