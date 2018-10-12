# imports
import urllib.request as rq
import re
import ssl
import zipfile
import os
import numpy as np
import pandas as pds
import logging as lg


#logging functions
def logging_setup():
	# please re-check the filename here, especially the folder path!!!!!!
	lg.basicConfig(filename = './log'+year+'.log',format = '[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]',level = lg.INFO, filemode = 'a', datefmt = '%Y-%m-%d %I:%M:%S %p')


yr = input("Please input the YEAR：")
if yr > 2017 or yr < 2003:
	lg.critical('Year should between 2003-2017')
	os._exit(0)
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



#download zip files
lg.info('start downloading zip files')
downloading()
lg.info('downloading finished! :D')


#un_zip files into folder: ./extract_year/...
lg.info('start unzip files')
un_zip()
lg.info('unzip successfully')

#data download and un_zip finished!!
#will start data cleaning below

def read_data_from_filename(filename):
	table = pds.read_csv(filename,low_memory=False)
	return table

def get_most_freq_time():
    table_copy['datetime'] = table_copy['date'] + ' ' + table_copy['time']
    pds.to_datetime(table_copy['datetime'])
    df_time_as_index = table_copy.set_index('datetime',drop=True)
    df_time_as_index.index = pds.to_datetime(df_time_as_index.index)
    period = df_time_as_index.to_period('H')
    datetime_freq = pds.value_counts(period.index)
    most_freq_datetime = datetime_freq.to_timestamp().index[0]
    return most_freq_datetime

def get_random_zero_or_one(column_name):
    total_counts = pds.value_counts(table_copy[column_name])
    ratio_of_index1 = total_counts[0]/row_counts
    random_number = random.randint(0,10)
    if random_number <= ratio_of_index1 * 10:
        return total_counts.index[0]
    else:
        return 1 - total_counts.index[0]
    
def replaceAll_outlier_withNaN():
    table_copy['noagent'] = np.where(np.abs(table_copy['noagent'] - 0.5) != 0.5,np.nan,table_copy['noagent'])
    table_copy['norefer'] = np.where(np.abs(table_copy['norefer'] - 0.5) != 0.5,np.nan,table_copy['norefer'])
    table_copy['crawler'] = np.where(np.abs(table_copy['crawler'] - 0.5) != 0.5,np.nan,table_copy['crawler'])
    table_copy['idx'] = np.where(np.abs(table_copy['idx'] - 0.5) != 0.5,np.nan,table_copy['idx'])
    table_copy['size'] = np.where(table_copy['size'] > 10000000,np.nan,table_copy['size'])
    #find outliers
    list_0_to_10 = np.arange(11)
    check_find = np.logical_not(np.isin(table_copy['find'],list_0_to_10))
    table_copy['find'] = np.where(check_find,np.nan,table_copy['find'])
    #browser outliers
    list_browser = ['mie','fox','saf','chr','sea','opr','oth','win','mac','lin','iph','ipd','and','rim','iem']
    check_browser = np.logical_not(np.isin(table_copy['browser'],list_browser))
    table_copy['browser'] = np.where(check_browser,np.nan,table_copy['browser'])
    #code outliers
    list_httpcode = [100,101,102,200,201,202,203,204,205,206,207,208,226,300,301,302,303,304,305,306,307,308,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,420,421,422,423,424,425,426,428,429,431,444,450,451,494,500,501,502,503,504,505,506,507,508,510,511]
    check_code = np.logical_not(np.isin(table_copy['code'],list_httpcode))
    table_copy['code'] = np.where(check_code,np.nan,table_copy['code'])
    
def drop_replace_nan():
    table_copy = table_copy.dropna(subset=['ip','cik','accession','extention'])
    mean_of_size = np.mean(table_copy['size'])
    fill_values = {'datetime':most_freq_datetime,'zone':0,'code':200,'size': mean_of_size,'idx':1,'browser':'ukn','norefer':get_random_zero_or_one('norefer'),'noagent':get_random_zero_or_one('noagent'),'crawler':get_random_zero_or_one('crawler'),'find':0}
    table_copy = table_copy.fillna(value=fill_values)




#create a list of filenames according to year, not finished
#be careful about the path of filename!!!!!!!!!!
#specify the file path here with its filename, e.g. : ./folder_name/folder_name/filename
filename_list = []

#loop through the filename_list and do the data cleaning
for filename in filename_list:
	#read data first
	table_copy = read_data_from_filename(filename)

	#calculate the length of the table
	row_counts = len(table_copy.index)

	#replace all outliers with NaN
	replaceAll_outlier_withNaN()

	#remove or replace NaN values
	drop_replace_nan()

	#delete date column and time column
	not finished

	#save the table into a new csv file
	not finished


































