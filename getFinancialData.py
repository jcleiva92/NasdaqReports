# -*- coding: utf-8 -*-

import pandas as pd
import urllib
from bs4 import BeautifulSoup

def get_Reports_Type(t_reports):

	if ',' in t_reports:
		t_reports=t_reports.split(',')
		
	for t_report in t_reports:
		if t_report not in ['1','2','3','4']:
			return False
	return t_reports

def get_Income_Statement(symbol):
	print 'Income'

def get_Balance_Sheet(symbol):
	menu_Base="Ingrese el tipo de periodo: \n"
	menu='\n 1. Annual'
	menu+='\n 2. Quartely'
	menu+='\n Opcion: '
	while True:
		period_type=raw_input(menu_Base+menu)
		if period_type not in ['1','2']:
			menu_Base='\nHa ingresado un tipo de periodo no valido!!! (Los tipos de periodo van del 1 al 2)\n'
		else: break
	
	url=r'http://www.nasdaq.com/symbol/' + symbol+'/financials?query=balance-sheet'
	if period_type=='2':url+=r'&data=quarterly'
	html=urllib.urlopen(url).read()
	soup=BeautifulSoup(html,"html.parser")
	table_head=soup.find_all('h3',class_='table-headtag')[0].contents[0]
	table_head=table_head.strip()[:table_head.strip().find(')')+1]
	print table_head
	tags=soup('table')
	
		
	
	print 'Balance',url
	
def get_Cash_Flow(symbol):
	print 'Cash'
	
def get_Financial_Ratios(symbol):
	print 'Ratios'

def chose_Report(symbol,t_reports):

	result={'1':get_Income_Statement,
			'2':get_Balance_Sheet,
			'3':get_Cash_Flow,
			'4':get_Financial_Ratios}
		 
	for t_report in t_reports:
		result[t_report](symbol)
	
	
if __name__=='__main__':
	symbol=raw_input("Escriba el simbolo de la compania: ")
	menuBase="Ingrese el numero segun tipo de informe (si desea varios separelos con una coma) "
	menu="\n 1. Income Statement"
	menu+="\n 2. Balance Sheet"
	menu+="\n 3. Cash Flow"
	menu+="\n 4. Financial Ratios \n\n"
	menu+="Opcion: "
	
	while True:
		report_type=raw_input(menuBase+menu)
		report_type=get_Reports_Type(report_type)
		if not report_type:
			menuBase='\nHa ingresado un tipo de informe no valido!!! (Los tipos de informe van del 1 al 4)\n'
		else:
			break
	chose_Report(symbol,report_type)