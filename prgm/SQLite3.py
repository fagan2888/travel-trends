import sqlite3 as sql
import pandas as pd

db_path = '../fixtures/travel-trends.db'
conn = sql.connect(db_path)

query00 = "DROP TABLE IF EXISTS CountryFinal;"
query01 = """CREATE TABLE CountryFinal AS
				SELECT DISTINCT a.*, 
				"2-byte" AS country_id,
				FROM Country_ID AS a
				INNER JOIN Crosswalk AS b
				ON UPPER(a.country)=UPPER("Country Name")
			;"""
			
query02 = "DROP TABLE IF EXISTS ArticlePurged;"
query03 = """CREATE TABLE ArticlePurged AS
				SELECT DISTINCT a.*
				FROM article_id AS a
				INNER JOIN CountryFinal AS b
				ON a.article_id=b.article_id
			;"""
			
query04 = "DROP TABLE IF EXISTS ArticleSent;"
query05 = """CREATE TABLE ArticleSent AS
				SELECT a.article_id as article_id,
					DATE(pub_date) AS date,
					SUBSTR(pub_date, 1, 4) AS year,
					SUBSTR(pub_date, 6, 2) AS month,
					Country, country_id,
					is_major, rank,
					document_type,
					word_count,
					a.headline AS headline,
					b.headline AS headline_sent,
					a.abstract AS abstract, 
					b.abstract AS abstract_sent,
					a.lead_paragraph AS lead_paragraph,
					b.lead_paragraph AS lead_paragraph_sent,
					b.total AS Total_Sent		
				FROM ArticlePurged AS a
				INNER JOIN SentAnalysis AS b
				ON a.article_id=b.article_id
				INNER JOIN CountryFinal AS c
				ON a.article_id=c.article_id
			;"""
			
query06 = "DROP TABLE IF EXISTS AdjNYTData;"
query07 = """CREATE TABLE AdjNYTData AS
				SELECT Country, Country_ID,
					year||'-'||month||'-01' AS date,
					Article_Cnt, Blog_Cnt, Other_Cnt, Major_Articles, 
					Total_Cnt, Total_AdjCnt,
					Rank_Total, Rank_Total/Total_Cnt AS Avg_Rank,
					WordCount_Total, WordCount_Total/Total_Cnt AS Avg_WordCount,
					Headline_Total, Abstract_Total, LeadParagraph_Total,
					Total_Sent/Total_Cnt AS Avg_Sent, Total_Sent, 
					AdjTotal_Sent/Total_AdjCnt Avg_AdjSent, AdjTotal_Sent 
				FROM
					(SELECT Country, Country_ID,
						year, month, 
						SUM(document_type='article') AS article_cnt,
						SUM(document_type='blog') AS blog_cnt,
						SUM(document_type not in ('article', 'blog')) AS other_cnt,
						COUNT(article_id) AS total_cnt,
						TOTAL(is_major='Y') AS Major_Articles,
						TOTAL(rank) AS Rank_Total,
						SUM(rank is not null) AS Total_AdjCnt,
						TOTAL(word_count) AS WordCount_Total,
						TOTAL(headline_sent) AS Headline_Total,
						TOTAL(abstract_sent) AS Abstract_Total,
						TOTAL(lead_paragraph) AS LeadParagraph_Total,
						TOTAL(Total_Sent) AS Total_Sent,
						TOTAL((rank is not null)*Total_Sent) AS AdjTotal_Sent
					FROM ArticleSent
					GROUP BY Country, Country_ID, Year, Month)
			;"""
			
query08 = "DROP TABLE IF EXISTS AdjFlightData;"
query09 = """CREATE TABLE AdjFlightData AS
				SELECT DATE(CASE WHEN "mo"<10 THEN "YR"||'-0'||"mo"||'-01' 
						ELSE "YR"||'-'||"mo"||'-01' END) AS date,
					"CNTRY_CD" AS Country_ID,
					TOTAL("Count(Distinct(TRAN_NBR))") AS Flights
				FROM FlightData
				WHERE "CNTRY_CD" IS NOT NULL
					AND "CNTRY_CD"!='?'
				GROUP BY "CNTRY_CD", Date
				ORDER BY "CNTRY_CD", Date
			;"""
			
query10 = "DROP TABLE IF EXISTS FlightData_Final;"
query11 = """CREATE TABLE FlightData_Final AS
				SELECT a.Country_ID as Country_Id,
					a.date as Date,
					a.flights AS CM_Flights, 
					b.flights AS PM_Flights,
					a.flights-b.flights AS OTMC_Flights,
					a.flights/b.flights-1 AS PctChg_Flights,
					(a.flights + b.flights + c.flights)/3 AS CM_3MvAvg,
					(b.flights + c.flights + d.flights)/3 AS PM_3MvAvg,
					
					(a.flights + b.flights + c.flights)/3
						-(b.flights + c.flights + d.flights)/3 AS Diff_3MvAvg,
						
					(a.flights + b.flights + c.flights)/3
						/(b.flights + c.flights + d.flights)/3-1 AS PctChg_3MvAvg,
						
					(a.flights + b.flights + c.flights + d.flights
						+ e.flights + f.flights)/6 AS CM_6MvAvg,
						
					(b.flights + c.flights + d.flights + e.flights
						+ f.flights + g.flights)/6 AS PM_6MvAvg,
						
					(a.flights + b.flights + c.flights + d.flights
							+ e.flights + f.flights)/6
						-(b.flights + c.flights + d.flights + e.flights
							+ f.flights + g.flights)/6 AS Diff_6MvAvg,
							
					(a.flights + b.flights + c.flights + d.flights
							+ e.flights + f.flights)/6
						/(b.flights + c.flights + d.flights + e.flights
							+ f.flights + g.flights)/6-1 AS PctChg_6MvAvg,					
						
						
					(a.flights + b.flights + c.flights + d.flights
						+ e.flights + f.flights + g.flights + h.flights 
						+ i.flights + j.flights + k.flights + l.flights)/12 AS CM_12MvAvg,
						
					(b.flights + c.flights + d.flights + e.flights 
						+ f.flights + g.flights + h.flights + i.flights
						+ j.flights + k.flights + l.flights + m.flights)/12 AS PM_12MvAvg,
						
					(a.flights + b.flights + c.flights + d.flights
							+ e.flights + f.flights + g.flights + h.flights 
							+ i.flights + j.flights + k.flights + l.flights)/12
						- (b.flights + c.flights + d.flights + e.flights 
							+ f.flights + g.flights + h.flights + i.flights
							+ j.flights + k.flights + l.flights + m.flights)/12 AS Diff_12MvAvg,
					
					(a.flights + b.flights + c.flights + d.flights
							+ e.flights + f.flights + g.flights + h.flights 
							+ i.flights + j.flights + k.flights + l.flights)/12
						/(b.flights + c.flights + d.flights + e.flights 
							+ f.flights + g.flights + h.flights + i.flights
							+ j.flights + k.flights + l.flights + m.flights)/12-1 AS PctChg_12MvAvg
								
				FROM AdjFlightData AS a
				LEFT JOIN AdjFlightData AS b
				ON a.Country_ID=b.Country_ID
					AND DATE(a.date)=DATE(b.date, '+1 month')
				LEFT JOIN AdjFlightData AS c
				ON a.Country_ID=c.Country_ID
					AND DATE(a.date)=DATE(c.date, '+2 month')
				LEFT JOIN AdjFlightData AS d
				ON a.Country_ID=d.Country_ID
					AND DATE(a.date)=DATE(d.date, '+3 month')
				LEFT JOIN AdjFlightData AS e
				ON a.Country_ID=e.Country_ID
					AND DATE(a.date)=DATE(e.date, '+4 month')
				LEFT JOIN AdjFlightData AS f
				ON a.Country_ID=f.Country_ID
					AND DATE(a.date)=DATE(f.date, '+5 month')
				LEFT JOIN AdjFlightData AS g
				ON a.Country_ID=g.Country_ID
					AND DATE(a.date)=DATE(g.date, '+6 month')
				LEFT JOIN AdjFlightData AS h
				ON a.Country_ID=h.Country_ID
					AND DATE(a.date)=DATE(h.date, '+7 month')
				LEFT JOIN AdjFlightData AS i
				ON a.Country_ID=i.Country_ID
					AND DATE(a.date)=DATE(i.date, '+8 month')
				LEFT JOIN AdjFlightData AS j
				ON a.Country_ID=j.Country_ID
					AND DATE(a.date)=DATE(j.date, '+9 month')
				LEFT JOIN AdjFlightData AS k
				ON a.Country_ID=k.Country_ID
					AND DATE(a.date)=DATE(k.date, '+10 month')
				LEFT JOIN AdjFlightData AS l
				ON a.Country_ID=l.Country_ID
					AND DATE(a.date)=DATE(l.date, '+11 month')
				LEFT JOIN AdjFlightData AS m
				ON a.Country_ID=m.Country_ID
					AND DATE(a.date)=DATE(m.date, '+12 month')
			;"""

query12 = "DROP TABLE IF EXISTS FinalOutput;"
query13 = """CREATE TABLE FinalOutput AS
				SELECT DISTINCT *
				FROM
					(SELECT DISTINCT a.Country_Id, a.date, Article_Cnt, Blog_Cnt, Other_Cnt, 
						Major_Articles, Total_Cnt, Total_AdjCnt, Rank_Total, Avg_Rank,
						WordCount_Total, Avg_WordCount, Headline_Total, Abstract_Total,
						LeadParagraph_Total, Avg_Sent, Total_Sent, Avg_AdjSent, AdjTotal_Sent
						CM_Flights, PM_Flights, OTMC_Flights, PctChg_Flights, 
						CM_3MvAvg, PM_3MvAvg, Diff_3MvAvg, PctChg_3MvAvg, 
						CM_6MvAvg, PM_6MvAvg, Diff_6MvAvg, PctChg_6MvAvg, 
						CM_12MvAvg, PM_12MvAvg, Diff_12MvAvg, PctChg_12MvAvg
					FROM AdjNYTdata AS a
					LEFT JOIN FlightData_Final AS b
					ON a.country_id=b.country_id
						AND a.date=b.date
					UNION
					SELECT DISTINCT  a.Country_Id, a.date, Article_Cnt, Blog_Cnt, Other_Cnt, 
						Major_Articles, Total_Cnt, Total_AdjCnt, Rank_Total, Avg_Rank,
						WordCount_Total, Avg_WordCount, Headline_Total, Abstract_Total,
						LeadParagraph_Total, Avg_Sent, Total_Sent, Avg_AdjSent, AdjTotal_Sent
						CM_Flights, PM_Flights, OTMC_Flights, PctChg_Flights, 
						CM_3MvAvg, PM_3MvAvg, Diff_3MvAvg, PctChg_3MvAvg, 
						CM_6MvAvg, PM_6MvAvg, Diff_6MvAvg, PctChg_6MvAvg, 
						CM_12MvAvg, PM_12MvAvg, Diff_12MvAvg, PctChg_12MvAvg
					FROM FlightData_Final AS a
					LEFT JOIN AdjNYTdata AS b
					ON a.country_id=b.country_id
						AND a.date=b.date) 
				ORDER BY Country_ID, date
			;"""

c = conn.cursor()
# c.execute(query00)
# c.execute(query01)
# c.execute(query02)
# c.execute(query03)
# c.execute(query04)
# c.execute(query05)
# c.execute(query06)
# c.execute(query07)
# c.execute(query08)
# c.execute(query09)
# c.execute(query10)
# c.execute(query11)
# c.execute(query12)
# c.execute(query13)

df = pd.read_sql_query("""SELECT * FROM FinalOutput;""", conn)
path = '../fixtures/FinalOutput.csv'
save = df.to_csv(path)