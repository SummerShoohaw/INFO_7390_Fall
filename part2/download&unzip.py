# imports
import urllib.request as rq
import re
import ssl
import zipfile
import os
from bs4 import BeautifulSoup

# download .zip file from website
def downloading(year):
    year = str(year)
    url_total = 'https://www.sec.gov/files/EDGAR_LogFileData_thru_Jun2017.html'

    ssl._create_default_https_context = ssl._create_unverified_context
    response = rq.urlopen(url_total)

    res_total = r'www.sec.gov/dera/data/Public-EDGAR-log-file-data/'+year+'/Qtr[0-9]/log[0-9]+01\.zip'
    lst = re.findall(res_total,response.read().decode('utf-8'))

    for i in range(len(lst)):
        url = 'https://'+lst[i]
        month = str(i+1)
        filename = year+"_"+month+"_01.zip"
        response = rq.urlopen(url,context = ctt)
        rq.urlretrieve(url,filename)

# un-zip files
def un_zip(year,month):
    year = str(year)
    month = str(month)
    file_name = year+'_'+month+'_01.zip'
    folder_path = year + '_' + month + "_01"
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    for names in zip_file.namelist():
        zip_file.extract(names,folder_path + '/')
    zip_file.close()

#TEST: download all files in year 2016
downloading(2016)
#TEST: un zip file '2016_1_01.zip'(just downloaded) to folder '2016_1_01'
un_zip(2016,1)
