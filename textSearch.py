#!/usr/bin/env python

# This script is for scan a given folder, search the first line contain the given pattern in each file under the given folder, 
# Then shows the file name and the whole line which contains the pattern

# usage: python3 textSearch.py
# create: 2023/11/1
# author: Yi Jie

import os, re

path = "/Users/mayijie/git/zrobot/zRobot_WSAPI/libraries/pl/"
pattern = "TC_TITLE"

for file in os.listdir(path):
    file_path = os.path.join(path, file)
    target_line = ""
    file_name = ""

    if os.path.isdir(file_path):
        print("folder: ", file_path)
    else:
        # print("file: ", file_path)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if re.search(pattern, line) != None:
                    target_line = line.strip().split(':')[-1]
                    break
    file_name = file_path.split('/')[-1]


    print (file_name + target_line)