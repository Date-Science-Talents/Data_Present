#!/usr/bin/env python
# coding: utf-8

# In[2]:


#import data
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os 
print(os.getcwd())
data = pd.read_csv(os.getcwd()+'/cleaned_data.csv')
dataP = np.array(data)


# In[46]:


#transfer time

import time

size = [1,dataP.shape[0]]
timee = np.zeros(shape = size)
for i in range(dataP.shape[0]):
    timeArray = time.strptime(dataP[i,1], "%Y/%m/%d %H:%M")
    timee[:,i] = timeArray.tm_yday
    
    
dataR = np.hstack((dataP,timee.T))

#initialize variables
cntN = 0
cntO = []
user = []
dicN = {}
dicO = {}


#find distinct user
for i in range(dataR.shape[0]):
    if(dataR[i,2] not in user):
        user.append(dataR[i,2])
        condition = np.where(dataR[:,2] == dataR[i,2])[0]
        dataT = dataR[condition]
#first time
        timeS = dataT[-1,-1]
        timeE = int(timeS) + 7
        cnttO = 0
        temp = 0
        
#find the very first time recorded of each user        
        for j in range(dataT.shape[0]):
#find the 7-days before
            if(int(dataT[j,-1]) <= int(timeE)):
                cntN += 1
            
#sum before7 individually            
                if(dataT[j,6] not in dicN.keys()):
                    dicN[dataT[j,6]] = 1 
                else:
                    dicN[dataT[j,6]] += 1
#find the 7-days after
            else:
                temp = int(dataT[j,-1])
                cnttO += 1
                
#sum after7 individually
                if(dataT[j,6] not in dicO.keys()):
                    dicO[dataT[j,6]] = 1
               
                else:
                    dicO[dataT[j,6]] += 1
        cntO.append(cnttO/(temp - int(dataT[-1,-1])))
    else:
        continue

#AVG
print('Every single new user use',cntN/(7*len(user)),'times of the platform each day')
print('Every single old user use',np.sum(cntO)/len(user),'times of the platform each day')

#top10 activities for new/old seperately
print('The Top10 activities for new users:',sorted(dicN.items(),key=lambda item:item[1])[-10:])
print('The Top10 activities for old users:',sorted(dicO.items(),key = lambda item:item[1])[-10:])
    
fig, ax1 = plt.subplots(2,1,figsize=(15,15))

v=[]
l=[]
for i in range(10):
    v.append(sorted(dicN.items(),key=lambda item:item[1])[-10:][i][1])
    l.append(sorted(dicN.items(),key=lambda item:item[1])[-10:][i][0])



# ax1[0].pie(v, labels=l, autopct='%.1f%%', pctdistance=0.7, shadow=True, startangle=90)
# ax1[0].axis('equal') # 等价于 ax1.set(aspect='euqal')，使得饼图在figure窗口放大缩小的过程中，保持圆形不变。

# ax1[0].set_title('pie chart of the top 10 popular activities for new users', fontsize = 20)


# ax1[1].barh(range(len(v)), v, tick_label=l)

# ax1[1].set_title('bar chart of the top 10 popular activities for new users', fontsize = 20)
# ax1[1].set_xlabel('times', fontsize = 15)




v=[]
l=[]
for i in range(10):
    v.append(sorted(dicO.items(),key=lambda item:item[1])[-10:][i][1])
    l.append(sorted(dicO.items(),key=lambda item:item[1])[-10:][i][0])


ax1[0].pie(v, labels=l, autopct='%.1f%%', pctdistance=0.7, shadow=True, startangle=90)
ax1[0].axis('equal') # 等价于 ax1.set(aspect='euqal')，使得饼图在figure窗口放大缩小的过程中，保持圆形不变。

ax1[0].set_title('pie chart of the top 10 popular activities for old users', fontsize = 20)


ax1[1].barh(range(len(v)), v, tick_label=l)

ax1[1].set_title('bar chart of the top 10 popular activities for old users', fontsize = 20)
ax1[1].set_xlabel('times', fontsize = 15)


plt.show()



# In[47]:


fig, ax1 = plt.subplots(2,1,figsize=(15,15))
v=[]
l=[]
for i in range(10):
    v.append(sorted(dicN.items(),key=lambda item:item[1])[-10:][i][1])
    l.append(sorted(dicN.items(),key=lambda item:item[1])[-10:][i][0])



ax1[0].pie(v, labels=l, autopct='%.1f%%', pctdistance=0.7, shadow=True, startangle=90)
ax1[0].axis('equal') # 等价于 ax1.set(aspect='euqal')，使得饼图在figure窗口放大缩小的过程中，保持圆形不变。

ax1[0].set_title('pie chart of the top 10 popular activities for new users', fontsize = 20)


ax1[1].barh(range(len(v)), v, tick_label=l)

ax1[1].set_title('bar chart of the top 10 popular activities for new users', fontsize = 20)
ax1[1].set_xlabel('times', fontsize = 15)


# In[ ]:




