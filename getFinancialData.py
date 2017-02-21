# -*- coding: utf-8 -*-

import pandas as pd
from bs4 import BeautifulSoup
from download_Data import get_Data
from utils import report_type_Menu


if __name__=='__main__':
	reports,symbol=report_type_Menu()
	repo_Dict={'1':'income-statement',
			   '2':'balance-sheet',
			   '3':'cash-flow',
			   '4':'ratios'
				}
	for report in reports:
		get_Data(symbol,repo_Dict[report])