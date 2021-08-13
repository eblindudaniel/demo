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

#read only selected columns for time based analisys
target = pd.read_csv("ais.csv", delimiter=",",usecols = ['VesselType','Length','Width','LAT','LON','SOG','COG'], low_memory = True)





#filter bad records (like NaN) from the file, so it can be processed
#enc = OneHotEncoder(handle_unknown='ignore')
#enc.fit(X)
target = pd.DataFrame(target).dropna()



#print myData
est = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='uniform')
est.fit(target)
Xt = est.transform(target)





pd.DataFrame(Xt,columns=['VesselType','Length','Width','Latitude','Longitude','Speed over Ground','Course over Ground']).head(200000).to_csv("To_CaMML_time_series.csv",index = False)
