#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Necessary import
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time
import datetime # standard Python library for dates and times
# Import statsmodels Python statistical module for data exploration and visualization
import statsmodels.api as sm


# In[2]:


customer = pd.read_excel('./CustomerDataAnon.xlsx',index_col=0)
cc = pd.read_excel('./cleaned_data.xlsx',index_col=0)


# In[3]:


customer.head()


# In[4]:


cc.head()

# In[6]:


# Heatmap of use of LinkTitle and access frequency at different health conditions
tempDf = cc.groupby(['ExternalID','LinkTitle'],as_index=False).count()
# Merge data, link  Externl ID in cc with ID in customer — being the common link
tempDf = pd.merge(left=tempDf,right=customer,how="inner",left_on='ExternalID',right_on='ID')
tempDf = tempDf.groupby(['LinkTitle','CareSysCondition']).count()
tempDf = tempDf.unstack(level=-1)['VisitorID']
# Create heatmap to show indensity
plt.figure(figsize=(15,50)) # Set canvas size
sns.heatmap(tempDf).set(xlabel='CareSysCondition',ylabel='LinkTitle')
plt.title('Heatmap of use of LinkTitle and access frequency at different health conditions') # Add title
plt.show()


# In[7]:

# Figure e4
# Heatmap of use of LinkTitle and access frequency at different health conditions
tempDf = cc.groupby(['ExternalID','LinkTitle'],as_index=False).count()
# Merge data, link  Externl ID in cc with ID in customer — being the common link
tempDf = pd.merge(left=tempDf,right=customer,how="inner",left_on='ExternalID',right_on='ID')
tempDf = tempDf.groupby(['LinkTitle','CareSysCondition']).count()
tempDf = tempDf.unstack(level=-1)['VisitorID']
# Create heatmap to show indensity
plt.figure(figsize=(15,30)) # Set canvas size
sns.heatmap(tempDf).set(xlabel='CareSysCondition',ylabel='LinkTitle')
plt.title('Heatmap of use of LinkTitle and access frequency at different health conditions') # Add title
plt.show()



# In[8]:


# The number of visits of different LinkTypes between Genders
# Group data and compute operations on them, ExternalId and LinkType are indexed
tempDf = cc.groupby(['ExternalID','LinkType'],as_index=False).count()
# Merge data, link  Externl ID in cc with ID in customer — being the common link
tempDf = pd.merge(left=tempDf,right=customer,how="inner",left_on='ExternalID',right_on='ID')
tempDf = tempDf.groupby(['Gender','LinkType'],as_index=False).count()
# Use bar chart to show differences
plt.figure(figsize=(25,15)) # Set canvas size
sns.barplot(x='LinkType',y='ExternalID',hue='Gender',data=tempDf).set(xlabel='LinkType',ylabel='Number of visits')
plt.title('Number of visits of different linktypes between genders') # Add title
plt.show()


# In[21]:

# The number of visits of different LinkTypes between Genders
# Group data and compute operations on them, ExternalId and LinkType are indexed
tempDf = cc.groupby(['ExternalID','LinkType'],as_index=False).count()
# Merge data, link  Externl ID in cc with ID in customer — being the common link
tempDf = pd.merge(left=tempDf,right=customer,how="inner",left_on='ExternalID',right_on='ID')
tempDf = tempDf.groupby(['Gender','LinkType'],as_index=False).count()
# Use bar chart to show differences
plt.figure(figsize=(25,15)) # Set canvas size
result=tempDf.pivot_table(
       values='LinkType',
       index='ExternalID',
       columns='Gender',
       aggfunc=numpy.sum
       )
index=numpy.arange(len(result))
plt.title('Number of visits of different linktypes between genders') # Add title
plt.show()

# Problems to solve: 1. would the length of Figure e4 affect the entire layout of our infographics 2. unsuccessful practice of bidirectional bar chart

customer.iloc[:,0:1]


# Problem 3 drop U in Gender or not？


