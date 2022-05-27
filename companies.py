import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# read data and make a copy of it in order to preserve original
data_Original= pd.read_csv("Inc_5000_Companies/INC 5000 Companies 2019.csv")
data=data_Original.copy()
#checking data types
print(data.dtypes)
# regex=True is needed if we want the key string("Billion") to be replaced by value string("*1e3")
# we mathematically evaluate each value using map(pd.eval)
data['revenue']=data['revenue'].replace({" ":"" , "Million":""},regex=True)
data['revenue']=data['revenue'].replace('Billion','*1e3',regex=True).map(pd.eval).astype(float)
# print(data['revenue'].tail(30))
print("\nData types in revenue",data['revenue'].apply(type).value_counts())
print("\n\nROWS,COLUMNS COUNT->",data.shape)
# print("\n",data.head)
# print("\nCOLUMNS",data.columns)
# print("\nValues \n",data.axes)

data.drop(['profile', 'url','rank','yrs_on_list','metro'], inplace=True, axis=1)
# print(data.head)
print("\nCOLUMNS",data.columns)
#What's the average revenue among companies on the list?
#Broken down by industry?
# print(data.value_counts([]))
## print("\nAVERAGE REVENUE BY INDUSTRY IN MILLIONS\n",data.groupby(['industry']).mean().revenue)
## print("\nAVERAGE REVENUE IN MILLIONS : ",data.revenue.mean())

# Which industries are most and least represented in the list?
# print("NUMBER OF COMPANIES IN A INDUSTRY: \n",data['industry'].value_counts())
print("HIGHEST NUMBER OF COMPANIES IN A INDUSTRY: \n",data['industry'].value_counts().idxmax())
print("LEAST NUMBER OF COMPANIES IN A INDUSTRY: \n",data['industry'].value_counts().idxmin())

# Which industries saw the largest average growth rate?
# print("\n LARGEST AVERAGE GROWTH RATE BY INDUSTRY \n",data.groupby(['industry']).mean().growth_percent)
print("\nLARGEST AVERAGE GROWTH RATE BY INDUSTRY \n",data.groupby(['industry']).mean().growth_percent.idxmax(),"-> ", data.groupby(['industry']).mean().growth_percent.max())

# Which companies had the largest increase in staff/new hires?
data = data.assign(increase_staff=data['workers'] - data['previous_workers'])
print("\nCOMPANY HAVING LARGEST INCREASE IN STAFF", data.increase_staff.idxmax(axis=1))
print("\nCOMPANY HAVING LARGEST INCREASE IN STAFF", data[data.increase_staff == data.increase_staff.max()].name)




