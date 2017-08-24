# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 16:00:47 2017

@author: lcao
"""

import pandas as pd
import numpy as np
import os
import re


# set working directory
os.chdir('D:\Personal\Hackathon\WeiboSum')


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# import statistical data of weibo 
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
weibo_stat_1 = pd.read_csv('WeiboStat\Weibo_Stat_1.csv')
weibo_stat_2 = pd.read_csv('WeiboStat\Weibo_Stat_2.csv')
weibo_stat = weibo_stat_1.append(weibo_stat_2)
print weibo_stat_1.shape
print weibo_stat_2.shape
print weibo_stat.shape




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# clean statistical data of weibo
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
weibo_stat.head(1)

# check number of unique funds to detect duplicates
print len(weibo_stat.User_name.values) 




'''
check number of NaN
check with WeiboSpyderImplement.py again to see if we can retrieve data from weibo
If not, remove null fund names from weibo_stat
'''
idx = np.where(np.array(pd.isnull(weibo_stat.User_name))==True)[0]
print len(idx) 
Users_id = np.array(weibo_stat.iloc[idx]['User_id']) 




'''
replace NaN data if new data is retrieved
'''
weibo_stat_3 = pd.read_csv('WeiboStat\Weibo_Stat_3.csv')
for i in range(weibo_stat_3.shape[0]):
    user_id = weibo_stat_3.User_id.iloc[i]
    weibo_stat.iloc[np.where(np.array(weibo_stat['User_id'])==user_id)[0][0]] = weibo_stat_3.iloc[i]
weibo_stat = weibo_stat.loc[[not x for x in pd.isnull(weibo_stat.User_name)]]
print weibo_stat.shape




'''
check number of fund names end with numbers (suspicious)
check if these user ids are institution ids
'''
M = [re.search(ur'\d+$', x) for x in np.array(weibo_stat.User_name)]
B = [m is None for m in M]
weibo_stat = weibo_stat.ix[B]
print weibo_stat.shape
            
            
        
        
'''
append fund name to weibo_stat
'''
weibo_user_id1 = pd.read_csv('WeiboStat\Weibo_users_id_1.csv')
weibo_user_id2 = pd.read_csv('WeiboStat\Weibo_users_id_2.csv')
weibo_user_id = weibo_user_id1.append(weibo_user_id2)
print weibo_user_id1.shape
print weibo_user_id2.shape
print weibo_user_id.shape


# left outer join weibo_stat and weibo_user_id by user_id
temp = pd.merge(weibo_stat,weibo_user_id[['User_id','Fund_name']],how='left',on='User_id')
temp.head(1)
temp.shape
temp.drop(temp.columns[0], axis=1, inplace=True)
temp.to_csv('WeiboStat\Weibo_Stat.csv', index = False)



















        