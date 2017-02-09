# -*- coding: utf-8 -*-

import pandas as pd
import urllib
from bs4 import BeautifulSoup
from collections import OrderedDict

def get_Market_Book_Ratio(market_Value_Equity,book_Value_Equity):
	book_Value_Equity=book_Value_Equity.apply(to_Int)
	return market_Value_Equity/book_Value_Equity
	
def get_Market_Value_of_Equity(symbol):
	share_Price=get_Share_Price(symbol)
	shares_Outstanding=get_Shares_Outstanding(symbol)
	market_Value=shares_Outstanding*share_Price
	return market_Value/1000.00 #Valores en miles

def to_Double(my_String):
	my_String=my_String.replace('$','')
	my_String=my_String.replace(',','')
	deci_Pos=len(my_String)-len(my_String[:my_String.find('.')])-1
	my_String=my_String.replace('.','')
	my_Float=float(my_String)
	for i in range(deci_Pos): my_Float=my_Float/10.00
	return my_Float

def get_Share_Price(symbol):
	url=r'http://www.nasdaq.com/symbol/'+symbol+'/stock-report'
	html=urllib.urlopen(url).read()
	soup=BeautifulSoup(html,"html.parser")
	price=soup.find('div',class_='qwidget-dollar').contents[0]
	return to_Double(price)
	
	
def get_Shares_Outstanding(symbol):
	url=r'http://www.nasdaq.com/symbol/'+symbol+'/stock-report'
	html=urllib.urlopen(url).read()
	soup=BeautifulSoup(html,"html.parser")
	table=soup.find('table',class_='marginB5px')
	th_Tags=table.find_all('tr')[3]
	shares_Outstanding=th_Tags.find_all('td')[1].contents[0]
	shares_Outstanding=to_Double(shares_Outstanding)
	return shares_Outstanding

def get_Enterprise_Value(marketValueEquity,shortDebt,longDebt,cash):
	shortDebt=shortDebt.apply(to_Int)
	longDebt=longDebt.apply(to_Int)
	cash=cash.apply(to_Int)
	return marketValueEquity+shortDebt+longDebt-cash
	
def get_Balance_Sheet(symbol):

	fname=symbol+'-Balance-Sheet'

	menu_Base="Ingrese el tipo de periodo: \n"
	menu='\n 1. Annual'
	menu+='\n 2. Quarterly'
	menu+='\n Opcion: '
	while True:
		period_type=raw_input(menu_Base+menu)
		if period_type not in ['1','2']:
			menu_Base='\nHa ingresado un tipo de periodo no valido!!! (Los tipos de periodo van del 1 al 2)\n'
		else: break
	
	url=r'http://www.nasdaq.com/symbol/'+symbol+'/financials?query=balance-sheet'
	if period_type=='2':url+=r'&data=quarterly'
	
	html=urllib.urlopen(url).read()
	soup=BeautifulSoup(html,"html.parser")
	
	table_head=soup.find_all('h3',class_='table-headtag')[0].contents[0]
	table_head=table_head.strip()[:table_head.strip().find(')')+1]
	'''table_head'''	
	
	columns=[]
	t_Headers=soup.find('thead')
	
	for row in t_Headers.find_all('tr'):
		for col in row.find_all('th'):
			if col.contents: columns.append(col.contents[0])
	if 'Trend' in columns: columns.remove('Trend')
	'''columns'''
	if period_type=='1': 
		titles=columns[1:]
		fname+='-annual.csv'
	else:
		titles=columns[6:]
		fname+='-quarterly.csv'
	
	contents=soup.find_all('table',class_='')[3]
	results=[]
	
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
	netWorkingCap=net_Working_Capital(df.ix[('Current Assets','Total Current Assets')],df.ix[('Current Liabilities','Total Current Liabilities')])
	
	df.ix[('Metrics','Net Working Capital'),:]=netWorkingCap
	marketValueEquity=get_Market_Value_of_Equity(symbol)
	df.ix[('Metrics','Market Value of Equity'),:]= to_Cash(marketValueEquity)
	df.ix[('Metrics','Price to Book Ratio'),:]=get_Market_Book_Ratio(marketValueEquity,df.ix[('Stock Holders Equity','Total Equity'),:])
	df.ix[('Metrics','Enterprise Value (TEV)'),:]=get_Enterprise_Value(marketValueEquity,df.ix[('Current Liabilities','Short-Term Debt / Current Portion of Long-Term Debt'),:],df.ix[('Current Liabilities','Long-Term Debt'),:],df.ix[('Current Assets','Cash and Cash Equivalents'),:]).apply(to_Cash)
	df.to_csv(fname)

def net_Working_Capital(current_Assets,current_Liabilities):
	current_Assets=current_Assets.apply(to_Int)
	current_Liabilities=current_Liabilities.apply(to_Int)
	netWorkingCap=current_Assets-current_Liabilities
	netWorkingCap=netWorkingCap.apply(to_Cash)
	return netWorkingCap
	
def to_Int(my_String):
	my_String=my_String.replace('$','').replace(',','')
	return int(my_String)

def to_Cash(my_Int):
	parenthesis=False
	if my_Int<0:
		parenthesis=True
		my_Int=str(my_Int)[1:]
	else:
		my_Int=str(my_Int)
	decima=0
	if '.' in my_Int:
		decima=my_Int[my_Int.find('.'):]
		my_Int=my_Int[:my_Int.find('.')]
		
	val=''
	i=len(my_Int)-1
	j=0
	while i >=0:
		if (not j%3) and (j>0):
			val+=','
		val+=my_Int[i]
		if i==0:
			val+='$'
		i-=1
		j+=1
	val=val[::-1]
	if decima:
		val+=decima
	if parenthesis: 
		val='('+val+')'
	return val
	
if __name__=='__main__':
	print get_Balance_Sheet('ibm')