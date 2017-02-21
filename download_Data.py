# -*- coding: utf-8 -*-

import pandas as pd
import urllib
from bs4 import BeautifulSoup
from metrics import *
from utils import *


def get_Data(symbol,report):
	
	if report=='balance-sheet': 
		fname=symbol+'-Balance-Sheet'
	elif report=='income-statement':
		fname=symbol+'-Income-Statement'
	elif report=='cash-flow':
		fname=symbol+'-Cash-Flow'
	else:
		fname=symbol+'-Ratios'
		
	url=r'http://www.nasdaq.com/symbol/{0}/financials?query={1}'.format(symbol,report)
	
	if report!='ratios':
		period_type=get_Period_type()
	
	if period_type=='2':url+=r'&data=quarterly'
	
	html=urllib.urlopen(url).read()
	soup=BeautifulSoup(html,"html.parser")
	
	columns=[]
	t_Headers=soup.find('thead')
	
	for row in t_Headers.find_all('tr'):
		for col in row.find_all('th'):
			if col.contents: columns.append(col.contents[0])
	if 'Trend' in columns: columns.remove('Trend')
	
	if period_type=='1': 
		titles=columns[1:]
		fname+='-annual.csv'
	else:
		titles=columns[6:]
		fname+='-quarterly.csv'
	
	contents=soup.find_all('table',class_='')[3]
	results=[]
	
	if report=='income-statement': m_Index='Revenues'
	elif report=='cash-flow': m_Index='Income'
	
	for row in contents.find_all('tr')[1:]:
		for col in row.find_all('th'):
			if col.contents: 
				index=col.contents[0]
		values=[]
		if row.find_all('td',attrs={'class':''}):
			for con in row.find_all('td',attrs={'class':''}): 
				if con.find_all('table'): continue
				if con.contents: values.append(con.contents[0])					
			if values: 
				results.append([m_Index,index,values])
		else:
			m_Index=index
	
	g_Index=[]
	for i in range(len(results)):
		g_Index.append((results[i][0],results[i][1]))
	
	g_Index = pd.MultiIndex.from_tuples(g_Index, names=['Clase', 'Cuenta (Valores en miles)'])
	vals=[]
	for i in range(len(results)):
		vals.append(results[i][2])

	df=pd.DataFrame(vals,index=g_Index,columns=titles)
	if report=='balance-sheet': 
		df=get_Balance_Metrics(df,symbol)
	if report=='income-statement':
		df=get_Income_Metrics(df,symbol)
	df.to_csv(fname)

if __name__=='__main__':
	get_Data('ibm','income-statement')
	get_Data('ibm','balance-sheet')