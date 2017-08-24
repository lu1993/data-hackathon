# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:18:40 2017

@author: lcao
"""
import pandas as pd
from WeiboSpyder import weibo

Users_id = pd.read_csv('WeiboStat\Weibo_users_id.csv')
Users_id = Users_id['User_id']
print len(Users_id)


for i in range(2,len(Users_id)):
    #使用实例,输入一个用户id，所有信息都会存储在wb实例中		
    user_id = Users_id[i] #可以改成任意合法的用户id（爬虫的微博id除外）
    filter = 1 #值为0表示爬取全部的微博信息（原创微博+转发微博），值为1表示只爬取原创微博
    wb = weibo(user_id,filter) #调用weibo类，创建微博实例wb
    wb.start() #爬取微博信息
    print '用户名：' + wb.userName
    print '全部微博数：' + str(wb.weiboNum)
    print '关注数：' + str(wb.following)
    print '粉丝数：' + str(wb.followers)
    #print '最新一条微博为：' + wb.weibos[0] #若filter=1则为最新的原创微博，如果该用户微博数为0，即len(wb.weibos)==0,打印会出错，下同
    #print '最新一条微博获得的点赞数：' + str(wb.num_zan[0])
    #print '最新一条微博获得的转发数：' + str(wb.num_forwarding[0])
    #print '最新一条微博获得的评论数：' + str(wb.num_comment[0])
    wb.writeTxt() #wb.writeTxt()只是把信息写到文件里，大家可以根据自己的需要重新编写writeTxt()函数

    if i == 0:
        df = pd.DataFrame(data={'User_name':[wb.userName],
                                'User_id':[str(user_id)],
                                'Num_post':[wb.weiboNum],
                                'Num_original_post':[wb.weiboNum2],
                                'Num_following':[wb.following],
                                'Num_follower':[wb.followers],
                                'Num_comment':[sum(wb.num_comment)],
                                'Num_forward':[sum(wb.num_forwarding)],
                                'Num_good':[sum(wb.num_zan)]})
    else:
        df2 = pd.DataFrame(data={'User_name':[wb.userName],
                                 'User_id':[str(user_id)],
                                 'Num_post':[wb.weiboNum],
                                 'Num_original_post':[wb.weiboNum2],
                                 'Num_following':[wb.following],
                                 'Num_follower':[wb.followers],
                                 'Num_comment':[sum(wb.num_comment)],
                                 'Num_forward':[sum(wb.num_forwarding)],
                                 'Num_good':[sum(wb.num_zan)]})
        df = df.append(df2, ignore_index = True)
        
df.to_csv('WeiboStat\Weibo_Stat.csv')




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# get df data from weibo txt files
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from os import listdir
from os.path import isfile, join
files = [f for f in listdir('Weibo') if isfile(join('Weibo', f))]
print len(files)

import csv
for i in range(len(files)):
    with open(join('Weibo', files[i])) as f:
        reader = csv.reader(f)
        row1 = next(reader)
        row2 = next(reader) # User_name
        row3 = next(reader) # User_id
        row4 = next(reader) # Num_post
        row5 = next(reader) # Num_folloing
        row6 = next(reader) # Num_follower
        row7 = next(reader) # Num_comment
        row8 = next(reader) # Num_forward
        row9 = next(reader) # Num_good