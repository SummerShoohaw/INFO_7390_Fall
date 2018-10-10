# imports
import urllib.request as rq
import re
import ssl
import zipfile
import os
from bs4 import BeautifulSoup


yr = input("Please input the YEAR：")
year = str(yr)
# download .zip file from website
def downloading():
    url_total = 'https://www.sec.gov/files/EDGAR_LogFileData_thru_Jun2017.html'

    ssl._create_default_https_context = ssl._create_unverified_context
    response = rq.urlopen(url_total)

    res_total = r'www.sec.gov/dera/data/Public-EDGAR-log-file-data/'+year+'/Qtr[0-9]/log[0-9]+01\.zip'
    lst = re.findall(res_total,response.read().decode('utf-8'))
    for i in range(len(lst)):
        url = 'https://'+lst[i]
        month = str(i+1)
        filename = year+"_"+month+"_01.zip"
        rq.urlretrieve(url,filename)

# un-zip files
def un_zip():
    for i in range(12):
        month = str(i+1)
        file_name = year+'_'+month+'_01.zip'
        folder_path = 'extract_'+year
        zip_file = zipfile.ZipFile(file_name)
        if os.path.isdir(folder_path):
            pass
        else:
            os.mkdir(folder_path)
        for names in zip_file.namelist():
            zip_file.extract(names,folder_path + '/')
        zip_file.close()

downloading()
un_zip()
