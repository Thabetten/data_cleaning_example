#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import libraries and data.

import pandas as pd
import numpy as np
from collections import Counter

#df_profiles_q1 is profile data to be analyzed as per question 1.
df_profiles_q1 = pd.read_excel('Data_set1.xlsx', header = 0, dtype = 'object')
#df_new_data_q2 is the data for purchase in question 2 of the assignment.
df_new_data_q2 = pd.read_excel('DataSet7734_USA_Consumers_test-ver2.xls')
#df_old data contains the old data already owned by piple for question 2 of the assignment.
df_old_data_q2 = pd.read_excel('DataSet7734_USA_Consumers_test-ver2.xls', sheet_name = 'Current-07734ZipCode')

#Print shapes to have a general idea of the data.

print(df_profiles_q1.shape)
print(df_new_data_q2.shape)
print(df_old_data_q2.shape)


# In[2]:


#Here we find the frequency of email domain used by creaing a seperate list of domains through splitting the string.
#We make a dataframe out of the splits column.
email =  df_profiles_q1.email.str.split(pat = '@', expand = True)

#We get the frequency of each Value.
d_count = email[1].value_counts()


#Make a dataframe of this.
counts_df = pd.DataFrame(d_count)


#This will hold the percentage of use value for each domain.
dom_per = []


#This loop will ger the percentage and add it to dom_per.
for i in counts_df[1]:
    dom_per.append(i*100/sum(counts_df[1]))

    
#We add a column to the dataframe for percent of users per domain with dummy name.
counts_df['Up'] = dom_per

#We reindex the new dataframe.
counts_df.reset_index(inplace = True)

#Rename the columns.
counts_df.columns = ['Domain', '# of Users', 'Percent of Users']

print(counts_df)



# 
# 
# 

# In[6]:


#Prefixes can easily be added as a fixed list or brought in as a data frame.
#prefixes = ['20', '21', '22', '30', '31', '32', '40', '41', '42', '50', '51', '52', '60', '61', '62']

df_prefixes = pd.read_excel('Data_set1.xlsx', header = 0, sheet_name = 'mobile prefixes', dtype = 'str')
prefixes = list(df_prefixes['mobile prefixes'])

num_list = []


#Remove all unnecessary columns from the data frame for ease.
df_profiles_q1_reduced = df_profiles_q1.drop(['index', 'first', 'last', 'gender'], axis = 1)


#Check shape is as expected.
print(df_profiles_q1_reduced.shape)


#This loop creates a string of two digit numbers from 0 to 99 as might appear at the beginning of a phone number.
for z in range(0, 99):
    if z < 10:
        num_list.append('0' + str(z))
    else:
        num_list.append(str(z))
        
#land pres is all combos of two digits not in mobile pregfixes.

landpres = [x for x in num_list if x not in prefixes]

phone_lines = []


#This loop will iterate through the rows in the reduced profile data and will check if the first two digits are
#for a landline or mobile phone and then count the number of each for the row.
#The two elif statements are equivalent. 
for i in df_profiles_q1_reduced.itertuples(index = False):
    mobile = 0
    landline = 0
    phones = []
    for k in i[1:9]:
        k = str(k)
        if k[0:2] in prefixes:
            mobile += 1
        #elif k[0:2] in num_list and k[0:2] not in prefixes:
        elif k[0:2] in landpres:
            landline += 1
    phones.append(i[0]), phones.append(mobile), phones.append(landline)
    phone_lines.append(phones)



df_phones = pd.DataFrame(phone_lines, columns = ['email', '# Mobiles', '# Landlines'])

pd.to_numeric(df_phones['# Mobiles'])
pd.to_numeric(df_phones['# Landlines'])

more_than_one_phone = df_phones.loc[(df_phones['# Mobiles'] > 1) | (df_phones['# Landlines'] > 1)]
                                          



print('Number of people with N of mobile phones.', '\n', df_phones['# Mobiles'].value_counts().sort_index())

print('Number of people with N landlines.', '\n', df_phones['# Landlines'].value_counts().sort_index())

print('% of people with N mobile phones.', '\n', (df_phones['# Mobiles'].value_counts().sort_index()/5000)*100)

print('% of people with N landlines', '\n', (df_phones['# Landlines'].value_counts().sort_index()/5000)*100)


#Print a single entry to compare to a line in the original data (I did this in Excel).
print(df_phones.iloc[1])


# In[7]:


#In this section we will calculate the fill values for columns in the old data for Kearney N.J. and the sample data for purchase.
#We will do this by finding the ratio of values the are not NA to the total number of values.

#Establish list of headers for convenience.

raw_list_new_data = list(df_new_data_q2.columns.values)
raw_list_old_data = list(df_old_data_q2.columns.values)

#Create empty lists for fill ratios.

fill_new = []
fill_old = []
comparison_old_new = []


#The fill value is calculated by dropping NA values from each column and dividing by the original length of the column.
#looking at the data in a spreadsheet reveals that some values are filled in phone numbers for the old data that should be NA.
#I.E. some phone numbers as '0' in the old data.
#This will be remedied buy replacing zeros with NA values.

df_old_data_q2['phone number'].replace(0, np.nan, inplace = True)


#This iterates of columns in the new data to get the fill percentage.


for i in raw_list_new_data:
    fill_new.append(len(df_new_data_q2[str(i)].dropna())*100/len(df_new_data_q2[str(i)]))

#This creates a list pairing the column head with the fill percentage.
fill_by_col_new = list(zip(raw_list_new_data, fill_new))

#Do the same for the old data.

for k in raw_list_old_data:
    fill_old.append((len(df_old_data_q2[str(k)].dropna()))/len(df_old_data_q2[str(k)])*100)

fill_by_col_old = list(zip(raw_list_old_data, fill_old))

#Print both.
print('The fill value by column of the old data.', '\n', fill_by_col_old)
print('\n', 'The fill value by column of the new data.', '\n', fill_by_col_new)

#Make the lists into dataframes and get a mean fill value.

fill_old_df = pd.DataFrame(fill_old)
fill_new_df = pd.DataFrame(fill_new)

print('\n', 'The mean fill of the old data is', '\n', fill_old_df.mean())

print('\n', 'The mean fill of the new data is', '\n', fill_new_df.mean())


# In[70]:


#While the new data seems to have a better fill than the old data, it still may not be of high quality.


print(df_new_data_q2.iloc[1:25])


# In[8]:


#First a sample of the data is inpspected. It is immediately obvious two phone numbers are of the wrong length.
#It is also immediately obvious that data seems sorted by both birthdate and alphabetically by name.
#In addition the first two 'Chalie Bowman' born a day appart live on the same street.
#This seems suspicious. 

#Next we find the dimensions of the data.
print(df_new_data_q2.shape)


dupes = df_new_data_q2['EMail'].value_counts()

print(dupes[0:5])








# In[9]:


#We now see a significant amount of the data in the new data set is repeated entries and possibly spurious.
#More tests should be run. First We drop all duplicate emails.

df_new_data_q2_no_dupe = df_new_data_q2.drop_duplicates(subset = ['EMail'])

print(df_new_data_q2_no_dupe.shape)


#It is also seen that the city of Hazlet is included in the cities. Hazlet has a different zip code 07730.
#We drop rows from Hazlet.

df_new_data_q2_no_dupe = df_new_data_q2_no_dupe[df_new_data_q2_no_dupe.City != 'HAZLET TOWNSHIP']

print(df_new_data_q2_no_dupe.shape)

#As a final test we will see if any phone numbers are also repeated.

df_new_data_q2_no_dupe_final = df_new_data_q2_no_dupe.drop_duplicates(subset = ['Phone Number'])

print(df_new_data_q2_no_dupe_final.shape)


# In[66]:


#As can be seen the original data set for purchase is largely composed of incorrect or repeated values in fields that should
#be unique such as phone number and email.
#Further cleaning of this set is possible however it is not necessary as the data is poor or more likely fake.

