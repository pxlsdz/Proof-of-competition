#!/usr/bin/env python
# coding: utf-8
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')

prod=pd.read_csv("data/附件2：prod_info.csv")
inv=pd.read_csv("data/附件3：inv_info.csv")
prod.head()
#二维字典的添加
def addtwodimdict(thedict, key_a, key_b, val):
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a:{key_b: val}})    


from collections import defaultdict
prod_dict={}

for ind,row in prod.iterrows():
    prod_dict[row["skc"]]=[row["tiny_class_code"],row["tag_price"]]


sale=pd.read_csv("data/附件1：sale_info.csv")
sale.head()

from datetime import datetime

def cal(time):
    format = '%Y-%m-%d'
    time=str(time)[0:10]
    return datetime.strptime(time, format)

class_dict={}
for ind,row in sale.iterrows():
    if( cal(row["date_rcd"])>cal("2019-10-01") or cal(row["date_rcd"])<cal("2019-06-01")):
        continue
    #print(row)
    try:
        if prod_dict[row["skc"]][0] not in class_dict:
            class_dict[prod_dict[row["skc"]][0]]=[[row["skc"],row["date_rcd"],row["s"],row["real_cost"]]]
        else:
            class_dict[prod_dict[row["skc"]][0]].append([row["skc"],row["date_rcd"],row["s"],row["real_cost"]])
    except KeyError:
        pass

data_list=[]
for key,val in class_dict.items():
    summ=0
    for it in val:
        summ+=it[3]
    data_list.append([key,summ])
data_list.sort(key=lambda x:x[1],reverse=True)
data_list[0:10]
inv=pd.read_csv("data/附件3：inv_info.csv")
inv.head()

inv_dict=defaultdict(int)
temp_dict=defaultdict(int)
for ind,row in inv.iterrows():
    inv_dict[str(row["skc"])+","+str(row["date_rcd"][0:7])]+=row["ie"]
    temp_dict[row["skc"]]=1

from datetime import datetime
#获取月时间
def cal1(time):
    format = '%Y-%m'
    return datetime.strptime(time, format)


class_dict={}
for ind,row in sale.iterrows():
    try:
        if prod_dict[row["skc"]][0] not in class_dict:
            class_dict[prod_dict[row["skc"]][0]]=[[row["skc"],row["date_rcd"],row["s"],row["real_cost"]]]
        else:
            class_dict[prod_dict[row["skc"]][0]].append([row["skc"],row["date_rcd"],row["s"],row["real_cost"]])
    except KeyError:
        pass


#历史销售时间处于 2019 年 6 月 1 日至 2019 年 10 月 1 日内的小类销售记录
data=[[] for i in range(0,11)]
item=set()
i=0
for it in data_list:
    i+=1
    if i>=11:break
    class_dict[it[0]].sort(key=lambda x:cal(x[1]))
    s=0
    price=0
    pre=class_dict[it[0]][0][1][:7]
    for row in class_dict[it[0]]:
        #print(row[1][:7])
        item.add(row[0])
        if cal1(row[1][:7])==cal1(pre):
            s+=row[2]
            price+=row[3]
        else:
           
            kucun=0
            tag=0
            for id in item:
                tag+=prod_dict[id][1]
                kucun+=inv_dict[str(id)+","+str(pre)]
            tag/=len(item)
            
            data[i].append([it[0],pre,s,price,price/s,tag,kucun,price/s/tag])
            s=row[2]
            price=row[3]
            pre=row[1][:7]
            item=set()
    kucun=0
    tag=0
    for id in item:
        tag+=prod_dict[id][1]
        kucun+=inv_dict[str(id)+","+str(pre)]
    tag/=len(item)
    data[i].append([it[0],pre,s,price,price/s,tag,kucun,price/s/tag])
    s=row[2]
    price=row[3]
    pre=row[1][:7]
    item=set()
        

name=["classid","date_rcd","s","real_cost","price","tag_price","ie","discount"]
for i in range(1,11):
    all=pd.DataFrame(columns=name,data=data[i])
    all.to_csv("问题2/"+str(i)+"_new.csv")   


name=["classid","date_rcd","s","real_cost","price","tag_price","ie","discount"]
all_list=[]
for i in range(1,11):  
    for j in data[i]:
        all_list.append(j)
all=pd.DataFrame(columns=name,data=all_list)
all.to_csv("问题2/all.csv") 


#判断时间是第几周
import datetime
def cal_week(y,m,d):
    y=int(y)
    m=int(m)
    d=int(d)
    be = int(datetime.datetime(2018, 12, 31).strftime("%W"))
    if y<2019:
        return int(datetime.datetime(y, m, d).strftime("%W"))
    return be+int(datetime.datetime(y, m, d).strftime("%W"))

#根据周获取时间
def week2date(n,w):
    be = int(datetime.datetime(2018, 12, 31).strftime("%W"))
    if n<=be:
        y=2018
    else:
        y=2019
        n-=be
    wk = str(y)+'-W'+str(n)+'-'+str(w)
    return str(datetime.datetime.strptime(wk, '%Y-W%W-%w'))[0:10]

inv_dict=defaultdict(int)
for ind,row in inv.iterrows():
    inv_dict[str(row["skc"])+","+str(row["date_rcd"])]+=row["ie"]


def tran(time):
    format = '%Y-%m-%d'
    time=str(time)[0:10]
    return datetime.datetime.strptime(time, format)
tran("2018-01-01")

#获取目标小类内所有 skc 的周数据
data=[[] for i in range(0,11)]
item=set()
i=0
for it in data_list:
    i+=1
    if i>=11:break
    class_dict[it[0]].sort(key=lambda x:tran(x[1]))
    item=set()
    for row in class_dict[it[0]]:
        item.add(row[0])
    
    for id in item: 
        s=0
        price=0
        num=1
        
        for row in class_dict[it[0]]:
            if row[0]!=id:continue
            if cal_week(row[1][:4],row[1][5:7],row[1][8:10])==num:
                s+=row[2]
                price+=row[3]
            elif cal_week(row[1][:4],row[1][5:7],row[1][8:10])==num+1:
                kucun=0
                tag=0
                tag=prod_dict[id][1]
                for t in range(1,7+1):
                    x=t
                    if t==7:x=0
                    kucun+=inv_dict[str(id)+','+str(week2date(num,x))]
                single=0.0
                if s==0:
                    single=0
                else:
                    single=price/s
                data[i].append([it[0],row[0],num,s,price,single,tag,kucun,single/tag])
                s=row[2]
                price=row[3]
                num+=1
            else:
                while(num<cal_week(row[1][:4],row[1][5:7],row[1][8:10])):
                    kucun=0
                    tag=0
                    tag=prod_dict[id][1]
                    for t in range(1,7+1):
                        x=t
                        if t==7:x=0
                        kucun+=inv_dict[str(id)+','+str(week2date(num,x))]
                    single=0.0
                    if s==0:
                        single=0
                    else:
                        single=price/s
                    data[i].append([it[0],row[0],num,s,price,single,tag,kucun,single/tag])
                    s=0
                    price=0
                    num+=1    
                s=row[2]
                price=row[3]
                
            
        while num<=104:
            kucun=0
            tag=0
            tag=prod_dict[id][1]
            for t in range(1,7+1):
                x=t
                if t==7:x=0
                kucun+=inv_dict[str(id)+','+str(week2date(num,x))]
            single=0.0
            if s==0:
                single=0
            else:
                single=price/s
            data[i].append([it[0],id,num,s,price,single,tag,kucun,single/tag])
            s=0
            price=0
            num+=1  

name=["classid","ksc","date_rcd","s","real_cost","price","tag_price","ie","discount"]
all_list=[]
for i in range(1,11):  
    for j in data[i]:
        all_list.append(j)
all=pd.DataFrame(columns=name,data=all_list)
all.to_csv("问题3/all.csv") 


print(len(all_list))


data=[[] for i in range(0,11)]
item=set()
i=0
summ=0
for it in data_list:

    i+=1
    if i>=11:break
    print(it[0])
    print(it[0])
    class_dict[it[0]].sort(key=lambda x:tran(x[1]))
    item=set()
    for row in class_dict[it[0]]:
        item.add(row[0])
    summ+=len(item)
print(summ)        

        

import scipy.io as sio 
import matplotlib.pyplot as plt 
import numpy as np 
import scipy.io as scio
skc = [i[1] for i in all_list]
data=[[i[5],i[7],i[8]] for i in all_list]
s = [i[3] for i in all_list]
sio.savemat('all.mat', {'input':data,'output':s ,'skc': skc}) 



