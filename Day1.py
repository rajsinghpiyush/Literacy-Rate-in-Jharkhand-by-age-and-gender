import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = 'DDW-2000C-08.xlsx'
sheet_name = 'C-08'

df = pd.read_excel("C:\\Python CA2\\DDW-2000C-08.xlsx")

print("First 15 rows of raw data:")
print(df.head(15))

header_row1 = 5  
header_row2 = 6  
data_start_row = 7
headers1 = df.iloc[header_row1].values
headers2 = df.iloc[header_row2].values
