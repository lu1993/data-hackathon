# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 13:59:29 2017

@author: lcao
"""

import os
import pandas as pd
import numpy as np
import pickle
import requests
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import re


os.chdir('C:\Users\LuCao\Desktop\Fund_Hackathon')  # set working directory




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# count number of funds and news 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
basic_info = pd.read_excel('Index.xlsx', sheetname = 0)
fund_name = basic_info[u'基金会名称']
print len(fund_name) # 605 funds in total


files = [f for f in listdir('TXT') if isfile(join('TXT', f))] # list of files in 新闻内容页.rar
print len(files) # 41132 files in total




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# number of goole search results
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
NumGS = [] 
for i in range(len(fund_name)):
    r = requests.get('http://www.google.com/search',
                     params={'q':fund_name[i]})
    soup = BeautifulSoup(r.text)
    s = soup.find('div',{'id':'resultStats'}).text
    num = [int(ss.replace(',', '')) for ss in s.split() if ss.replace(',', '').isdigit()]
    NumGS.extend(num)
    print 'Get the number of google search result of ' + fund_name[i]
    



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# number of news for each fund
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
funds = []
for i in range(len(files)):
    print 'Search file ' + str(i)
    unicodeText = open(join('TXT', files[i])).read().decode('utf-8')
    matches = []
    for j in range(len(fund_name)):
        pattern = re.compile(fund_name[j], re.UNICODE)
        match = pattern.findall(unicodeText)
        if len(match) != 0:
            matches.extend(match)
    funds.append(list(set(matches)))

print len(funds) # 41132 in total

with open('FundStat\Funds_Mentioned','wb') as fp: # write list of funds mentioned in each file to pickle
    pickle.dump(funds,fp)
    
with open('FundStat\Funds_Mentioned','rb') as fp: # read list of funds mentioned in each file from pickle
    funds_mentioned = pickle.load(fp)
    

NumNews = [] # count number of files(news) for each fund
for i in range(len(fund_name)):
    num = len(np.where(np.array([fund_name[i] in f for f in funds_mentioned]) == True)[0])
    NumNews.extend([num])
    print 'Number of news for ' + fund_name[i] + 'is' + str(num)
    



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 基金会项目数，项目总收入，项目总支出
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
project_info = pd.read_excel('Index.xlsx', sheetname = 4)
NumProject = []
Income = []
Spend = []
for i in range(len(fund_name)):
    sub_project_info = project_info.loc[project_info[u'基金会名称'] == fund_name[i]]
    NumProject.extend([sub_project_info.shape[0]])
    income = [m for m in sub_project_info[u'项目收入'] if (type(m) == int)]
    spend = [n for n in sub_project_info[u'项目支出'] if (type(n) == int)]
    Income.extend([sum(income)])
    Spend.extend([sum(spend)])
    print 'Number of projects for ' + fund_name[i] + 'is ' + str(sub_project_info.shape[0])
  



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 基金会捐赠总额
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
donation_info = pd.read_excel('Index.xlsx', sheetname=3)
DonAmount = []
for i in range(len(fund_name)):
    sub_donation_info = donation_info.loc[donation_info[u'基金会名称'] == fund_name[i]]
    amount = sum(sub_donation_info[u'捐赠金额'])
    DonAmount.extend([amount])
    print 'Amount of donation to ' + fund_name[i] + 'is ' + str(amount)




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 基金会资助总额
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
subsidize_info = pd.read_excel('Index.xlsx', sheetname=5)
SubAmount = []
for i in range(len(fund_name)):
    sub_subsidize_info = subsidize_info.loc[subsidize_info[u'受助单位名称'] == fund_name[i]]
    amount = sum(sub_subsidize_info[u'资助金额'])
    SubAmount.extend([amount])
    print 'Amount of subsidation to ' + fund_name[i] + 'is ' + str(amount)




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 基金会成立时间
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from datetime import datetime
Age = []
for i in range(len(fund_name)):
    start_date = basic_info.loc[basic_info[u'基金会名称'] == fund_name[i]][u'成立时间'].values[0]
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    age = datetime.now() - start_date
    Age.extend([age.days])
    print 'Days to establishment for ' + fund_name[i] + ' are ' + str(age.days)
 
    
    
    
    
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 基金会原始基金，总员工数，志愿者数,专项基金数量,经纬度
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
basic_stat = basic_info[[u'基金会名称', u'原始基金',u'全职员工',u'志愿者数量',
                         u'专项基金数量',u'经度',u'纬度',u'网站地址']]




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# group all features into one file
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
df = {'FundName':fund_name,
      'NumGS':NumGS,
      'NumNews':NumNews,
      'NumProject':NumProject,
      'ProjectIncome':Income, 
      'ProjectSpend':Spend,
      'DonationAmount':DonAmount,
      'SubsidizeAmount':SubAmount,
      'FundAge':Age,
      'NumEmployer':basic_info[u'全职员工'],
      'NumVolunteer':basic_info[u'志愿者数量'],
      'NumSpecialFund':basic_info[u'专项基金数量'],
      'OriginalCapital':basic_info[u'原始基金'],
      'Lon':basic_info[u'经度'],
      'Lat':basic_info[u'纬度'],
      'Sector':basic_info[u'基金会行业领域'],
      'Location':basic_info[u'所在地'],
      'Website':basic_info[u'网站地址']
      }
fund_stat = pd.DataFrame(data = df)
fund_stat['FundName'] = [i.encode('utf-8') for i in fund_stat['FundName']]
fund_stat['Location'] = [i.encode('utf-8') for i in fund_stat['Location']]
fund_stat['Sector'] = [i.encode('utf-8') for i in fund_stat['Sector']] 




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# manually fill NaN latitude and longitude
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
idx = fund_stat.loc[[(x or y) for (x,y) in zip(pd.isnull(fund_stat.Lat), pd.isnull(fund_stat.Lon))]].index
print len(idx)

print fund_stat.loc[idx[0],['FundName','Location','Lat','Lon']]
fund_stat.loc[idx[0],['Lat','Lon']] = [31.3360,120.6173]

print fund_stat.loc[idx[1],['FundName','Location','Lat','Lon']]
fund_stat.loc[idx[1],['Lat','Lon']] = [39.0037,117.7105]

print fund_stat.loc[idx[2],['FundName','Location','Lat','Lon']]
fund_stat.loc[idx[2],['Lat','Lon']] = [30.0819,120.4951]

print fund_stat.loc[idx[3],['FundName','Location','Lat','Lon']]
fund_stat.loc[idx[3],['Lat','Lon']] = [33.5525,119.0271]

print fund_stat.loc[idx[4],['FundName','Location','Lat','Lon']]
fund_stat.loc[idx[4],['Lat','Lon']] = [23.2611,113.8109]

print fund_stat.loc[idx[5],['FundName','Location','Lat','Lon']]
fund_stat.loc[idx[5],['Lat','Lon']] = [33.2942,118.8732]

print fund_stat.loc[idx,['FundName','Location','Lat','Lon']]


fund_stat.to_csv('FundStat\Fund_Stat.csv', index = False)




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# province for each fund
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Fund_Stat = pd.read_csv('FundStat\Fund_Stat.csv')
Location = np.array(Fund_Stat.Location)
Provinces = pd.read_csv('FundStat\Province.csv')
Provinces = np.array(Provinces[Provinces.columns.values[0]])

matches = []
for i in range(len(Location)):
    count = 0
    for j in range(len(Provinces)):
        pattern = re.compile(Provinces[j], re.UNICODE)
        match = pattern.findall(Location[i])
        if len(match) != 0:
            count = count + 1
            matches.extend([match[0]])
        if len(match) > 1: # check if thare are multi-matches in single location
            print i
            print match
    if count >1: # check if single fund matches multi-provinces
        print i
        
        
print len(np.where(matches=='')[0]) # check if there are null values

Fund_Stat['Province'] = matches
Fund_Stat.to_csv('FundStat\Fund_Stat.csv',index=False)




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# number of unique sector 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import string

sectors = []
regex = re.compile(r'[%s\s]+' % re.escape(string.punctuation))

for i in range(Fund_Stat.shape[0]):
    
    s = np.array(Fund_Stat.Sector)[i]
    clean_s = re.sub(ur"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-]+", ",", s.decode("utf8"))     # replace unicode punctuation with utf-8 punctuation
    list_s = regex.split(clean_s) # split string by punctuation
    sectors.extend(list_s)

sectors_set = set(sectors)
print len(sectors_set) # 28 kinds of sectors in total


df = pd.DataFrame({'Sectors':list(sectors_set)}) # export sectors set to csv file
df['Sectors'] = [i.encode('utf-8') for i in df['Sectors']]
df.to_csv('FundStat\Sector.csv',index=False)




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# label encode sector and province
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
provinces = pd.read_csv('FundStat\Province.csv')
sectors = pd.read_csv('FundStat\Sector.csv')
Fund_Stat = pd.read_csv('FundStat\Fund_Stat.csv')


SectorNum = []
ProvinceNum = []
for i in range(Fund_Stat.shape[0]):
    pNum = np.where(np.array(provinces[provinces.columns.values[0]])== Fund_Stat.Province.iloc[i])[0][0] + 1
    ProvinceNum.extend([pNum])
    
    s = np.array(Fund_Stat.Sector)[i]
    clean_s = re.sub(ur"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：；《）《》“”()»〔〕-]+", ",", s.decode("utf8"))
    list_s = regex.split(clean_s)
    
    sNum = [(np.where(np.array(sectors[sectors.columns.values[0]])==x.encode('utf-8'))[0][0] + 1) for x in list_s]
    SectorNum.append(sNum)
   

SectorStr = [','.join(str(e) for e in sn) for sn in SectorNum] # convert list to string
Fund_Stat['SectorNum'] = SectorStr
Fund_Stat['ProvinceNum'] = ProvinceNum
Fund_Stat.to_csv('FundStat\Fund_Stat.csv',index=False)



































