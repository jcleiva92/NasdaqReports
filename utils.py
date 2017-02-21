# -*- coding: utf-8 -*-

import pandas as pd
from bs4 import BeautifulSoup

def to_Double(my_String):
	my_String=my_String.replace('$','')
	my_String=my_String.replace(',','')
	deci_Pos=len(my_String)-len(my_String[:my_String.find('.')])-1
	my_String=my_String.replace('.','')
	my_Float=float(my_String)
	for i in range(deci_Pos): my_Float=my_Float/10.00
	return my_Float

def get_Period_type():

	menu_Base="Ingrese el tipo de periodo: \n"
	menu='\n 1. Annual'
	menu+='\n 2. Quarterly'
	menu+='\n Opcion: '
	while True:
		period_type=raw_input(menu_Base+menu)
		if period_type not in ['1','2']:
			menu_Base='\nHa ingresado un tipo de periodo no valido!!! (Los tipos de periodo van del 1 al 2)\n'
		else: break
	
	return period_type

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

def get_Reports_Type(t_reports):

	if ',' in t_reports:
		t_reports=t_reports.split(',')
		
	for t_report in t_reports:
		if t_report not in ['1','2','3','4']:
			return False
	return t_reports
	
def report_type_Menu():
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
	return report_type,symbol
	
if __name__=='__main__':
	print 'hola'