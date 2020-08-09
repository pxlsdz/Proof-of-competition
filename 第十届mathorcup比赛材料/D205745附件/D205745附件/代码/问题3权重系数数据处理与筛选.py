#!/usr/bin/env python
# coding: utf-8

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')
data=pd.read_csv("all.csv")
data.head()
list=[]
for index,row in data.iterrows():
    list.append([row[1],row[2],row[3],row[4],row[6],row[8],row[9],0)
    

name=["classid","skc","date_rcd","s","price","ie","discount","predict"]
all=pd.DataFrame(columns=name,data=list)
all.to_csv("all_list.csv")    

item=set()
for it in list:
    item.add(it[0])
#筛选小类周数据
from collections import defaultdict
item_dict=defaultdict(int)
class_list=[]
T=104
l=1
r=104
num=0
MAPE=0
name=["0classid","1skc","2date_rcd","3s","4price","5ie","6discount","7predict"]
for classid in item:
    l=0
    for i in range(0,len(list)):
        if int(list[i][0])==int(classid):
            l=i
            break
    temp=l
    for i in range(1,104+1):
        
        l=temp
        l+=i
        s=0
        price=0
        kucun=0
        tag=0
        cnt=0
        
        while(l<=len(list) and int(list[l-1][0])==int(classid)):
            cnt+=1
            if i<92:
                item_dict[list[l-1][1]]+=s
            s+=list[l-1][3]
            price+=list[l-1][4]
            kucun+=list[l-1][5]
            tag+=list[l-1][4]/list[l-1][6]
            l+=104
        if price==0:
            discount=0
        else:
            discount=tag/price
        
        class_list.append([classid,i,price/cnt,kucun,discount,s])
        
name=["classid","date_rcd","price","ie","discount","s"]
all=pd.DataFrame(columns=name,data=class_list)
all.to_csv("BP_class_week.csv")    

#读取目标小类周数据的预测结果
data=pd.read_csv("PSO_BP_class_week_result.csv")
data.head()


class_dict=defaultdict(int)
class_d=defaultdict(int)
for index,row in data.iterrows():
    class_dict[str(int(row[1]))+","+str(int(row[2]))]=row[7]
 
    if row[2]<92:
        class_d[str(int(row[1]))]+=row[6]
    

#依旧权重系数计算目标小类的所有skc
BP_list=[]
T=104
l=1
r=104
num=0
MAPE=0
name=["0classid","1skc","2date_rcd","3s","4price","5ie","6discount","7predict"]
while l<=len(list):
    cnt=0
    mape=0.0
    for i in range(r-12+1,r+1):
        w=item_dict[list[i-1][1]]/class_d[str(int(list[i-1][0]))]
        list[i-1][7]=w*class_dict[str(int(list[i-1][0]))+","+str(i-l)]
        mape+=abs(list[i-1][3]-list[i-1][7])/list[i-1][3]
        if list[i-1][3]==0:
            cnt+=1
    if cnt>=1:
        l+=T
        r+=T
        continue
       
    cnt=0
    for i in range(l,r-12+1):
        if list[i-1][5]!=0:
            cnt+=1

    if cnt>20:
        MAPE+=mape/12
        for i in range(l,r+1):
            BP_list.append([list[i-1][0],list[i-1][1],list[i-1][2],list[i-1][4],list[i-1][5],list[i-1][6],list[i-1][3],list[i-1][7],mape/12])
        num+=1
    l+=T
    r+=T
print(num)
print(MAPE/264)          


name=["classid","skc","date_rcd","price","ie","discount","s","predict","MAPE"]
all=pd.DataFrame(columns=name,data=BP_list)
all.to_csv("PSO_BP_calss_skc_result.csv")    

data=pd.read_csv("PSO_BP_calss_skc_result.csv")
data.head()
#画图可视化
plt.figure(figsize=(12, 6),facecolor='snow')
 
plt.rcParams['font.sans-serif']=['Microsoft YaHei']
T=104
x = data["date_rcd"][T-12:T]
y1 = data["s"][T-12:T]
y2 = data["predict"][T-12:T]

plt.plot(x,y1,label='真实销售量',linewidth=3,mfc='w',markersize=12,mfcalt='b') 
plt.plot(x,y2,label='预测销售量',color='r',marker='*',linewidth=2)
#plt.vlines(0, 0, 0.5, colors = "r", linestyles = "dashed")
#plt.axvline(x=x[92],ls="--",c="green")#添加垂直直线

# x轴标签
plt.xlabel('日期/周',fontdict={'size'   : 16})
# y轴标签
plt.ylabel('销售量',fontdict={'size'   : 16})

# 可视化图标题
plt.title('skc596572119262的周预测模型结果',fontdict={'size'   : 16})

# 显示图例
plt.legend(prop={ 'size'   : 16})
plt.xticks(rotation=45)
plt.show()





