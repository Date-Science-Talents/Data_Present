#!/usr/bin/env python
# coding: utf-8

# In[12]:


# Necessary import
import pandas as pd
import numpy as np


# In[13]:


c=pd.read_excel('./gender+tag.xlsx',index_col=0)


# In[14]:


c.head()


# In[15]:


c.groupby('tags',as_index=False).count()


# In[16]:


c.groupby('gender',as_index=False).count()


# In[17]:


c.groupby(['tags', 'gender'])['gender'].agg({'count'}).reset_index()


# In[ ]:





# In[ ]:





# In[ ]:




