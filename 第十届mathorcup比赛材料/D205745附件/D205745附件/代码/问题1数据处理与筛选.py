#!/usr/bin/env python
# coding: utf-8
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')

sale=pd.read_csv("data/附件1：sale_info.csv")
sale.head()

from datetime import datetime
# 时间转换函数
def cal(time):
    format = '%Y-%m-%d'
    time=str(time)[0:10]
    return datetime.strptime(time, format)


#获取符合题目要求的数据，目标 skc 为销售时间处于 2018 年 7 月 1日至 2018 年 10 月 1 日
skc_dict={}
for ind,row in sale.iterrows():
    if( cal(row["date_rcd"])<cal("2018-07-01") or cal(row["date_rcd"])>cal("2018-10-01")):
        continue
    if row["skc"] not in skc_dict:
        skc_dict[row["skc"]]=[[row["date_rcd"],row["s"],row["real_cost"]]]
    else:
        skc_dict[row["skc"]].append([row["date_rcd"],row["s"],row["real_cost"]])


#累计销售额排名前 50 的 skc
data_list=[]
for key,val in skc_dict.items():
    summ=0
    for it in val:
        summ+=it[2]
    data_list.append([str(key),summ])
data_list.sort(key=lambda x:x[1],reverse=True)


prod=pd.read_csv("data/附件2：prod_info.csv")
inv=pd.read_csv("data/附件3：inv_info.csv")
holiday=pd.read_csv("data/附件4：holiday_info.csv")


prod.head()


#二维字典的添加
def addtwodimdict(thedict, key_a, key_b, val):
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a:{key_b: val}})    



from collections import defaultdict
prod_dict={}
#获取skc的类信息与原价
for ind,row in prod.iterrows():
    prod_dict[row["skc"]]=[row["tiny_class_code"],row["tag_price"]]

inv.head()
#获取skc的库存信息
inv_dict={}
temp_dict=defaultdict(int)
for ind,row in inv.iterrows():
    addtwodimdict(inv_dict,row["skc"],row["date_rcd"],row["ie"])
    temp_dict[row["skc"]]=1



#累计销售额排名前 50 的 skc
item=set()
i=0
for it in data_list:
    if temp_dict[int(it[0])]==1:
        i+=1
        item.add(it[0])
        if i>=50:break
print(len(item))

dict=defaultdict(int)
for it in item:
    dict[str(it)]=1
    
print(inv.dtypes)
print(prod.dtypes)
print(sale.dtypes)

#2018 年国庆节，双十一，双十二和元旦这四个节假日销售记录
data=[]
for ind,row in sale.iterrows():
    if dict[str(row["skc"])] ==1:
        try:
            if( cal(row["date_rcd"])<=cal("2018-10-07") and cal(row["date_rcd"])>=cal("2018-10-01")):#国庆

                data.append([row["skc"],row["date_rcd"],row["s"],row["real_cost"],prod_dict[row["skc"]][1],inv_dict[row["skc"]][row["date_rcd"]]])

            if( cal(row["date_rcd"])==cal("2018-11-11")):#双十一
                data.append([row["skc"],row["date_rcd"],row["s"],row["real_cost"],prod_dict[row["skc"]][1],inv_dict[row["skc"]][row["date_rcd"]]])

            if( cal(row["date_rcd"])==cal("2018-12-12")):#双十二
                data.append([row["skc"],row["date_rcd"],row["s"],row["real_cost"],prod_dict[row["skc"]][1],inv_dict[row["skc"]][row["date_rcd"]]])

            if( cal(row["date_rcd"])<=cal("2019-01-01") and cal(row["date_rcd"])>=cal("2018-12-30")):#元旦
                data.append([row["skc"],row["date_rcd"],row["s"],row["real_cost"],prod_dict[row["skc"]][1],inv_dict[row["skc"]][row["date_rcd"]]])
        except KeyError:
            pass 

name=["skc","date_rcd","s","real_cost","tag_price","ie"]
all=pd.DataFrame(columns=name,data=data)
all.to_csv("问题1.csv")


name=["skc","总销售额"]
all=pd.DataFrame(columns=name,data=data_list[:50])
all.to_csv("50.csv")

all=[]
for it in data:
    all.append([it[0],it[1],it[2],it[3],it[4],it[5],it[3]/it[2]/it[4],it[3]/it[2]])
name=["skc","date_rcd","s","real_cost","tag_price","ie","discount","price"]
all=pd.DataFrame(columns=name,data=all)
all.to_csv("问题1_all.csv")    

#条形图
# 指定默认字体
plt.rcParams['font.sans-serif'] = ['SimHei']  

# 解决保存图像是负号'-'显示为方块的问题 
plt.rcParams['axes.unicode_minus'] = False  
sns.set(font='SimHei')  # 解决Seaborn中文显示问题


data = pd.read_csv("all.csv",encoding="GBK")
data.head()


#散点图绘制
#plt.figure(figsize=(30, 10)) 
fig,axes=plt.subplots(1,3,figsize=(12,6)) 
#plt.subplots_adjust(，wspace =1, hspace =1)
plt.subplots_adjust(wspace =0.5,hspace =0.5)
sns.regplot(x='库存量',y='销售量',data=data,
            color='r',marker='+',ax=axes[0], fit_reg=False)


sns.regplot(x='折扣',y='销售量',data=data,
            color='g',marker='+',ax=axes[1],fit_reg=False)

sns.regplot(x='售价',y='销售量',data=data,
            color='g',marker='+',ax=axes[2],fit_reg=False)
