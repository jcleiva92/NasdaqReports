# -*- coding: utf-8 -*-

import pandas as pd
import urllib
from bs4 import BeautifulSoup
from collections import OrderedDict

def get_Income_Statement(symbol):
	fname=symbol+'-Income-Statement'

	menu_Base="Ingrese el tipo de periodo: \n"
	menu='\n 1. Annual'
	menu+='\n 2. Quarterly'
	menu+='\n Opcion: '
	while True:
		period_type=raw_input(menu_Base+menu)
		if period_type not in ['1','2']:
			menu_Base='\nHa ingresado un tipo de periodo no valido!!! (Los tipos de periodo van del 1 al 2)\n'
		else: break
	
	url=r'http://www.nasdaq.com/symbol/'+symbol+'/financials?query=income-statement'
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
	m_Index='Revenues'
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
	df.to_csv(fname)
	
if __name__=='__main__':
	print get_Income_Statement('ibm')