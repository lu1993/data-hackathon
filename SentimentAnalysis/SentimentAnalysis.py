# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 08:54:20 2017

@author: lcao
"""
import os
from os.path import join
import re
import jieba
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


filepath = 'D:/Personal/Hackathon/SentimentAnalysis'
filename = 'temp_weibo.txt'
os.chdir(filepath)




# 读取整个文件
unicodeText = open(join(filepath, filename)).read().decode('utf-8')
unicodeText = re.findall(ur'[\u4e00-\u9fff]+',unicodeText)
corpus = []
for line in unicodeText:
    corpus.append(" ".join(jieba.cut(line.split(',')[0], cut_all=False)))
    
   
    
    
# 根据词的重要性打分
joined_corpus = [" ".join(corpus)]
vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(joined_corpus)
print tfidf.shape
tfidf_score = tfidf.toarray()[0]
words = vectorizer.get_feature_names()
score = pd.DataFrame(data = {'word':words, 'score':tfidf_score})  
uni_word = [u'转发',u'点赞数',u'评论',u'长微博',u'新浪',u'文字版']
score = score.loc[[x not in uni_word for x in np.array(score.word)]]
score = score.sort_values(by=['score'], ascending=False)




# 构造情感词字典
filename = 'sentiment_words.txt'
senDict = {}
for x in open(join(filepath, filename),'r').readlines():
    if x.strip() != '':
        senDict[x.strip().split(" ")[0].decode('utf-8')] = float(x.strip().split(" ")[1])




# 构造否定词List
filename = 'not_words.txt'
notList = []
for x in open(join(filepath, filename),'r').readlines():
    if x.strip() != '':
        notList.extend([x.strip().decode('utf-8')])




# 构造程度字典
filename = 'degree_words.txt'
degDict = {}
count = 0
score = 0
set_score = False
for x in open(join(filepath, filename), 'r').readlines():
    if x.strip() != '':
        if len(x.strip().split("."))>1:
            if x.strip().split(".")[0].isdigit():
                if int(x.strip().split(".")[0]) == 1:
                    score = 2
                    set_score = True
                if int(x.strip().split(".")[0]) == 2:
                    score = 1.25
                    set_score = True
                if int(x.strip().split(".")[0]) == 3:
                    score = 1.2
                    set_score = True
                if int(x.strip().split(".")[0]) == 4:
                    score = 0.8
                    set_score = True
                if int(x.strip().split(".")[0]) == 5:
                    score = 0.5
                    set_score = True
                if int(x.strip().split(".")[0]) == 6:
                    score = 1.5
                    set_score = True
        if (len(x.strip().split("."))==1) and set_score:
            degDict[x.strip().split(" ")[0].decode('utf-8')] = score
            count = count + 1




# 计算微博的情感度得分
W = 1
M = 1
score = np.nan
Sen_Score = []
for sen in corpus:
    sen_split = sen.split(" ")
    for word in sen_split:
        if word in senDict.keys() and word not in notList and word not in degDict.keys():
            score = senDict[word]
            sen_score = W * M * score
            Sen_Score.extend([sen_score])
            # reset
            W = 1
            M = 1
            score = np.nan
        elif word in notList and word not in degDict.keys():
            W = -1
        elif word in degDict.keys():
            M = degDict[word]
            
if(len(Sen_Score)>1):
    np.mean(Sen_Score)

    
