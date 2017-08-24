# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 09:22:19 2017

@author: lcao
"""

import os
import pickle
import pandas as pd
import numpy as np


os.chdir('C:\Users\LuCao\Desktop\Fund_Hackathon') # set working directory




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# laod funds mentioned in each txt file
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
with open('FundStat\Funds_Mentioned','rb') as fp:
    funds_mentioned = pickle.load(fp)
print len(funds_mentioned) # 41132 txt files in total




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# construct co-occurrence matrix 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
basic_info = pd.read_excel('Index.xlsx', sheetname = 0)
fund_name = np.array(basic_info[u'基金会名称'])
print len(fund_name) # 605 funds in total


cooc_matrix = np.zeros((len(fund_name), len(fund_name))) # 605 * 605 matrix with 0 in each cell


for i in range(len(funds_mentioned)):
    fund_list = funds_mentioned[i]
    if len(fund_list) >= 2:
        print 'There are ' + str(len(fund_list)) + ' funds in file ' + str(i)
        for j in range(len(fund_list)):
            f1 = fund_list[j]
            idx1 = np.where(fund_name == f1)[0][0]
            for k in range((j+1),len(fund_list)):
                f2 = fund_list[k] 
                idx2 = np.where(fund_name == f2)[0][0]
                if idx1<=idx2:
                    cooc_matrix[idx1, idx2] = cooc_matrix[idx1, idx2] + 1
                else:
                    cooc_matrix[idx2, idx1] = cooc_matrix[idx2, idx1] + 1
                    

with open('FundStat\Funds_Cooccurrence_Matrix','wb') as fp: # write matrix to pickle
    pickle.dump(cooc_matrix,fp)
    



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# compute number of connections for each fund
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
with open('FundStat\Funds_Cooccurrence_Matrix','rb') as fp: # read matrix from pickle
    cooc_matrix = pickle.load(fp)

connection = [0] * len(fund_name)
for i in range(len(fund_name)):
    connection[i] = sum(cooc_matrix[0:(i+1),i]) + sum(cooc_matrix[i,(i+1):cooc_matrix.shape[1]])
    

# append connection to Fund_Stat dataframe
fund_stat = pd.read_csv('FundStat\Fund_Stat.csv')
fund_stat['Connection'] = connection
fund_stat.to_csv('FundStat\Fund_Stat.csv')
    

 
    
