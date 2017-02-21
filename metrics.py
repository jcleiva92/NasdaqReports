# -*- coding: utf-8 -*-

import pandas as pd
import urllib
from bs4 import BeautifulSoup
from utils import *

def get_Market_Book_Ratio(market_Value_Equity,book_Value_Equity):
	book_Value_Equity=book_Value_Equity.apply(to_Int)
	return market_Value_Equity/book_Value_Equity
	
def get_Market_Value_of_Equity(symbol):
	share_Price=get_Share_Price(symbol)
	shares_Outstanding=get_Shares_Outstanding(symbol)
	market_Value=shares_Outstanding*share_Price
	return market_Value/1000.00 #Valores en miles

def get_Share_Price(symbol):
	url=r'http://www.nasdaq.com/symbol/{0}/stock-report'.format(symbol)
	html=urllib.urlopen(url).read()
	soup=BeautifulSoup(html,"html.parser")
	price=soup.find('div',class_='qwidget-dollar').contents[0]
	return to_Double(price)
	
def get_Shares_Outstanding(symbol):
	url=r'http://www.nasdaq.com/symbol/{0}/stock-report'.format(symbol)
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

def net_Working_Capital(current_Assets,current_Liabilities):
	current_Assets=current_Assets.apply(to_Int)
	current_Liabilities=current_Liabilities.apply(to_Int)
	netWorkingCap=current_Assets-current_Liabilities
	netWorkingCap=netWorkingCap.apply(to_Cash)
	return netWorkingCap

def get_EPS(net_Income,shares_Outstanding):
	net_Income=net_Income.apply(to_Int)*1000.00
	eps=net_Income/shares_Outstanding
	return eps
	
def get_Balance_Metrics(df,symbol):
	netWorkingCap=net_Working_Capital(df.ix[('Current Assets','Total Current Assets')],df.ix[('Current Liabilities','Total Current Liabilities')])
	df.ix[('Metrics','Net Working Capital'),:]=netWorkingCap
	marketValueEquity=get_Market_Value_of_Equity(symbol)
	df.ix[('Metrics','Market Value of Equity'),:]= to_Cash(marketValueEquity)
	df.ix[('Metrics','Price to Book Ratio'),:]=get_Market_Book_Ratio(marketValueEquity,df.ix[('Stock Holders Equity','Total Equity'),:])
	df.ix[('Metrics','Enterprise Value (TEV)'),:]=get_Enterprise_Value(marketValueEquity,df.ix[('Current Liabilities','Short-Term Debt / Current Portion of Long-Term Debt'),:],df.ix[('Current Liabilities','Long-Term Debt'),:],df.ix[('Current Assets','Cash and Cash Equivalents'),:]).apply(to_Cash)
	return df

def get_Income_Metrics(df,symbol):
	shares_Outstanding=get_Shares_Outstanding(symbol)
	df.ix[('Metrics','Earnings per Share'),:]=get_EPS(df.ix[('Operating Expenses','Net Income'),:],shares_Outstanding)
	return df
	
if __name__=='__main__':
	print 'hola'