import pandas as pd
import io 
import os
import gc
import geopy.distance
import numpy as np

df_rssi = pd.read_csv('rssi.csv')
df_velocities = pd.read_csv('velocities.csv')
df_disruption = pd.read_csv('disruptions.csv')
df_events = pd.read_csv('events.csv')

print("Done!")

df_rssi = df_rssi.drop('ID',1)
df_velocities = df_velocities.drop('ID',1)
df_disruption = df_disruption.drop('ID',1)
df_events = df_events.drop('ID',1)

df_disruption = df_disruption[(df_disruption['DisruptionCode'] == 960862258) | (df_disruption['DisruptionCode'] == 960861952) | (df_disruption['DisruptionCode'] == 1698873074) | (df_disruption['DisruptionCode'] == 1698873079) | (df_disruption['DisruptionCode'] == 1698873080)]
df_events = df_events[(df_events['EventCode'] == 960862258) | (df_events['EventCode'] == 960861952) | (df_events['EventCode'] == 1698873074) | (df_events['EventCode'] == 1698873079) | (df_events['EventCode'] == 1698873080)]

df_disruption = df_disruption.drop('Description',1)
df_events = df_events.drop('Description',1)

df_rssi['A1_ratio'] = df_rssi['A1_ValidTel']/df_rssi['A1_TotalTel']
df_rssi['A2_ratio'] = df_rssi['A2_ValidTel']/df_rssi['A2_TotalTel']

df_rssi = df_rssi.drop('A1_TotalTel',1)
df_rssi = df_rssi.drop('A1_ValidTel',1)
df_rssi = df_rssi.drop('A2_TotalTel',1)
df_rssi = df_rssi.drop('A2_ValidTel',1)

'''
for i in range(0,len(df_rssi)):
    coords_1 = (df_rssi.iloc[i-1,6],df_rssi.iloc[i-1,7])
    coords_2 = (df_rssi.iloc[i,6],df_rssi.iloc[i,7])
    df_rssi.iloc[i,-1] = (geopy.distance.geodesic(coords_1, coords_2).km)
    print('Finished processing for '+str(i)+' row')
    gc.collect()
'''
#df_rssi['latitude_change'] = df_rssi.Latitude - df_rssi.Latitude.shift(1)
#df_rssi['longitude_change'] = df_rssi.Longitude - df_rssi.Longitude.shift(1)

#coords_1 = (df_rssi['Latitude'], df_rssi['Longitude'])
#coords_2 = (df_rssi['latitude_change'], df_rssi['longitude_change'])
#df_rssi.loc['Distance Travelled'] = geopy.distance.geodesic(coords_1,coords_2)

#df_rssi = df_rssi.drop('Latitude',1)
#df_rssi = df_rssi.drop('Longitude',1)
#df_rssi = df_rssi.drop('latitude_change',1)
#df_rssi = df_rssi.drop('longitude_change',1)

df_rssi_velocties = pd.merge(df_rssi, df_velocities, on="DateTime", how='outer')

df_rssi_velocties = df_rssi_velocties.drop('AllowedVelocity',1)
df_rssi_velocties = df_rssi_velocties.drop('EmergencyStopLimit',1)
df_rssi_velocties = df_rssi_velocties.drop('Position',1)

df_f_1 = pd.merge(df_rssi_velocties, df_disruption, on="DateTime", how='outer')
df_f = pd.merge(df_f_1, df_events, on="DateTime", how='outer')
df_f = df_f[df_f['A2_RSSI'].notna()]

#df_rssi_one_track = df_rssi_velocties[(df_rssi_velocties['AreaNumber']==33) & (df_rssi_velocties['Track']==1)]
df_one_track = df_f[(df_f['AreaNumber']==33) & (df_f['Track']==1)]
print(df_f)
#df_rssi_velocties.to_csv('test.csv', index=False, compression='gzip')
#df_rssi_one_track.to_csv('one_track.csv',index=False, compression='gzip')
df_one_track.to_csv('one_track_f.csv',index=False, compression='gzip')
df_f.to_csv('merged.csv',index=False)#, compression='gzip')