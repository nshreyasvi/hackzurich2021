import pandas as pd
import io
import os
import gc

df = pd.read_csv('merged.csv')
#df = pd.read_csv('demo.csv')
#df = df.dropna(axis = 0, how = 'all', inplace = True)
df = df[df['DateTime'].notna()]
print(df.head())
print("Done")

df[['Day-Month', 'Time']] = df.DateTime.str.split(" ",expand=True)
#df[['year','month','day']] = df.Day-Month.str.split("-", expand=True)
#df['year-month'] = df[['year', 'month']].agg('-'.join, axis=1)

df = df.drop('DateTime',1)
df = df.drop('Time',1)
#df = df.drop('Day-Month',1)
#df = df.drop('day',1)
#f = df.drop('month',1)
#df = df.drop('year',1)

aggregation_functions = {'Latitude':'mean','Longitude':'mean','PositionNoLeap': 'mean', 'A2_RSSI': 'mean','A1_ratio':'mean' ,'A2_ratio':'mean','CurrentVelocity':'mean','DisruptionCode':'first','EventCode':'first'}
df_new = df.groupby(['Day-Month','AreaNumber','Track'],as_index=False).agg(aggregation_functions)

print(df_new.head())
print(len(df_new))
df_new.to_csv('month_agg.csv', index=True)