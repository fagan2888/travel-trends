import sqlite3 as sql
import pandas as pd
from sklearn import linear_model

conn = sql.connect('../fixtures/travel-trends.db')

df = pd.read_sql_query("""SELECT * FROM FinalOutput WHERE PM_Flights IS NOT NULL 
							AND Article_Cnt + Blog_Cnt + Other_Cnt + Major_Articles
								+ Total_Cnt + Total_AdjCnt + Rank_Total + Avg_Rank 
								+ WordCount_Total + Avg_WordCount + Headline_Total
								+ Abstract_Total + LeadParagraph_Total + Avg_Sent 
								+ Total_Sent + Avg_AdjSent IS NOT NULL;""", conn)

indep = ['Article_Cnt', 'Blog_Cnt', 'Other_Cnt', 'Major_Articles', 'Total_Cnt',
			'Total_AdjCnt', 'Rank_Total', 'Avg_Rank', 'WordCount_Total',
			'Avg_WordCount', 'Headline_Total', 'Abstract_Total', 'LeadParagraph_Total',
			'Avg_Sent', 'Total_Sent', 'Avg_AdjSent']
			
dep = ['OTMC_Flights']

data = df[indep].as_matrix()
target = df[dep].as_matrix()

clf = linear_model.LinearRegression()
clf.fit(data, target)

#   Country_Id TEXT,
#   date,
#   Article_Cnt,
#   Blog_Cnt,
#   Other_Cnt,
#   Major_Articles,
#   Total_Cnt,
#   Total_AdjCnt,
#   Rank_Total,
#   Avg_Rank,
#   WordCount_Total,
#   Avg_WordCount,
#   Headline_Total,
#   Abstract_Total,
#   LeadParagraph_Total,
#   Avg_Sent,
#   Total_Sent,
#   Avg_AdjSent,
#   CM_Flights,
#   PM_Flights,
#   OTMC_Flights,
#   PctChg_Flights,
#   CM_3MvAvg,
#   PM_3MvAvg,
#   Diff_3MvAvg,
#   PctChg_3MvAvg,
#   CM_6MvAvg,
#   PM_6MvAvg,
#   Diff_6MvAvg,
#   PctChg_6MvAvg,
#   CM_12MvAvg,
#   PM_12MvAvg,
#   Diff_12MvAvg,
#   PctChg_12MvAvg