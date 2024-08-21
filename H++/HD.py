#!/users/40413353/soft/miniconda3/envs/Py27_AmberTools23/bin/python
# Filename: HD.py

# 2024/05/08 created
# @ Jun

# reference
# https://www.cnblogs.com/pennyy/p/4248934.html

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--prefix", type=str, required=True, help="input the prefix title, for example -p http://newbiophysics.cs.vt.edu/H++/uploads/Jun/0.15_80_10_pH6.5_FL62-reduce/")
parser.add_argument("-f", "--file", type=str, required=True, help="input the file name, for example -f name.txt")
# eg:
# HD.py -p http://newbiophysics.cs.vt.edu/H++/uploads/Jun/0.15_80_10_pH6.5_FL62-reduce/ -f name.txt
# python HD.py -p http://newbiophysics.cs.vt.edu/H++/uploads/Jun/0.15_80_10_pH6.5_FL62-reduce/ -f name.txt
# I believe it is unecessary to record a log.
# HD.py -p http://newbiophysics.cs.vt.edu/H++/uploads/Jun/0.15_80_10_pH6.5_FL62-reduce/ -f name.txt > record.log
# python HD.py -p http://newbiophysics.cs.vt.edu/H++/uploads/Jun/0.15_80_10_pH6.5_FL62-reduce/ -f name.txt > record.log

args = parser.parse_args()
prefix = args.prefix
file = args.file

before_downloading = os.listdir('./')

with open(file, 'r') as f:
    data = f.readlines()

download_number = len(data)
print(str(download_number) + ' files should be downloaded from H++ server.')

px = "wget "
work = []
for i in data:
    i = i.replace('\n','')
    i = px + prefix + '/' + i
    os.system(i)

all_files = os.listdir('./')
for i in before_downloading:
    all_files.remove(i)

count = 0
if download_number != len(all_files):
    print('Not every file is sucessfully downloaded, following files are missing, please check.')
    print('Also pay attention that wget will rename the downloading file if there is a file with same name.')
    for i in data:
        i = i.replace('\n','')
        if i not in all_files:
            count += 1
            print(i)
    print('There are ' + str(count) + ' missing files.')
else:
    print(str(download_number) + ' flies have been downloaded, the downloaded file number matches the request.')




