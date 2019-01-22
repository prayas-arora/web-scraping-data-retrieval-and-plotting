# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 21:29:18 2019

@author: Prayas
Roll number: 101503171
College: Thapar Institue of Engineering & Technology
"""
import numpy as np
import pandas as pd
import requests 
from bs4 import BeautifulSoup 
import matplotlib.pyplot as plt

def get_table(): 
    # the target we want to open	 
    url='https://en.wikipedia.org/wiki/Economy_of_the_European_Union '
    
    #open with GET method 
    resp=requests.get(url) 
    
    #http_respone 200 means OK status 
    if resp.status_code==200:
        # we need a parser,Python built-in HTML parser is enough . 
        soup=BeautifulSoup(resp.text,'html.parser')
        table = soup.find("table",{"class":"wikitable"})
        table_body = table.find('tbody')
        data=[]
        
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('th')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) # Get rid of empty values
        
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) # Get rid of empty values
        
        return data
    else:
        print("Error") 
        
table = get_table()
df = pd.DataFrame(table, columns=table[0])
df = df.iloc[12:,]
df = df.reset_index(drop=True)
df['Revenue $ millions'] = df['Revenue $ millions'].str.replace(",","").astype(float)
df['Employees'] = df['Employees'].str.replace(",","").astype(float)
df['Profit $ millions'] = df['Profit $ millions'].str.replace(",","").astype(float)

df['Revenue ($mn) per Employee'] = df['Revenue $ millions']/df['Employees']
df['Profit ($mn) per Employee'] = df['Profit $ millions']/df['Employees']
df['Profit margins (Profit / Revenue) (in %)'] = (df['Profit $ millions']/df['Revenue $ millions'])*100


total_revenue_share = df['Revenue $ millions'].sum()
df['Revenue Share(%)'] = (df['Revenue $ millions']/total_revenue_share)*100

df.to_csv('task1.csv', index=False)

print(df)

var = df.groupby(['Industry'], sort=False)['Profit margins (Profit / Revenue) (in %)'].max() #grouped sum of sales at Gender level
idx =  df.groupby(['Industry'], sort=False)['Profit margins (Profit / Revenue) (in %)'].transform(max) == df['Profit margins (Profit / Revenue) (in %)']
labels = df[idx]
labels = labels['Corporation']

fig = plt.figure(figsize=(16, 9))
ax1 = fig.add_subplot(1,1,1)
ax1.set_xlabel('Industry')  
ax1.set_ylabel('Profit Margin(%)')
ax1.set_title("Best Profit Margin in each Industry") 
plt.xticks(range(8), labels, rotation='horizontal')
plt.yticks(range(8), rotation='horizontal')
ax=var.plot(kind='bar')

rects = ax.patches

# Making labels.
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height, label, ha='center', va='bottom')
    
plt.savefig('bar_graph.png', dpi=600)    