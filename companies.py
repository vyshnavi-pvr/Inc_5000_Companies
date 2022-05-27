import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data= pd.read_csv("Inc_5000_Companies/INC 5000 Companies 2019.csv")
print("\n\nrows,columns ->",data.shape)
print("\n",data.head)