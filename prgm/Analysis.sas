filename data "X:\Python\travel-trends\fixtures\FinalOutput2.csv";

data data (keep=Country_ID date Article_Cnt Blog_Cnt Other_Cnt
		Major_Articles Total_Cnt Total_AdjCnt Rank_Total Avg_Rank
		WordCount_Total Avg_WordCount Headline_Total Abstract_Total
		LeadParagraph_Total Avg_Sent Total_Sent Avg_AdjSent CM_Flights  
		PM_Flights OTMC_Flights PctChg_Flights);
	infile data delimiter=',' dsd truncover firstobs=2;
	input Country_ID :$2. date :mmddyy. Article_Cnt :best12. 
		Blog_Cnt :best12. Other_Cnt :best12. Major_Articles :best12.
		Total_Cnt :best12. Total_AdjCnt :best12. Rank_Total :best12.
		Avg_Rank :best12. WordCount_Total :best12. Avg_WordCount :best12. 
		Headline_Total :best12. Abstract_Total :best12. LeadParagraph_Total :best12. 
		Avg_Sent :best12. Total_Sent :best12. Avg_AdjSent :best12. CM_Flights :best12. 
		PM_Flights :best12. OTMC_Flights :best12. PctChg_Flights :best12. 
		CM_3MvAvg :best12. PM_3MvAvg :best12. Diff_3MvAvg :best12. 
		PctChg_3MvAvg :best12. CM_6MvAvg :best12. PM_6MvAvg :best12. 
		Diff_6MvAvg :best12. PctChg_6MvAvg :best12. CM_12MvAvg :best12. 
		PM_12MvAvg :best12. Diff_12MvAvg :best12. PctChg_12MvAvg :best12.;;
run;

proc sql noprint;
	select CATS('SUM(,', compress(name), ') AS ', compress(name))
		into :sum_slct separated by ','
		from dictionary.columns
		where libname='WORK'
			and memname='DATA'
			and name not in ('Country_ID', 'date')
		;
	create table columns as
		select compress(name) as name
		from dictionary.columns
		where libname='WORK'
			and memname='DATA'
			and name not in ('Country_ID', 'date')
		;
quit;

proc sql;
	create table Adj_Data as
		select Country_ID, date, &sum_slct
		from data
		group by Country_ID, date
	;
quit;

data _null_;
	set columns end=fin;
	file 'X:\Python\travel-trends\prgm\SasMacros\MvgAvg12.txt';
	if _n_=1 then
		put 'PROC SQL;' /
			'CREATE TABLE data_12MvAvg AS' /
				'SELECT cm.Country_ID, put(cm.Date, mmddyy.) AS Date';
	j=0;
	new_name1 = compress(name||'_12Cnt');
	put ', SUM(';
	do while(j<=11);
		if j=0 then
			put '		cm.' name ' IS NOT NULL';
		else put '		, pm' j '.' name 'IS NOT NULL';
		if j=11 then
			put '	) AS ' new_name1;
		j = j + 1;
	end;
	i=0;
	new_name2 = compress(name||'_12MvAvg');
	put ', MEAN(';
	do while(i<=11);
		if i=0 then
			put '		cm.' name;
		else put '		, pm' i '.' name;
		if i=11 then
			put '	) AS ' new_name2;
		i = i + 1;
	end;
	n = 0;
	if fin then do while(n<=11);
		if n=0 then
			put 'from Data as cm';
		else
			put 'left join Data as ' 'pm' n /
				'on cm.Country_ID=pm' n '.Country_ID' /
				'AND cm.date=intnx("month",' 'pm' n'.date,' n ')';
		if n=11 then
			put 'GROUP BY cm.Country_ID' /
				'ORDER BY cm.Country_ID, cm.Date;' /
				'QUIT;';
		n=n+1;
	end;
run;

%include 'X:\Python\travel-trends\prgm\SasMacros\MvgAvg12.txt';
