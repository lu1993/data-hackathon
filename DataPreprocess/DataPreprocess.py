# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 11:58:22 2017

@author: LuCao
"""

import os
import pandas as pd
import numpy as np



os.chdir('C:\Users\LuCao\Desktop\Fund_Hackathon')  # set working directory



# import data
full_data = pd.read_excel('DataPreprocess\Full_Data.xlsx')




# log transform data based on data exploration
sub_full_data = full_data[['NumGS','NumNews','Connection','Num_follower',
                           'Num_following','Num_original_post','Num_post',
                           'Num_forward','Num_comment','Num_good']]
           
full_data_transform = sub_full_data.apply(lambda x:np.log(x+1), axis = 1)




# normalize data and convert data to score with min 0 and max 10
full_data_transform = full_data_transform.apply(lambda x:np.round(10*(x - np.min(x))/(np.max(x) - np.min(x)),2))
full_data_transform[['FundName','ProvinceNum','SectorNum','Lat','Lon','Website']] = full_data[['FundName','ProvinceNum','SectorNum','Lat','Lon','Website']]




# export data
full_data_transform.to_excel('Shiny\My_Shiny\data\Full_Data.xlsx', sheet_name = 'Sheet1')

