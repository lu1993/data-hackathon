# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 09:30:23 2017

@author: lcao
"""

import os
import pandas as pd


os.chdir('C:/Users/LuCao/Desktop/Fund_Hackathon') # set working directory




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# import fund stat and weibo stat data
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
fund_data = pd.read_csv('FundStat/Fund_Stat.csv')
weibo_data = pd.read_csv('WeiboSum/WeiboStat/Weibo_Stat.csv')

fund_data.columns.values
weibo_data.columns.values

fund_data.head(1)
weibo_data.head(1)

fund_data.shape[0] # 605
weibo_data.shape[0] # 192




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# left merge data by FundName 
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
weibo_data.columns.values[-1] = 'FundName'
weibo_data.columns = weibo_data.columns.values

full_data = pd.merge(fund_data, weibo_data, how='left', on='FundName')

# replace NaN data with 0
full_data[weibo_data.columns.values] = full_data[weibo_data.columns.values].fillna(0)




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# export data 
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
full_data.to_csv('DataPreprocess/Full_Data.csv', index=False)
