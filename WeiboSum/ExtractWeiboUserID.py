# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:24:02 2017

@author: lcao
"""
import os
import pandas as pd
import numpy as np


# set working directory
os.chdir('C:\Users\lcao\Desktop\Hackathon')


# laod basic information
basic_info = pd.read_excel('Index.xlsx', sheetname = 0)
basic_info.shape # There are 605 funds in total


# extract numerical user id
data = basic_info.loc[basic_info[u'基金会微博'].notnull()]
data.shape # There are 145 funds whose weibo ids are not null
data = data.loc[[data[u'基金会微博'].iloc[i].rsplit('/', 1)[-1].isdigit() \
                             for i in range(data.shape[0])]]
data.shape # There are 87 funds whose weibo ids are numbers
Users_id = [int(data[u'基金会微博'].iloc[i].rsplit('/', 1)[-1]) \
            for i in range(data.shape[0])]
print len(Users_id) # 87


data['User_id'] = Users_id
data['Fund_name'] = [i.encode('utf-8') for i in data[u'基金会名称']]
data[['Fund_name','User_id']].to_csv('Weibo_users_id.csv')


# extract funds with null or non-numerical user id
data2 = basic_info.loc[[n not in np.array(data[u'基金会名称']) for n in basic_info[u'基金会名称']]]
print data2.shape[0] # 518 funds in total
data2['Fund_name'] = [i.encode('utf-8') for i in data2[u'基金会名称']]
data2['Fund_name'].to_csv('Funds_wo_weibo_users_id.csv')
