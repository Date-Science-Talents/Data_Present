#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# read data
df_1 = pd.read_excel('CustomerDataAnon.xlsx')
df_1_use = df_1[['ID', 'Gender']]

df_2 = pd.read_excel('cleaned_data.xlsx')
df_2_use = df_2[['ExternalID', 'LinkType']].rename(columns={'ExternalID': 'ID'})
df_2_use = df_2_use[pd.notnull(df_2_use['LinkType'])]


# In[2]:


# merge
df_3 = pd.merge(df_2_use, df_1_use, how='left')
df_3 = df_3[pd.notnull(df_3['Gender'])]
df_3_use = df_3[['LinkType', 'Gender']]
# groupby, to screen out the number of different 'LinkType' and different 'Gender'
df_4 = df_3_use.groupby(['LinkType', 'Gender'])['Gender'].agg({'count'}).reset_index()
df_4_M = df_4[df_4['Gender'] == 'M'].rename(columns={'Gender': 'Gender_M', 'count': 'count_M'})
df_4_F = df_4[df_4['Gender'] == 'F'].rename(columns={'Gender': 'Gender_F', 'count': 'count_F'})
# merge, get the result dataframe: df_5, index index: 'LinkType'; Contains columns: 'count_M', 'count_F' 
df_5 = pd.merge(df_4_M, df_4_F, how='left')
del df_5['Gender_M'], df_5['Gender_F'] 
df_5.fillna(0, inplace=True)       # NaN data is populated with 0
df_5 = df_5.sort_values(by='count_M', ascending=True)
df_5.set_index(['LinkType'], inplace=True)


# In[3]:


# draw bidirectional bar chart
index = np.arange(len(df_5))
lColor = (1/256, 1/256, 256/256, 3/3)     # blue
rColor = (256/256, 1/256, 1/256, 3/3)      # red
plt.figure(figsize=(16,6))
# using the arrangement, the data is stacked up, that is, a multi-dimensional bar chart
plt.barh(
    index, 
    df_5['count_M'], 
    color = lColor
)
plt.barh(
    index, 
    -df_5['count_F'], 
    color = rColor
)
plt.xticks([-40000, -20000, 0, 20000, 40000], ['40000', '20000', '0', '20000', '40000'])    # Set the scale (originally negative for left side of the origin, now all positive)
plt.yticks(index, df_5.index)
plt.legend(['M', 'F'])
plt.show()


# In[ ]:




