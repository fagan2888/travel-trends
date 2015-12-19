#!/usr/bin/env python

import sqlite3
import pandas as pd
import numpy as np
from textblob import TextBlob

class SentAnalyze(object):

	def __init__(self):
		pass	
		
	def TextGenerator(self, cell):
		for i in range(len(cell)):
			yield i, cell[i]
				
	def Sentiment(self, s):
		if s == None: sent = 0
		else:
			blob = TextBlob(s)
			sent = 0
			for sentence in blob.sentences:
				polarity = sentence.sentiment.polarity
				subjectivity = sentence.sentiment.subjectivity + 1
				sent = sent + (polarity * subjectivity)
		return sent
			
	def StoreSentiment(self, np_array):
		output_array = []
		for cell in np_array[:,[0,1,2,3]]:
			line = []
			tot_sent = 0
			for i, s in self.TextGenerator(cell):
				if i == 0: line.append(s)
				else:
					sent = self.Sentiment(s)
					line.append(sent)
					tot_sent = tot_sent + sent
			line.append(tot_sent)
			print(line)
			output_array.append(line)
		return np.array(output_array)
					
	def Save(self, np_array):
		column_names = ['article_id', 'headline', 'abstract', 'lead_paragraph', 'total']
		df = pd.DataFrame(data=np_array, columns=column_names)
		df.to_sql('SentAnalysis', conn, if_exists='replace')
				
if __name__ == "__main__":
	conn = sqlite3.connect('../fixtures/travel-trends.db')
	df = pd.read_sql_query("SELECT * FROM ArticlePurged;", conn)
	np_array = df.as_matrix()
	c = SentAnalyze()
	out_array = c.StoreSentiment(np_array)
	c.Save(out_array)
	# df = pd.read_sql_query("""SELECT e.*, f."2-byte"
	# 							FROM (SELECT c._id, c.pub_date, c.total, d.country
	# 								FROM (SELECT b._id, b.pub_date, a.total
	# 									FROM SentAnalysis AS a
	# 									INNER JOIN Article_ID AS b
	# 									ON a.id=b._id) as c
	# 								INNER JOIN country_id as d
	# 								ON c._id=d._id) as e
	# 							INNER JOIN Crosswalk as f
	# 							ON UPPER(e.country)=UPPER(f."Country Name")
	# 						;""", conn)
	# path = '../fixtures/Sentiment.csv'
	# save = df.to_csv(path)