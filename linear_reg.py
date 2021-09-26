import numpy as np 
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
import gc
import io
import os
import datetime as dt
from datetime import datetime, timedelta
import time
import scipy
import seaborn as sns
import streamlit as st
from scipy.stats import spearmanr
from pathlib import Path

st.set_page_config(page_title='HackZurich Siemens Challenge',layout = 'wide',initial_sidebar_state='auto')
st.title('Predicting Life expectancy of Train Tracks using multi-polyfit Models')
#area_number = 20
#track_number = 52
date_1 = "2021-02-01"
#position_1 = 300000

df = pd.read_csv('month_agg.csv')

col1,col2 = st.columns(2)
area_number = col1.selectbox('Select Area Number', options=df.AreaNumber.unique())
df_latitude_1 = df[df['AreaNumber']==area_number]
df_latitude_1 = df_latitude_1.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})

track_number = col1.selectbox('Select Track Number', options=df_latitude_1.Track.unique())
date = col1.text_input("Enter Date in format (YYYY-MM-DD)", date_1)
position_1 = col1.slider('Position Slider', min_value=97366, max_value=428060, step=1)

date_time_obj = datetime.strptime(date, '%Y-%m-%d')
df_latitude = df_latitude_1[(df_latitude_1['Track']==track_number)]
df_latitude = df_latitude.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})

#Finding closest
result_index = df_latitude['PositionNoLeap'].sub(position_1).abs().idxmin()
df_test = df_latitude.loc[[result_index]]
#df_test.to_csv('lat_long.csv',index=False)

position = df_test.iloc[0,6]

df['Day-Month'] = pd.to_datetime(df['Day-Month'], format='%Y-%m-%d')

df = df[(df['AreaNumber']==area_number) & (df['Track']==track_number)]
last_date = date_time_obj - timedelta(days=120)

#print(df['Day-Month'])
#print(last_date)
#print(date_time_obj)
#corr, _ = spearmanr(df['A1_ratio'], df['A2_RSSI'])
#print('Spearmans correlation: %.3f' % corr)

df = df[df['Day-Month']<=date]
df = df[df['Day-Month']>=last_date]

df['Day-Month']=df['Day-Month'].map(dt.datetime.toordinal)
#df['PositionNoLeap'] = np.cbrt(df['PositionNoLeap'])
#df['Day-Month'] = df['Day-Month'].replace('-','', inplace=True)
#df['Day-Month'] = pd.to_numeric(df['Day-Month'])
#print(df.sort_values(by=['Day-Month']))

#df = df.drop('Day-Month',1)
#df = df.drop('A1_ratio',1)
#df = df.drop('A2_ratio',1)
#df = df.drop('CurrentVelocity',1)

df = df.drop('Unnamed: 0',1)
#df = df.drop('PositionNoLeap',1)
df = df.drop('AreaNumber',1)
df = df.drop('Track',1)
df = df.drop('Latitude',1)
df = df.drop('Longitude',1)
df = df.drop('DisruptionCode',1)
df = df.drop('EventCode',1)
df = df.fillna(0)
#print(df.dtypes)
df['A2_ratio']=(df['A2_ratio']+df['A1_ratio'])/2
print("length: "+str(len(df)))
#if (len(df)<11):
#    st.write('There are less than 10 samples available for this Area & Track, risk prediction might be inaccurate')
x = df.drop('A2_RSSI',1)
y = df['A2_RSSI']

print(x.head())

x_1 = df['Day-Month'].to_numpy()
y_1 = df['A2_RSSI'].to_numpy()

x_p = df['PositionNoLeap'].to_numpy()
y_p = df['A2_RSSI'].to_numpy()

x_v = df['A2_ratio'].to_numpy()
y_v = df['A2_RSSI'].to_numpy()

#plt.plot(x_t[0], m*x_t[0] + b[0])
m_1, b_1 = np.polyfit(x_1, y_1, 1)
m_p, b_p = np.polyfit(x_p, y_p, 1)
m_v, b_v = np.polyfit(x_v, y_v, 1)
#1 = time 

print(m_1)
print(m_p)
print(m_v)

plt.plot(x_1, m_1*x_1 + b_1)
#plt.show()

#==============================================================================
y_t_1 = 2.9
y_t_1_5=2.0
y_t_2=1.9
y_t_2_5=1.6
y_t_3=1.5
y_t_3_5=1.2
y_t_4=1.1
y_t_4_5=0.9

y_p_t = m_p*position+b_p #Changes for specific position

x_t_1 = (y_t_1-b_1)/(m_1)-y_p_t*m_v
x_t_1_5 = (y_t_1_5-b_1)/(m_1)-y_p_t*m_v
x_t_2 = (y_t_2-b_1)/(m_1)-y_p_t*m_v
x_t_2_5 = (y_t_2_5-b_1)/(m_1)-y_p_t*m_v
x_t_3 = (y_t_3-b_1)/(m_1)-y_p_t*m_v
x_t_3_5 = (y_t_3_5-b_1)/(m_1)-y_p_t*m_v
x_t_4 = (y_t_4-b_1)/(m_1)-y_p_t*m_v
x_t_4_5 = (y_t_4_5-b_1)/(m_1)-y_p_t*m_v

col2.header("Results")
col2.write("Excellent rating RSSI signal might be present until: ")
#col2.text(str(datetime.fromordinal(int(x_t_1))).split(' ')[0]+" to "+
col2.write(str(datetime.fromordinal(int(x_t_1_5))).split(' ')[0])
col2.write("Good rating RSSI signal might be present until: ")
#col2.text(str(datetime.fromordinal(int(x_t_2))).split(' ')[0]+" to "+
col2.text(str(datetime.fromordinal(int(x_t_2_5))).split(' ')[0])
col2.write("Fair rating RSSI signal might be present until: ")
#col2.text(str(datetime.fromordinal(int(x_t_3))).split(' ')[0]+" to "+
col2.text(str(datetime.fromordinal(int(x_t_3_5))).split(' ')[0])
col2.write("Weak rating RSSI signal might be present until: ")
#col2.text(str(datetime.fromordinal(int(x_t_4))).split(' ')[0]+" to "+
col2.text(str(datetime.fromordinal(int(x_t_4_5))).split(' ')[0])

st.header('Use Scroll to zoom in and out of the map')
col1,col2,col3 = st.columns(3)
col1.header('Area Information')
col1.map(df_latitude)
col2.header('Track Information')
col2.map(df_latitude_1)
col3.header('Closest Position to input')
col3.map(df_test)
