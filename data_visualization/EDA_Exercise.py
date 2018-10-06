# import requests, BeautifulSoup, pandas
from bs4 import BeautifulSoup
import requests
import pandas as pd

#select all tables from a specific website and get all elements from these tables by BeautifulSoup
url = 'https://ucr.fbi.gov/crime-in-the-u.s/2016/crime-in-the-u.s.-2016/topic-pages/tables/table-1'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')
tables = soup.select('table')

#read HTML content as DataFrame by function called read_heml provided by pandas
#pd.read_html is a simply way to parse html
#function prettify() can transfrom BeautifulSoup's data type to String，because the arguments of function pd.read_html must be String
df_list = []
for table in tables:
    df_list.append(pd.concat(pd.read_html(table.prettify())))
df = pd.concat(df_list)

#export csv.file
df.to_csv('/Users/G/Documents/2018_Fall/DataScience/GitProject_7390/dataExtraction.csv',index=False)
    
