import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from prometheus_client import Counter

# read data and make a copy of it in order to preserve original
data_Original= pd.read_csv("Inc_5000_Companies/INC 5000 Companies 2019.csv")
data=data_Original.copy()
#checking data types
print("\nDATATYPE: \n",data.dtypes)
# regex=True is needed if we want the key string("Billion") to be replaced by value string("*1e3")
# we mathematically evaluate each value using map(pd.eval)
data['revenue']=data['revenue'].replace({" ":"" , "Million":""},regex=True)
data['revenue']=data['revenue'].replace('Billion','*1e3',regex=True).map(pd.eval).astype(float)
# print(data['revenue'].tail(30))
print("\nDATA TYPE OF REVENUE: ",data['revenue'].apply(type).value_counts())
print("\n\nROWS,COLUMNS COUNT: ",data.shape)
# print("\n",data.head)
# print("\nCOLUMNS",data.columns)
# print("\nValues \n",data.axes)

data.drop(['profile', 'url','rank','yrs_on_list','founded','metro'], inplace=True, axis=1)
# print(data.head)
print("\nCOLUMNS: ",data.columns)
#What's the average revenue among companies on the list?
#Broken down by industry?
print("\nAVERAGE REVENUE BY INDUSTRY IN MILLIONS: \n",data.groupby(['industry']).mean().revenue)
print("\nAVERAGE REVENUE IN MILLIONS : ",data.revenue.mean())

# Which industries are most and least represented in the list?
# print("NUMBER OF COMPANIES IN A INDUSTRY: \n",data['industry'].value_counts())
print("\nHIGHEST NUMBER OF COMPANIES IN A INDUSTRY: ",data['industry'].value_counts().idxmax())
print("\nLEAST NUMBER OF COMPANIES IN A INDUSTRY: ",data['industry'].value_counts().idxmin())

# Which industries saw the largest average growth rate?
# print("\n LARGEST AVERAGE GROWTH RATE BY INDUSTRY \n",data.groupby(['industry']).mean().growth_percent)
print("\nLARGEST AVERAGE GROWTH RATE BY INDUSTRY: ",data.groupby(['industry']).mean().growth_percent.idxmax(),"-> ", data.groupby(['industry']).mean().growth_percent.max())

# Which companies had the largest increase in staff/new hires?
data = data.assign(increase_staff=data['workers'] - data['previous_workers'])
# print("\nCOMPANY HAVING LARGEST INCREASE IN STAFF: ", data.increase_staff.idxmax(axis=1))
print("\nCOMPANY HAVING LARGEST INCREASE IN STAFF: ", data[data.increase_staff == data.increase_staff.max()].name)

# Did any companies increase revenue while reducing staff?

print("\nCOMPANIES REDUCING THEIR STAFF AND INCREASING THEIR GROWTH: \n",data.loc[ (data.increase_staff < 0.0)  & (data.growth_percent> 500.0) ].sort_values(by=['increase_staff','growth_percent']))

#interesting geographic trends?

#In which state what industry is famous
data_group = data.groupby(['state'])['industry'].apply(lambda x: x.value_counts().index[0]).reset_index()
print("\nLARGEST INDUSTRY IN A STATE: \n", data_group)


#Which state is famous for a particular industry
print("\nBEST STATE FOR A INDUSTRY: \n",data.groupby(['industry'])['state'].apply(lambda x: x.value_counts().index[0]).reset_index())

#Which state has more growth?
print("\nSTATE HAVING MORE GROWTH: ",data.groupby('state').agg({'growth_percent':'sum'}).idxmax())

#for a state, which industries are more and less
s = data.groupby(['state','industry']).size()
print("\nSTATE - MORE INDUSTRIES: \n",s.loc[s.groupby(level=0).idxmax()].reset_index().drop(0,axis=1))
print("\nSTATE - LESS INDUSTRIES: \n",s.loc[s.groupby(level=0).idxmin()].reset_index().drop(0,axis=1))

#which industry has more revenue
print("\nINDUSTRY HAVING MORE REVENUE: ",data.groupby('industry').agg({"revenue":"sum"}).idxmax())

#for a state, max and min revenve industry
print("\n FOR EACH STATE, MAXIMUM AND MINIMUM REVENUE IN A INDUSTRY: \n",data.groupby([data.state, data.industry])["revenue"].agg(["max", "min"]).rename_axis(["state", "industry"]))