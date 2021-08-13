import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.preprocessing import OneHotEncoder 
import os


#download sample if doesn't exist
filename="AIS_2020_01_01"
if os.path.isfile("ais.csv")==False:
    print 'downloading file unsafely'
    os.system('wget https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2020/{}.zip'.format(filename))
    os.system("unzip {}.zip".format(filename))
    os.system("mv {}.csv ais.csv".format(filename))



target = pd.read_csv("ais.csv", delimiter=",", low_memory = True)

#filter bad records (like NaN) from the file, so it can be processed
#enc = OneHotEncoder(handle_unknown='ignore')
#enc.fit(X)
target = pd.DataFrame(target).dropna()


#make vessel speed averagie
groupby_avg1 = target.groupby(['MMSI']).SOG.median()
groupby_avg2 = target.groupby(['MMSI']).COG.median()


groupby_avg3 = target.groupby(['MMSI']).Length.max()
groupby_avg4 = target.groupby(['MMSI']).Width.max()
groupby_avg5 = target.groupby(['MMSI']).Status.nunique()


df_outer1 = pd.merge(groupby_avg1, groupby_avg2, on='MMSI', how='outer')
df_outer2 = pd.merge(groupby_avg3, groupby_avg4, on='MMSI', how='outer')


df_final1 = pd.merge(df_outer1, df_outer2, on='MMSI', how='outer')
df_final2 = pd.merge(df_final1, groupby_avg5, on='MMSI', how='outer')



track_summary=df_final2[['SOG','COG','Length','Width','Status']]

est = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='uniform')
est.fit(df_final2)
Xt = est.transform(df_final2)

pd.DataFrame(Xt,columns=['Speed over Ground','Course over Ground','Length','Width','Number of status changes']).head(200000).to_csv("To_CaMML_track_summaries.csv",index = False)

