"""
Created on Wed Apr 22 21:08:36 2020

@author: Jerry
"""
import pandas as pd
import numpy as np
import re
import jieba
from sklearn.model_selection import train_test_split                #划分训练/测试集
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB     # 从sklean.naive_bayes里导入朴素贝叶斯模型
from sklearn.preprocessing import StandardScaler
from xgboost.sklearn import XGBClassifier
import lightgbm as lgb
import xgboost as xgb    
from bayes_opt import BayesianOptimization
from bayes_opt.util import Colours
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.metrics import roc_auc_score,precision_score,recall_score,f1_score,roc_curve,auc,accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore") 
import os,json,pickle
from sklearn.externals import joblib
from sklearn.calibration import CalibratedClassifierCV



# 中文分词函数，用正则去除多余的符号
def cut_text(text):
    text = str(text)
    stopwords = [line.strip() for line in open('chinese_stopwords.txt',encoding='UTF-8').readlines()]
    text = ''.join(re.findall('[\u4e00-\u9fff]', text))
    seg_list = jieba.cut(text)            
    sentence_segment=[] 
    for word in seg_list:
        if word not in stopwords:
            sentence_segment.append(word)
    #sentence_segment.append(word)        
    # 把已去掉停用词的sentence_segment，用' '.join()拼接起来
    seg_res = ' '.join(sentence_segment)
    return seg_res


def get_sentiment(txt, model = None):
    """ 获取文本情感
    :param txt: 输入的文本
    :return: 情感分析的结果，json格式
    """
    text = str(txt)
    text = cut_text(text)
    text_matrix = tfidf_vec.transform([text])
    text_pred = model.predict(text_matrix)
    text_prod = model.predict_proba(text_matrix)
    #print('预测结果',test_model_pred)
    #print(np.argmax(test_model_pred)) 
    if text_prod[0][0] > text_prod[0][1]:
        sentiment_label = 0
        sentiment_classification = '负面情感'
    else:
        sentiment_label = 1
        sentiment_classification = '正面情感'
    negative_prob = str(text_prod[0][0])
    positive_prob = str(text_prod[0][1])
    result = {'text':txt,
              'sentiment_label':sentiment_label,
              'sentiment_classification':sentiment_classification,
              'negative_prob':negative_prob,
              'positive_prob':positive_prob}
    return json.dumps(result, ensure_ascii=False) 


       
if __name__ == "__main__":
    # 读取分词文件
    data = pd.read_csv('seg_ratings_data.txt',sep='\t')    
    # TfidfVectorizer 是 CountVectorizer + TfidfTransformer的组合，输出的各个文本各个词的TF-IDF值
    # min_df=5, max_features=10000
    tfidf_vec = TfidfVectorizer(max_features=10000) 
    tfidf_matrix = tfidf_vec.fit_transform(data['comment'].astype('U'))   
    
    # 加载模型文件
    svc_model = joblib.load('2_svc_model.pkl')

    # 测试获取输入文本的情感
    text = '这店怎么这样了。第二次来吃，我买的套餐是5碟牛肉，最后只上了4碟，问老板娘，说已经改了只给4碟，没有这个套餐了。那我买这个券这个套餐，份量不给足我？ 你说改了就改了，我都不知情，那不你突然想加收就加收？那我买这个套餐写明有这些东西，那你一样也不能少，无论是什么时候买的，券都没有过期，难道我10年前买保险，10年后就不承认了？这等同于欺骗。以后不会再来，店铺没规律，没有诚信，只会做得越来越差，本来看着老板娘都是沙溪人就算了，免得在店铺里念叨。'
    get_sentiment(text, model = svc_model)


"""
|   iter    |  target   |   expC    |
-------------------------------------
|  1        |  0.9306   |  0.383    |
|  2        |  0.9296   |  1.244    |
|  3        |  0.9299   |  0.8755   |
|  4        |  0.9295   |  1.571    |
|  5        |  0.9295   |  1.56     |
|  6        |  0.9311   |  0.06607  |
=====================================
Final result: {'target': 0.9310559330642265, 'params': {'expC': 0.06607344051840425}}
精度:0.861
召回:0.861
f1-score:0.861
accuracy_scores:0.861
AUC:0.933
"""
# lsvc_c = LinearSVC()

# lsvc_c.fit(X_train, y_train)
# # lsvc_y_pred为预测类别，lsvc_y_prod为预测类别的概率
# lsvc_y_pred = lsvc_c.predict(X_test)
# lsvc_y_prod = lsvc_c.decision_function(X_test)

# # 展示模型的各个评分
# lsvc_ms = metrics_result(y_test, lsvc_y_pred, lsvc_y_prod)


# #3.使用朴素贝叶斯进行训练
# mnb = MultinomialNB()   # 使用默认配置初始化朴素贝叶斯
# mnb.fit(X_train,y_train)    # 利用训练数据对模型参数进行估计
# mnb_y_pred = mnb.predict(X_test)     # 对参数进行预测
# mnb_y_prod = mnb.predict_proba(X_test)[:,1]

# # 展示模型的各个评分
# mnb_ms = metrics_result(y_test, mnb_y_pred, mnb_y_prod)
# # 














