#!/usr/bin/env python

from os import getcwd
from os import listdir
from json import load
import pandas as pd
from pandas.io.json import json_normalize 
import sqlite3

class NYT_Wrangle(object):
	
	def __init__(self):
		# self.json_indexer = ['pub_date', 'lead_paragraph', ['headline', 'main'], 'abstract', 'word_count', \
		# 					 'document_type', '_id']
		self.json_indexer = ['pub_date', 'news_desk', 'lead_paragraph', 'section_name', \
							 ['headline', 'main'], 'print_page', 'snippet', 'abstract', \
							 'word_count', 'source', 'document_type', 'type_of_material', \
							 '_id']
	
	def ListFiles(self, paths):
		for path in paths:
			dir_list = listdir(path)
			for file in dir_list:
				yield '/'.join([path, file])
	
	def OpenJsonFile(self, path):
		with open(path, 'r', encoding='utf-8') as data_file:
			data = load(data_file)
			return data

	def DeNormalizedDataFrame(self, path):
		data = w.OpenJsonFile(path)
		df = json_normalize(data['docs'], 'keywords', self.json_indexer)
		return df

	def GenDataFrames(self, list_files):
		for i, file in enumerate(list_files):
			df = self.DeNormalizedDataFrame(file)
			yield i, df
            
if __name__ == "__main__":
	w = NYT_Wrangle()
	paths = ['../fixtures/part1', '../fixtures/part2']
	list_files = w.ListFiles(paths)
	for i, path in enumerate(list_files):
		print(path)
		if i == 0:
			df = w.DeNormalizedDataFrame(path)
		else:
			df2 = w.DeNormalizedDataFrame(path)
			df = df.append(df2, ignore_index=True)
	db_path = '../fixtures/Travel-Trends.db'
	conn = sqlite3.connect(db_path)
	df.to_sql('DeNormalizedNYT', conn, if_exists='replace')
	
	query00 = "DROP TABLE IF EXISTS country_id;"
	query01 = """CREATE TABLE country_id as
					SELECT DISTINCT _id as article_id,
						CASE WHEN INSTR(value,"(")>0
								THEN UPPER(SUBSTR(value, INSTR(value, "(") + 1,
									INSTR(value, ")") - INSTR(value, "(") - 1))
							ELSE UPPER(value) END AS Country, is_major, rank
					FROM DeNormalizedNYT
					WHERE UPPER(name)=="GLOCATIONS"
						AND UPPER(document_type) IN ("ARTICLE","BLOGPOST")
						AND UPPER(value)!="UNITED STATES"
					ORDER BY Country, _id
				;"""
	query10 = "DROP TABLE IF EXISTS article_id;"
	query11 = """CREATE TABLE article_id as
					SELECT DISTINCT _id as article_id, "headline.main" as headline, 
						abstract, lead_paragraph,
						pub_date, document_type, word_count
					FROM DeNormalizedNYT
					WHERE UPPER(name)=="GLOCATIONS"
						AND UPPER(document_type) IN ("ARTICLE","BLOGPOST")
						AND UPPER(value)!="UNITED STATES"
					ORDER BY pub_date, _id
				;"""
	c = conn.cursor()
	c.execute(query00)
	c.execute(query01)
	c.execute(query10)
	c.execute(query11)
