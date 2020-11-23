#!/usr/bin/env python
# coding: utf-8

# # Assignment 2

# For this assignment, the usage data of the Clevercogs platform in the Blackwood home and care project will be analysed. 
# As an innovative product, CleverCogs digitally enhances care services, and customers can achieve diversified digital activities through the platform. The dataset relates to personal characteristics (Excel file1 CustomerDataAnon) and platform usage (Excel file2 CC Data 2020).
# The analysis aspect will be mainly based on：Frequency (Time of year, the pandemic period in Scotland) and Correlation (Personal characteristics) of activities and users on Clevercogs platform.

# # Setup - Import data

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


# Set the figure space to Seaborn default style, with grids
sns.set_style('darkgrid')


# In[3]:


# Reading files. To prevent data loss, directly import Excel files and process the data
customer = pd.read_excel('./data/CustomerDataAnon.xlsx',index_col=0) # Import file1 CustomerDataAnon,set the first column to index
cc = pd.read_excel('./data/CC Data 2020.xlsx',
                   usecols='A:H',
                   names=[
                       'Time', 'Visitor ID', 'External ID', 'Identity', 'Location',
                       'Link Title', 'Link Type', 'Content Info'
                   ])  # Import file2 CC Data2020, read columns A to H, clarify column names


# In[4]:


# Return first 5 rows of file1, quickly test if dataframe has the right type of data in it
customer.head()


# In[5]:


# Return first 5 rows of file2, quickly test if dataframe has the right type of data in it
cc.head()


# # Describe data

# In this data experiment, 314707 X 18-panel data recorded in tabular form are used. The table collected the access records of people from 33 different areas of the UK using CleverCogs platform from Oct29 00:58 2018 to Oct30 13:16 2020. 
# 
# By reading unique values, the dataset includes 622 visitor ids, 1388 LinkTitles and 15 LinkTypes visited, as well as 396 external ids displayed by the platform when tourists visit. The External ID is also the Unique ID in this data experiment, associating different databases. Since there are only 396 external ids, but 622 visitor ids, we cannot track all of them. Therefore, in the subsequent processing of user information related data, data cleaning is needed, which cannot be cleaned by using unique ID data. In another table CustomerDataAnon, details of customers are recorded according to 441 unique ID, which is also the external ID displayed on the platform. Specifically, it includes the age, gender, date of birth, occupation status and physical condition of these persons. 

# In[6]:


# Use Dataframe.info() to find out general information summary of file1
customer.info()


# In[7]:


# Use Dataframe.info() to find out general information summary of file2
cc.info()


# # Preliminary data cleaning

# By importing data and describing data, we can see the complexity of existing data. In order to better perform the next step of the analysis, for missing data, errors and inconsistencies in data, data cleaning will be applied. Moreover, we could find some data confusion, such as Time and LinkTitle. Some elements were not recorded correctly, such as Row2156 and Row55556. 
# The data needs to be cleaned on a case-by-case basis for next steps.

# In[8]:


# Drop missing values
cc.dropna(subset = ['External ID'],inplace=True) # Consider along axes, operate inplace and return


# In[9]:


# Convert float ExternalId data to integer
cc['External ID'] = cc['External ID'].astype(int)


# In[10]:


# Remove the exception line where LinkTitle is numeric (time)
cc['LinkTitleType'] = cc['Link Title'].apply(lambda x:type(x).__name__)
cc = cc[cc['LinkTitleType']=='str']


# In[11]:


# Result of cleaning
# Time format
print(type(cc.loc[0,'Time']))
# Time range
print('Time range:',cc['Time'].max(),cc['Time'].min())

# Number of Location
tempDf = cc.groupby('Location').count()
print('Number of Location:',len(tempDf))

# Number of VisitorIds, including numbers without ExternalIds
tempDf = cc.groupby('Visitor ID').count()
print('Number of Visitor:',len(tempDf))

# Number of LinkTitle
tempDf = cc.groupby('Link Title').count()
print('Number of LinkTitle:',len(tempDf))

# Number of LinkType
tempDf = cc.groupby('Link Type').count()
print('Number of LinkType:',len(tempDf))

# Size of dataframe
print("Number of Row and column:",len(cc),len(cc.columns.to_list()))


# # Explore

# In[12]:


# Figure 1 Age distribution of users
# Set age range (yearRegion) into '0_10','11_20','21_30','31_40','41_50','51_60','61_70','71_80','81_90','91_100']
listBins = [0,10,20,30,40,50,60,70,80,90,100]
listLabels = ['0_10','11_20','21_30','31_40','41_50','51_60','61_70','71_80','81_90','91_100']
customer['yearRegion'] = pd.cut(customer['Age'], bins=listBins, labels=listLabels, include_lowest=True)
# Count people from each age range
tempDf = customer.groupby('yearRegion',as_index=False).count()
# Use a bar chart to show the number of people in each age range
sns.catplot(x='ID',y='yearRegion',kind='bar',data=tempDf).set(xlabel='Number of user',ylabel='Age range')
plt.title('Figure 1. Age distribution of Clevercogs users') # Add title
plt.show()


# According to Figure 1, the ages of users collected in this data experiment are mainly between 41 and 90 years old, among which users between 81 and 90 years old are the most, followed by users between 51 and 60 years old. In general, subjects are older people.

# In[13]:


# Figure 2 Gender distribution of users
# Group data and compute operations on them, Gender is indexed
tempDf = customer.groupby('Gender',as_index=False).count()
# Use pie chart to show the number of users by gender
customer.Gender.value_counts().plot.pie(autopct='%1.1f%%')
plt.title('Figure 2. Gender distribution of Clevercogs users') # Add title 
plt.show()


# From Figure 2, Female users are in the majority, but the number of Male and Female users is not very different.

# In[14]:


# Figure 3 Health-situation distribution of users
# Division of physical conditions
'''In this step, there are two condition descriptions were used for the user's physical condition in the original 
data: Staffplan and CareSysCondition. The health conditions of users under them are sometimes the same and 
sometimes different. In order to unify the data standards, we adopted the user health conditions embodied by 
CareSysCondition for data cleaning.'''
# Group data and compute operations on them, CareSysCondition is indexed
tempDf = customer.groupby('CareSysCondition',as_index=False).count()
# Use bar chart to show different health conditions
sns.catplot(x='ID',y='CareSysCondition',kind='bar',data=tempDf,height=9).set(xlabel='Number of user',ylabel='CareSysCondition')
plt.title('Figure 3. Health-situation distribution of users') # Add title
plt.show()


# According to Figure 3, among all the customer information collected, users needing Elderly care/support the most, mental health issues, cerebral palsy and dementia were also common.

# In[15]:


# Figure 4 The number of visits of different LinkTypes
# Group data and compute operations on them, LinkTitle and LinkType are indexed
tempDf = cc.groupby(['Link Title','Link Type'],as_index=False).count() 
tempDf.sort_values(by='Visitor ID',ascending=False,inplace=True) # Sort the data by VisitorId
# Use swarmplot to represent page view amounts
plt.figure(figsize=(25,10)) # Set canvas size
sns.swarmplot(x='Link Type',y='Visitor ID',data=tempDf).set(xlabel='LinkType',ylabel='Number of visits')
plt.title('Figure 4. The number of visits in different linktypes') # Add title
plt.show()
# List the top 5 most popular websites
print('Top5 most popular LinkTitles:',tempDf['Link Title'].to_list()[:5],tempDf['Visitor ID'].to_list()[:5])


# According to Figure 4, statistics on the access behaviours of the Internet platforms used in the past two years shows,  'Entertainment', 'My Interests', 'YouTube', 'Google' and 'My Music' had the highest click rates, Category and Internet LinkTypes were the most likely to be accessed. Because we want to look at how people of different characteristics use Clevercogs platform, a detailed analysis of the access behaviours of existing users and their basic personal information is more conducive for us to explore the differences.

# The following section focuses on the summary of the access information among LinkTypes and correlation with users.

# In[16]:


# Figure 5 The number of visits of different LinkTypes between Genders
# Group data and compute operations on them, ExternalId and LinkType are indexed
tempDf = cc.groupby(['External ID','Link Type'],as_index=False).count()
# Merge data, link  Externl ID in cc with ID in customer — being the common link
tempDf = pd.merge(left=tempDf,right=customer,how="inner",left_on='External ID',right_on='ID')
tempDf = tempDf.groupby(['Gender','Link Type'],as_index=False).count()
# Use bar chart to show differences
plt.figure(figsize=(25,15)) # Set canvas size
sns.barplot(x='Link Type',y='ID',hue='Gender',data=tempDf).set(xlabel='Link Type',ylabel='Number of visits')
plt.title('Figure 5. Number of visits of different linktypes between genders') # Add title
plt.show()


# In this part of the analysis, some interesting results emerged. According to the bar chart above, we can find that for website types with high visiting rates, such as Internet, category and HTMLPage, Female users are more than Male, while for other websites with low visiting rates, Male users are more than Female.

# In[17]:


# Figure 6 The number of visits by different age ranges
# Group data and compute operations on them, ExternalId is indexed
tempDf = cc.groupby(['External ID'],as_index=False).count()
# Merge data, link  Externl ID in cc with ID in customer — being the common link
tempDf = pd.merge(left=tempDf,right=customer,how="inner",left_on='External ID',right_on='ID')
# Use scatterplot to show general tendency of dependent variable to vary with independent variable
plt.figure(figsize=(20,10)) # Set canvas size
sns.scatterplot(x='Age',y='Link Type',data=tempDf).set(xlabel='Age',ylabel='Number of visits')
plt.title('Figure 6. Number of visits by different age ranges') # Add title
plt.show()


# Initially, I wanted to explore the relationship between age and page view, but it was hard to see any significant linear relationship between age them in the scatterplot. Overall, the distribution of visits in the whole age range is between 0 and 5000, but the entire distribution shows an inverted-U-shaped curve, which is a quadratic relationship. To briefly summarize, with the increase of age, users will gradually increase the number of visits to the platform, but the number of visits will decline after a certain age. This is actually consistent with our life; being too old or too young will make Internet access less convenient and less frequent.

# In[18]:


# Figure 7 Change of number of visits of different LinkTypes during 2018/10/29-2020/10-/30
# Use date and time formatting symbols to represent four-digit years and months
cc['Date'] = cc['Time'].apply(lambda x:x.strftime("%Y-%m")) 
# Group data and compute operations on them, LinkType and date are indexed
tempDf = cc.groupby(['Link Type','Date'],as_index=False).count()
tempDf.sort_values(by='Date',inplace=True) # Sort the data by date
# Use lineplot to show how the trend change over time
plt.figure(figsize=(25,15))# Set canvas size
sns.lineplot(x='Date',y='Visitor ID',hue='Link Type',markers=True,data=tempDf).set(xlabel='Time',ylabel='Number of visits')
plt.title('Figure 7. Change of number of visits of different LinkTypes during 29/10/2018-30/10/2020') # Add title
plt.show()


# According to Figure 7, we can see that the number of visits from December to February in 2018 and 2019 is the trough, specifically reflected in the synchronous decline of Internet and Category, the two most popular LinkTypes. During the epidemic this year, from March to May 2020, the number of visits to Internet and Category surged distinctly. The rest of the sites are essentially declining in the number of visits. Thus it can be seen that users' access habits are relatively fixed, and the popular mainstream website type is still in great demand.

# In[19]:


# Figure 8 Distribution of use in different Locations
# Heat map of the Number of access in differnt Location over Time
# Use date and time formatting symbols to represent four-digit years and months
cc['Year'] = cc['Time'].apply(lambda x:x.strftime("%Y-%m")) 
# Group data and compute operations on them, Location and Time are indexed
tempDf = cc.groupby(['Location','Year']).count()
tempDf.fillna(0,inplace=True) # Fill NaN values
tempDf = tempDf.unstack(level=-1)['Visitor ID'] # Replace NaN with VisitorID if the unstack produces missing values
# Create heatmap to show indensity
plt.figure(figsize=(20,10)) # Set canvas size
sns.heatmap(tempDf).set(xlabel='Time',ylabel='Location')
plt.title('Figure 8. Heat map of use in differnt Location over Time') # Add title
plt.show()


# In Figure 8, the slight colour means higher click rates. We can find that click rates of users at Belses and Broom Main Building area have been increasing gradually, while ones at Raeden Court and West area have been decreasing gradually in the past two years.

# # Reflection and Hypothesis

# Through the above analysis of use with different characteristics, the factors such as age, gender, living area and physical condition will influence the visiting behaviours of our user group. We can make the following hypothesis:

# - H1 Use of LinkType and Access frequency would change at different ages

# In[20]:


# Figure 9 Heatmap of use of LinkTypes and frequency by different age ranges
# Group data and compute operations on them, Location and Time are indexed
tempDf = cc.groupby(['External ID','Link Type'],as_index=False).count()
# Merge data, link  Externl ID in cc with ID in customer — being the common link
tempDf = pd.merge(left=tempDf,right=customer,how="inner",left_on='External ID',right_on='ID')
# Group data and compute operations on them
tempDf = tempDf.groupby(['Link Type','yearRegion']).count()
tempDf.fillna(0,inplace=True) # Fill NaN values
tempDf = tempDf.unstack(level=-1)['External ID'] # Replace NaN with VisitorID if the unstack produces missing values
# Create heatmap to show indensity
plt.figure(figsize=(10,10)) # Set canvas size
sns.heatmap(tempDf).set(xlabel='Age range',ylabel='Link Type')
plt.title('Figure 9. Heatmap of use of LinkTypes and access frequency by different age ranges') # Add title
plt.show()


# According to the use of LinkType and Access frequency would change at different ages (H1), we could intuitively find that age difference is not very obvious for niche websites. However, for popular sites, the age difference during use is stark. For example, older people are more likely to visit traditional websites, and younger people are more likely to visit platforms like YouTube. To test this hypothesis further, we need to find more data, do a more in-depth analysis, or use surveys and interviews to support our findings and hypothesis.

# - H2 Customer from different locations have different preferences for accessing websites

# In[21]:


# Figure 10 Heatmap of use of LinkTypes and access frequency at different locations
# Group data and compute operations on them, Location and LinkType are indexed
tempDf = cc.groupby(['Location','Link Type']).count()
tempDf.fillna(0,inplace=True) # Fill NaN values
tempDf = tempDf.unstack(level=-1)['Visitor ID']  # Replace NaN with VisitorID if the unstack produces missing values
# Create heatmap to show indensity
plt.figure(figsize=(15,10)) # Set canvas size
sns.heatmap(tempDf).set(xlabel='Link Type',ylabel='Location')
plt.title('Figure 10. Heatmap of use of LinkTypes and access frequency at different locations') # Add title
plt.show()


# For the hypothesis of 'Customer from different locations have different preferences for accessing websites', the numbers of accessing more popular LinkTypes such as Internet and Category are quite different in the location-based aspect. For niche sites, the differences between regions are not obvious because the overall frequency of visits to these sites is small. We can collect more comprehensive data including information such as region and income, set location as the control variable, conduct a statistical regression analysis, determine significance and confidence intervals to get the exact locational difference value.

# - H3 As time moves, development of technology and society, the user population may grow older or more widespread.

# In[22]:


# Figure 11 Number of access of different age ranges in full years range (29/10/2018-30/10/2019 & 31/10/2019-30/10/2020)
# Resolve the Time string into a tuple according to the specified format %d-%m-%Y, set time range
t=datetime.datetime.strptime('30-10-2019', "%d-%m-%Y") 
cc['2Year'] = cc['Time'].apply(lambda x:'2018-2019' if x<t else '2019-2020' )
# Summarize the number of access by different users in years
tempDf = cc.groupby(['External ID','2Year'],as_index=False).count()
# Merge data, associate the number of access with personal data
tempDf = pd.merge(left=tempDf,right=customer,how="inner",left_on='External ID',right_on='ID')
# Create boxplot
plt.figure(figsize=(20,20)) # Set canvas size
sns.boxplot(x='yearRegion',y='Visitor ID',hue='2Year',data=tempDf).set(xlabel='yearRegion',ylabel='click rate')
plt.title('Figure 11. Number of access of different age regions in years') # Add title
plt.show()


# According to the current number of access of different age ranges in H3, the number of Internet visits of users aged 20-50 years old remained basically the same during the two years, but for users aged 51-100 years old decreased in the second year. However, the overall average level of access was similar for users aged 20 to 70. As mentioned above, the main group of users is still between 40 and 70 years old because there are larger outliers and length of boxes in figures. The future development of CleverCogs can also combine the influence of the external environment on the user group in different age ranges to provide services and platform support further.
# 
# There is also a finding in the process that, for the LinkTypes with a high visiting rate, such as the Internet, category and HTMLPage, Female visitors are more than Male; while for other website types with a low accessing rate, Male visitors are more than Female. For this aspect of usage, we can also conduct classified research and service support.
# 
# For subsequent data experiment, we can continue the graphical method to understand the relationship between variables; more accurate corrections can also be achieved by collecting more comprehensive data and understanding users better; learn consumer behaviour and theoretically verify the frequency and correlation findings.

# In[ ]:




