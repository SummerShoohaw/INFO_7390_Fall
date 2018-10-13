import pandas
import csv

df = pandas.DataFrame([1,2,3],[4,5,6])
import os
path = "./test"
if os.path.isdir(path):
    pass
else: os.mkdir(path)
df.to_csv("./test/test.csv", index = False, header = True)

df1 = pandas.read_csv("./test/test.csv")
print(df1)
